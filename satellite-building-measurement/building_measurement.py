import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

# ----------- CONFIG -----------
IMAGE_PATH = "data/vasundhara_zoom.jpg"
clicked_points = []
drawing = False
points = []

ASSUMED_FLOOR_HEIGHT_FT = 10
ASSUMED_FLOOR_HEIGHT_M = ASSUMED_FLOOR_HEIGHT_FT * 0.3048

# ----------- STEP 1: CALIBRATION USING MATPLOTLIB -----------
def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        x, y = int(event.xdata), int(event.ydata)
        clicked_points.append((x, y))
        print(f"Point selected: ({x}, {y})")
        plt.plot(x, y, 'ro')
        if len(clicked_points) == 2:
            plt.plot([clicked_points[0][0], clicked_points[1][0]],
                     [clicked_points[0][1], clicked_points[1][1]], 'b-')
        plt.draw()

# Load image (original size)
original_img = cv2.imread(IMAGE_PATH)
if original_img is None:
    raise FileNotFoundError("Image not found. Check IMAGE_PATH.")
img_rgb = cv2.cvtColor(original_img.copy(), cv2.COLOR_BGR2RGB)

# Show for calibration
fig, ax = plt.subplots()
ax.imshow(img_rgb)
ax.set_title("Step 1: Click both ends of the known-length line")
cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

if len(clicked_points) != 2:
    print(" Error: You must select exactly two points.")
    exit()

pt1, pt2 = clicked_points
pixel_distance = np.linalg.norm(np.array(pt1) - np.array(pt2))
print(f"\n Distance between selected points (pixels): {pixel_distance:.2f}")

real_distance = float(input(" Enter real-world distance (in meters): "))
PIXELS_PER_METER = pixel_distance / real_distance
print(f" Pixels per meter = {PIXELS_PER_METER:.4f}")

# ----------- STEP 2: FREEHAND AREA DRAWING + HEIGHT MEASUREMENT -----------
def calculate_area(contour, ppm):
    pixel_area = cv2.contourArea(contour)
    meter_area = pixel_area / (ppm ** 2)
    return pixel_area, meter_area

# State variables
height_points = []
height_result_text = ""
height_mode = False
height_taken = False  # prevents multiple heights in same cycle

def reset_state():
    """Resets everything except calibration."""
    global drawing, points, height_points, height_result_text, height_mode, height_taken, original_img_copy
    drawing = False
    points.clear()
    height_points.clear()
    height_result_text = ""
    height_mode = False
    height_taken = False
    original_img_copy = original_img.copy()
    print("\n--- Reset done. Draw a new area ---")

def mouse_callback(event, x, y, flags, param):
    global drawing, points, original_img_copy, height_mode, height_points, height_result_text, height_taken

    if not height_mode:
        # ---- AREA DRAW MODE ----
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            points.clear()
            points.append((x, y))
            original_img_copy = original_img.copy()

        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            points.append((x, y))
            preview = original_img.copy()
            cv2.polylines(preview, [np.array(points)], isClosed=False, color=(0, 255, 0), thickness=5)
            original_img_copy = preview

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            points.append((x, y))
            if len(points) > 2:
                annotated = original_img.copy()
                cv2.polylines(annotated, [np.array(points)], isClosed=True, color=(0, 255, 0), thickness=5)
                contour = np.array(points).reshape((-1, 1, 2)).astype(np.int32)
                px_area, m_area = calculate_area(contour, PIXELS_PER_METER)
                print(f"Area: {px_area:.2f} px²  |  {m_area:.2f} m²")
                cv2.putText(annotated, f"{m_area:.2f} m^2", points[0],
                            cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), 5)
                original_img_copy = annotated
                height_mode = True
                height_points.clear()
                height_result_text = ""
                print("\nNow click base of building → click roof to estimate height.")
    else:
        # ---- HEIGHT MODE ----
        disp = original_img_copy.copy()

        # On clicks
        if event == cv2.EVENT_LBUTTONDOWN and not height_taken:
            if len(height_points) == 0:
                height_points = [(x, y)]
                cv2.circle(disp, (x, y), 10, (0, 0, 200), -1)  # Large dark red dot
                original_img_copy = disp
            elif len(height_points) == 1:
                height_points.append((x, y))
                (x1, y1), (x2, y2) = height_points
                pixel_len = math.hypot(x2 - x1, y2 - y1)
                meters = pixel_len / PIXELS_PER_METER
                est_floors = max(1, int(round(meters / ASSUMED_FLOOR_HEIGHT_M)))
                height_result_text = f"{meters:.2f} m ≈ {est_floors} floors"
                print(f"Height line: {pixel_len:.1f}px  ~  {meters:.2f} m  ~  ≈ {est_floors} floors")

                # Final permanent line + dots
                cv2.line(disp, height_points[0], height_points[1], (255, 0, 0), 5)  # Blue line
                cv2.circle(disp, height_points[0], 10, (0, 0, 200), -1)  # Dark red
                cv2.circle(disp, height_points[1], 10, (0, 0, 200), -1)  # Dark red

                cv2.putText(disp, height_result_text, (min(x1, x2), min(y1, y2) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)
                original_img_copy = disp
                height_taken = True

# Init
original_img_copy = original_img.copy()
cv2.namedWindow('Draw Area + Height - Press ESC to Exit', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Draw Area + Height - Press ESC to Exit', original_img.shape[1], original_img.shape[0])
cv2.setMouseCallback('Draw Area + Height - Press ESC to Exit', mouse_callback)

print("\nStep 2: Draw a closed area using the mouse (hold + drag + release)")
print("Press 'R' to reset and start again.")

while True:
    cv2.imshow('Draw Area + Height - Press ESC to Exit', original_img_copy)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == ord('r'):
        reset_state()

cv2.destroyAllWindows()
