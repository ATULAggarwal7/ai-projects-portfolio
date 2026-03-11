import cv2
import matplotlib.pyplot as plt
import numpy as np

clicked_points = []

def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        x, y = int(event.xdata), int(event.ydata)
        clicked_points.append((x, y))
        print(f"Point selected: ({x}, {y})")
        
        plt.plot(x, y, 'ro')  # mark red dot
        if len(clicked_points) == 2:
            plt.plot([clicked_points[0][0], clicked_points[1][0]],
                     [clicked_points[0][1], clicked_points[1][1]], 'b-')
        plt.draw()

# Load image
image_path = "data/jammu_009.jpg"
img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)

# Show image using matplotlib
fig, ax = plt.subplots()
ax.imshow(img)
ax.set_title("Click on both ends of the scale line")
cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()

# After click
if len(clicked_points) == 2:
    pt1, pt2 = clicked_points
    pixel_distance = np.linalg.norm(np.array(pt1) - np.array(pt2))
    print(f"\nDistance between selected points (in pixels): {pixel_distance:.2f}")

    real_distance = float(input("Enter real-world distance of the selected line (in meters): "))
    pixels_per_meter = pixel_distance / real_distance
    print(f"Pixels per meter = {pixels_per_meter:.4f}")

    with open("pixels_per_meter.txt", "w") as f:
        f.write(str(pixels_per_meter))
    print("\n Calibration saved to 'pixels_per_meter.txt'")
else:
    print(" Please click exactly two points.")
