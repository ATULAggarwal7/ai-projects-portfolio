import cv2
import numpy as np
import matplotlib.pyplot as plt

def run_calibration(image_bgr):
    """
    Matplotlib window: user clicks two points of known real-world distance (meters).
    Returns: pixels_per_meter (float)
    """
    clicked_points = []

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

    img_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    fig, ax = plt.subplots()
    ax.imshow(img_rgb)
    ax.set_title("Calibration: Click both ends of a known-length line")
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    if len(clicked_points) != 2:
        raise RuntimeError("Calibration failed: need exactly two clicks.")

    pt1, pt2 = clicked_points
    pixel_distance = np.linalg.norm(np.array(pt1) - np.array(pt2))
    print(f"Distance between selected points (pixels): {pixel_distance:.2f}")
    real_distance = float(input(" Enter real-world distance (in meters): "))
    ppm = pixel_distance / real_distance
    print(f" Pixels per meter = {ppm:.4f}")
    return ppm
