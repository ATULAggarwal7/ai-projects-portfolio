import argparse
import cv2
import numpy as np
import os
from src.calibration import run_calibration
from src.sam_wrapper import SAMSegmenter
from src.height_from_mask import auto_height_from_mask
from src.utils import overlay_mask, put_text, pixels_to_area_sq_m

ASSUMED_FLOOR_HEIGHT_FT = 10
ASSUMED_FLOOR_HEIGHT_M = ASSUMED_FLOOR_HEIGHT_FT * 0.3048

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image",
        default="data/jammu_022.jpg",
        help="Path to input image (default: data/jammu_022.jpg)"
    )
    parser.add_argument(
        "--sam",
        default="models/sam_vit_h.pth",
        help="Path to SAM checkpoint (default: models/sam_vit_h.pth)"
    )
    parser.add_argument("--model_type", default="vit_h", choices=["vit_h", "vit_l", "vit_b"])
    parser.add_argument("--save", action="store_true", help="Save annotated outputs to ./output")
    args = parser.parse_args()

    os.makedirs("output", exist_ok=True)

    image_bgr = cv2.imread(args.image)
    if image_bgr is None:
        raise FileNotFoundError(f"Image not found: {args.image}")

    # Step 1: Always calibrate for PPM
    ppm = run_calibration(image_bgr)  # pixels per meter

    # Load SAM
    segmenter = SAMSegmenter(args.sam, model_type=args.model_type)

    base = image_bgr.copy()
    disp = base.copy()
    last_result_img = None
    building_counter = 1  # For naming files building1, building2, ...

    print("\nInstructions:")
    print("  • Left-click on ANY building to auto-segment & auto-measure.")
    print("  • Press 'R' to reset.")
    print("  • Press 'ESC' to quit.\n")

    def on_mouse(event, x, y, flags, param):
        nonlocal disp, last_result_img, building_counter

        if event == cv2.EVENT_LBUTTONDOWN:
            disp = base.copy()

            # Segmentation
            mask = segmenter.segment_from_point(base, (x, y))
            if mask is None or mask.sum() == 0:
                print("No mask found at click.")
                return

            # Overlay mask
            disp = overlay_mask(disp, mask, color=(0, 255, 0), alpha=0.35)

            # Area
            area_m2, area_px = pixels_to_area_sq_m(mask, ppm)
            put_text(disp, f"Area: {area_m2:.2f} m^2", (20, 50), scale=1.2)

            # Height
            endpoints, measures = auto_height_from_mask(base, mask, (x, y), ppm)
            if endpoints is None or measures["vertical_m"] is None:
                put_text(disp, "Height: (auto failed, try another click)", (20, 90), scale=1.0, color=(0, 0, 255))
                last_result_img = disp.copy()
                return

            (pt_top, pt_bottom) = endpoints
            slanted_m = measures["slanted_m"]
            vertical_m = measures["vertical_m"]
            floors = measures["floors"]

            # Draw height line
            cv2.circle(disp, pt_top, 10, (0, 0, 200), -1)
            cv2.circle(disp, pt_bottom, 10, (0, 0, 200), -1)
            cv2.line(disp, pt_top, pt_bottom, (255, 0, 0), 5)

            put_text(disp, f"Height (vertical): {vertical_m:.2f} m  ~  Floors: {floors}", (20, 90), scale=1.2)
            put_text(disp, f"Line length (slanted): {slanted_m:.2f} m", (20, 130), scale=1.0)

            # Save measurements to file automatically
            file_path = os.path.join("output", f"building{building_counter}.txt")
            with open(file_path, "w") as f:
                f.write(f"Building {building_counter}\n")
                f.write(f"Area: {area_m2:.2f} m² ({area_px:.0f} px)\n")
                f.write(f"Height (vertical): {vertical_m:.2f} m\n")
                f.write(f"Height (slanted): {slanted_m:.2f} m\n")
                f.write(f"Estimated Floors: {floors}\n")
                f.write(f"Pixels-per-meter (ppm): {ppm:.4f}\n")
            print(f"Saved measurements to: {file_path}")

            # Save annotated image
            img_out_path = os.path.join("output", f"building{building_counter}_annotated.png")
            cv2.imwrite(img_out_path, disp)
            print(f"Saved annotated image to: {img_out_path}")

            building_counter += 1
            last_result_img = disp.copy()

    cv2.namedWindow("Auto Area + Height (Click building) - R=reset, ESC=exit", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Auto Area + Height (Click building) - R=reset, ESC=exit", base.shape[1], base.shape[0])
    cv2.setMouseCallback("Auto Area + Height (Click building) - R=reset, ESC=exit", on_mouse)

    while True:
        cv2.imshow("Auto Area + Height (Click building) - R=reset, ESC=exit", disp)
        k = cv2.waitKey(16) & 0xFF
        if k == 27:  # ESC
            break
        elif k == ord('r'):
            disp = base.copy()
            last_result_img = None

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
