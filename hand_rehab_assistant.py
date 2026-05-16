import cv2
import mediapipe as mp
import numpy as np
import math
import time

try:
    from clinical_modules import (
        ClinicalAccuracyFilter,
        VirtualSensei,
        RecoveryPredictor,
        TherapistDashboard,
        EmergencyPause,
    )
except ImportError:
    print("Please make sure clinical_modules.py is in the same directory.")
    ClinicalAccuracyFilter = None

class HandRehabAssistant:
    """
    A class-based application for hand rehabilitation tracking using MediaPipe.
    Detects gestures (Fist, Opposition, Extension) and calculates joint angles (ROM).
    """

    def __init__(self, width=640, height=480):
        """
        Initialize MediaPipe Hands, drawing tools, and camera.
        """
        self.width = width
        self.height = height

        # MediaPipe Hands initialization
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            min_detection_confidence=0.7,
            max_num_hands=1,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Webcam initialization
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Try DirectShow for Windows
        if not self.cap.isOpened():
            print("Camera index 0 failed. Trying index 1...")
            self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        # 1. Initialize Clinical Modules
        if ClinicalAccuracyFilter:
            self.accuracy_filter = ClinicalAccuracyFilter(window_size=5)
            self.sensei = VirtualSensei(target_angle=90, tolerance=15, hold_duration=3.0)
            self.predictor = RecoveryPredictor(db_path="rehab_data.db")
            self.dashboard = TherapistDashboard(db_path="rehab_data.db")
            self.pause_guard = EmergencyPause(confidence_threshold=0.5, grace_frames=5)
            
            # Predict recovery
            pred_result = self.predictor.predict()
            if "predicted_angle" in pred_result:
                self.ml_prediction_text = f"Predicted Recovery: +{pred_result.get('improvement_pct', 0)}%"
            else:
                self.ml_prediction_text = "Predicted Recovery: Need more data"
                
            # Generate static dashboard background once 
            self.dashboard.generate()
        else:
            self.accuracy_filter = None

    def calculate_distance(self, p1, p2):
        """
        Calculates Euclidean distance between two 3D landmarks (using x and y mostly for 2D plane).
        Using 2D distance for robust gesture detection on screen plane.
        """
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def calculate_angle_law_of_cosines(self, p1, p2, p3):
        """
        Calculates the angle at p2 formed by lines p1-p2 and p2-p3 using the Law of Cosines.
        
        Math Explanation:
        Given three points A(p1), B(p2), C(p3):
        1. Calculate lengths of sides of the triangle ABC:
           a = length(B to C)
           c = length(A to B)
           b = length(A to C)
        
        2. Law of Cosines formula:
           b^2 = a^2 + c^2 - 2ac * cos(B)
        
        3. Rearranging to solve for angle B (theta):
           cos(B) = (a^2 + c^2 - b^2) / (2ac)
           angle B = arccos( (a^2 + c^2 - b^2) / (2ac) )
        """
        # Calculate lengths of sides (using 3D coordinates for accuracy in depth if needed, 
        # but MediaPipe z is relative. We stick to x,y for screen processing or standard Euclidean).
        # We will use simple 2D Euclidean for screen visual angle, or 3D if z implies depth.
        # MediaPipe landmarks have x, y (normalized 0-1) and z (relative depth).
        # We'll use x and y for screen-based ROM.
        
        # Side lengths
        a = math.sqrt((p2.x - p3.x)**2 + (p2.y - p3.y)**2) # Distance p2-p3
        c = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2) # Distance p1-p2
        b = math.sqrt((p1.x - p3.x)**2 + (p1.y - p3.y)**2) # Distance p1-p3 - opposite to angle

        # Prevent division by zero
        if a * c == 0:
            return 0.0

        # Calculate cosine of the angle
        cos_angle = (a**2 + c**2 - b**2) / (2 * a * c)

        # Clamp value to [-1, 1] to handle float precision errors
        cos_angle = max(-1.0, min(1.0, cos_angle))

        # Calculate angle in radians and convert to degrees
        angle_rad = math.acos(cos_angle)
        angle_deg = math.degrees(angle_rad)

        return angle_deg

    def detect_gesture_and_rom(self, landmarks):
        """
        Analyzes landmarks to determine the current gesture and calculates relevant angles.
        Returns: gesture_name, angle_value (relevant to the gesture)
        """
        gesture = "Unknown"
        rom_angle = 0.0

        # Define landmarks (names for clarity)
        # Thumb: 1-4, Index: 5-8, Middle: 9-12, Ring: 13-16, Pinky: 17-20
        # wrist = landmarks[0]
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        
        wrist = landmarks[0]

        # ---------------------------------------------------------
        # 1. Finger Opposition (Thumb tip touches Index tip)
        # ---------------------------------------------------------
        dist_thumb_index = self.calculate_distance(thumb_tip, index_tip)
        # Loosened threshold to 0.1 for easier pinch detection
        if dist_thumb_index < 0.1: 
            gesture = "Finger Opposition"

        # ---------------------------------------------------------
        # 2. Fist Clench (Fingertips close to palm/wrist)
        # ---------------------------------------------------------
        
        # Calculate average distance of tips to wrist
        tips = [index_tip, middle_tip, ring_tip, pinky_tip]
        avg_dist_to_wrist = sum([self.calculate_distance(tip, wrist) for tip in tips]) / 4
        
        # Check thumb is tucked in - loosened to 0.2
        thumb_folded = self.calculate_distance(thumb_tip, landmarks[17]) < 0.2

        # Loosened heuristic for fist: avg dist < 0.35
        if avg_dist_to_wrist < 0.35:
             gesture = "Fist Clench"
             
        # ---------------------------------------------------------
        # 3. Hand Extension (All fingers spread out)
        # ---------------------------------------------------------
        
        # Angle at PIP for all 4 fingers
        angle_index_pip = self.calculate_angle_law_of_cosines(landmarks[5], landmarks[6], landmarks[7])
        angle_middle_pip = self.calculate_angle_law_of_cosines(landmarks[9], landmarks[10], landmarks[11])
        angle_ring_pip = self.calculate_angle_law_of_cosines(landmarks[13], landmarks[14], landmarks[15])
        angle_pinky_pip = self.calculate_angle_law_of_cosines(landmarks[17], landmarks[18], landmarks[19])
        
        # Check if open palm: Average distance is large
        if avg_dist_to_wrist > 0.4:
            gesture = "Hand Extension"

        # ---------------------------------------------------------
        # Metric
        # ---------------------------------------------------------
        # For simplicity, returning the average PIP angle of all 4 fingers
        rom_angle = (angle_index_pip + angle_middle_pip + angle_ring_pip + angle_pinky_pip) / 4.0

        # Override / Priority Logic
        if dist_thumb_index < 0.1:
            gesture = "Opposition"
        elif avg_dist_to_wrist < 0.35:
            gesture = "Fist Clench"
        elif avg_dist_to_wrist > 0.4:
             gesture = "Hand Extension"
        
        return gesture, rom_angle

    def get_processed_frame(self):
        """
        Captures a frame, processes key landmarks, and returns the image and data.
        Returns:
            image (numpy array): The specific frame with drawings.
            results (mediapipe results): Raw results.
            gesture (str): Detected gesture name.
            rom (float): Range of Motion angle.
            landmarks (list): List of landmark objects if found, else None.
        """
        if not self.cap.isOpened():
            return None, None, "Error", 0, None

        success, image = self.cap.read()
        if not success:
            return None, None, "Empty Frame", 0, None

        # Flip the image horizontally
        image = cv2.flip(image, 1)
        
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process
        results = self.hands.process(image_rgb)
        
        gesture = "Unknown"
        rom = 0.0
        landmarks = None
        
        # Fake hand_data object just to satisfy EmergencyPause structure 
        class HandDataMock:
            pass
        mock_hand = HandDataMock()
        mock_hand.landmarks = results.multi_hand_landmarks if results.multi_hand_landmarks else None
        
        # 5. Emergency Pause (Robustness)
        if self.accuracy_filter and self.pause_guard.check(mock_hand, results):
            cv2.putText(image, "HAND NOT DETECTED: Emergency Pause", (10, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            gesture = "Paused"
            return image, results, gesture, rom, landmarks

        if results.multi_hand_landmarks:
            # We only track the first hand for now
            hand_landmarks = results.multi_hand_landmarks[0]
            landmarks = hand_landmarks.landmark
            
            # Draw landmarks
            self.mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
                self.mp_drawing_styles.get_default_hand_landmarks_style(),
                self.mp_drawing_styles.get_default_hand_connections_style()
            )
            
            # Get gesture data
            gesture, rom = self.detect_gesture_and_rom(landmarks)
            
            if self.accuracy_filter:
                # 1. Filter angle
                # We send the ROM angle into the filter to smooth it out
                filtered = self.accuracy_filter.filter_angles([rom, rom, rom, rom])
                smooth_rom = filtered[0]
                
                # 2. Medical Correctness Engine 
                event = self.sensei.evaluate(smooth_rom)
                status_color = (0, 255, 0)
                if event == "bend_further":
                    status_color = (0, 0, 255)
                    
                cv2.putText(image, f"Sensei: {event}", (10, 130), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2, cv2.LINE_AA)
                
                rom = smooth_rom # Use smoothed rom for rendering
                
        else:
            # Logic to pause/show "Hand Not Found" 
            cv2.putText(image, "HAND NOT FOUND: Paused", (10, 150), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            gesture = "Paused"

        # 3. Machine Learning Prediction Overlay
        if hasattr(self, 'ml_prediction_text'):
            cv2.putText(image, self.ml_prediction_text, (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 200, 0), 2, cv2.LINE_AA)

        return image, results, gesture, rom, landmarks

    def run(self):
        """
        Main loop to capture frames and process MediaPipe results.
        """
        print("Starting Hand Rehab Assistant... Press 'q' to exit.")
        
        while self.cap.isOpened():
            image, results, gesture, rom, landmarks = self.get_processed_frame()
            
            if image is None:
                break

            # Display info on the CV2 window if running standalone
            if landmarks:
                cv2.putText(image, f"Gesture: {gesture}", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                
                cv2.putText(image, f"Index PIP Angle: {int(rom)} deg", (10, 90), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            cv2.imshow('Hand Rehab Assistant', image)
            
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = HandRehabAssistant()
    app.run()
