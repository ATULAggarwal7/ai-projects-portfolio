import cv2
import numpy as np

def overlay_mask(image_bgr, mask_uint8, color=(0, 255, 0), alpha=0.35):
    """Returns a copy with a translucent colored overlay where mask==255."""
    overlay = image_bgr.copy()
    color_img = np.zeros_like(image_bgr)
    color_img[:, :] = color
    mask_bool = mask_uint8.astype(bool)
    overlay[mask_bool] = cv2.addWeighted(image_bgr, 1 - alpha, color_img, alpha, 0)[mask_bool]
    return overlay

def put_text(img, text, org=(20, 50), scale=1.2, color=(255, 255, 255), thickness=3):
    cv2.putText(img, text, org, cv2.FONT_HERSHEY_SIMPLEX, scale, color, thickness, cv2.LINE_AA)

def pixels_to_area_sq_m(mask_uint8, ppm):
    """mask_uint8=0/255; area in m^2."""
    pix = int(np.count_nonzero(mask_uint8))
    return pix / (ppm ** 2), pix
