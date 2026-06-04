import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_flowchart():
    # Setup styling parameters
    # Cyber-medical aesthetic palette
    bg_color = "#0B0E1A"       # Dark medical blue
    box_color = "#152549"      # Panel background
    border_color = "#00C8FF"   # Neon cyan
    text_color = "#F0F0F0"     # Off-white text
    arrow_color = "#32FF96"    # Cyber success green
    warning_color = "#FF9600"  # Accent orange

    fig, ax = plt.subplots(figsize=(16, 22), facecolor=bg_color)
    ax.set_facecolor(bg_color)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 24)
    ax.axis("off")

    # Helper function to draw a process box (rounded rectangle)
    def draw_box(x, y, w, h, text, is_decision=False, is_warning=False):
        bcolor = border_color
        if is_warning:
            bcolor = warning_color
        
        if is_decision:
            # Draw diamond shape for decisions
            diamond = patches.Polygon([
                (x + w/2, y),        # Bottom
                (x + w, y + h/2),    # Right
                (x + w/2, y + h),    # Top
                (x, y + h/2)         # Left
            ], closed=True, facecolor=box_color, edgecolor=bcolor, linewidth=2)
            ax.add_patch(diamond)
        else:
            # Draw rounded rectangle for standard steps
            rect = patches.FancyBboxPatch(
                (x + 0.05, y + 0.05), w - 0.1, h - 0.1,
                boxstyle="round,pad=0.1",
                facecolor=box_color,
                edgecolor=bcolor,
                linewidth=2
            )
            ax.add_patch(rect)
        
        # Draw text inside box
        ax.text(x + w/2, y + h/2, text, color=text_color, fontsize=11,
                ha="center", va="center", wrap=True, fontweight="bold")

    # Helper function to draw arrows
    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=arrow_color, lw=2.5, mutation_scale=20))
        if label:
            ax.text((x1 + x2)/2, (y1 + y2)/2 + 0.15, label, color=arrow_color,
                    fontsize=10, ha="center", va="bottom", fontweight="bold")

    # Draw title
    ax.text(8, 23.3, "AI HAND REHABILITATION SYSTEM\nSYSTEM ARCHITECTURE & OPERATIONAL FLOW", 
            color=border_color, fontsize=18, ha="center", va="center", fontweight="bold")

    # Column 1 (Left): System Initialization & Profiling (x = 1 to 4)
    draw_box(1.5, 21.0, 3.0, 1.0, "SYSTEM START\n(Boot & Scale UI)")
    draw_box(1.5, 19.2, 3.0, 1.0, "SQLITE DATABASE\nInitialization &\nSchema Integrity Check")
    draw_arrow(3.0, 21.0, 3.0, 20.2)
    
    draw_box(1.5, 17.4, 3.0, 1.0, "CAMERA STREAM\n& MediaPipe Hand\nEngine Startup")
    draw_arrow(3.0, 19.2, 3.0, 18.4)
    
    draw_box(1.5, 15.6, 3.0, 1.0, "PATIENT REGISTRATION\nPortal UI Screen")
    draw_arrow(3.0, 17.4, 3.0, 16.6)
    
    draw_box(1.5, 13.5, 3.0, 1.3, "PATIENT PROFILE\nSTATUS?", is_decision=True)
    draw_arrow(3.0, 15.6, 3.0, 14.8)

    # Column 2 (Middle): Calibration & Menu (x = 6.5 to 9.5)
    draw_box(6.5, 13.5, 3.0, 1.3, "2-STEP CALIBRATION\n1. Open Hand ROM\n2. Closed Fist Value", is_warning=True)
    draw_arrow(4.5, 14.15, 6.5, 14.15, label="NEW PROFILE")
    
    draw_box(6.5, 11.2, 3.0, 1.2, "LOAD CALIBRATION\nSave baseline thresholds\nto SQLite database")
    draw_arrow(8.0, 13.5, 8.0, 12.4)
    
    draw_box(1.5, 11.2, 3.0, 1.2, "LOAD ROM DATA\nQuery existing settings\nfor patient from DB")
    draw_arrow(3.0, 13.5, 3.0, 12.4)
    
    # Merge pathways into Menu
    draw_box(4.0, 9.2, 3.0, 1.0, "MAIN LEVEL MENU\n(Hover or Click Selection)")
    # Arrow from Load existing
    ax.annotate("", xy=(5.0, 10.2), xytext=(3.0, 11.2),
                arrowprops=dict(arrowstyle="->", color=arrow_color, lw=2.5, connectionstyle="angle,angleA=0,angleB=90"))
    # Arrow from Load new calibration
    ax.annotate("", xy=(6.0, 10.2), xytext=(8.0, 11.2),
                arrowprops=dict(arrowstyle="->", color=arrow_color, lw=2.5, connectionstyle="angle,angleA=0,angleB=90"))

    # Column 3 (Right): Active Gameplay & Telemetry (x = 11.5 to 14.5)
    draw_box(11.5, 9.0, 3.0, 1.2, "ACTIVE GAMEPLAY LEVEL\n(Levels 1 - 6 Selection)")
    draw_arrow(7.0, 9.7, 11.5, 9.7, label="SELECT LEVEL")

    draw_box(11.5, 7.2, 3.0, 1.1, "SAFETY GRACE LOCK\n2.0s Transition Screen\nCursor Deactivated")
    draw_arrow(13.0, 9.0, 13.0, 8.3)
    
    draw_box(11.5, 5.4, 3.0, 1.1, "LIVE CAMERA CAPTURE\n& 21 3D MediaPipe\nLandmark Extraction")
    draw_arrow(13.0, 7.2, 13.0, 6.5)

    # Column 2 (Middle - Bottom): Tracking calculations (x = 6.5 to 9.5)
    draw_box(6.5, 5.4, 3.0, 1.1, "ANTI-TREMOR FILTER\nWeighted average sliding\nwindow buffer smoothing")
    draw_arrow(11.5, 5.95, 9.5, 5.95)
    
    draw_box(6.5, 3.6, 3.0, 1.1, "DYNAMIC REACH SCALING\nScale tracking coordinate\nspace by calibration ROM")
    draw_arrow(8.0, 5.4, 8.0, 4.7)

    draw_box(1.5, 3.6, 3.0, 1.1, "BIOMETRIC CALCULATIONS\nMCP joint angles (Law of Cosines)\nFist & Pinch Recognition")
    draw_arrow(6.5, 4.15, 4.5, 4.15)

    # UI updates & Pacing loop
    draw_box(1.5, 5.4, 3.0, 1.1, "SPLIT-SCREEN RENDER\nClinical Telemetry Sidebar\nwith Neon Joint Skeleton")
    draw_arrow(3.0, 4.7, 3.0, 5.4)

    draw_box(1.5, 7.2, 3.0, 1.1, "ADAPTIVE PACING\nAdjust speed multipliers\n& target sizing in real time")
    draw_arrow(3.0, 6.5, 3.0, 7.2)
    # Loop arrow back to capture
    ax.annotate("", xy=(11.5, 6.1), xytext=(4.5, 7.75),
                arrowprops=dict(arrowstyle="->", color=arrow_color, lw=2.5, connectionstyle="angle,angleA=0,angleB=90"))

    # Completion and Reports (Bottom)
    draw_box(1.5, 1.2, 3.0, 1.3, "LEVEL COMPLETE / TIMEOUT?\n(Duration limit reached)", is_decision=True)
    draw_arrow(3.0, 3.6, 3.0, 2.5)

    draw_box(6.5, 1.2, 3.0, 1.2, "INTEGRATED NRS PAIN SCALE\n0-10 Assessment Screen\n(Hover or Click Input)")
    draw_arrow(4.5, 1.85, 6.5, 1.85, label="YES")

    draw_box(11.5, 1.2, 3.0, 1.2, "DATA WRITER & REPORT\nSave session telemetry to SQL\nExport PDF Progress Chart")
    draw_arrow(9.5, 1.85, 11.5, 1.85)

    # Return to Menu Arrow
    ax.annotate("", xy=(5.5, 9.2), xytext=(13.0, 2.4),
                arrowprops=dict(arrowstyle="->", color=arrow_color, lw=2.5, connectionstyle="angle,angleA=0,angleB=90"))
    
    # Save the output image
    plt.savefig("c:/Users/gamin/OneDrive/Desktop/major/system_flowchart.png", 
                dpi=300, facecolor=bg_color, edgecolor='none', bbox_inches='tight')
    plt.close()
    print("[SUCCESS] Flowchart generated and saved successfully at c:/Users/gamin/OneDrive/Desktop/major/system_flowchart.png")

if __name__ == "__main__":
    draw_flowchart()
