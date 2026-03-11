import cv2
import numpy as np
import torch
from segment_anything import sam_model_registry, SamPredictor

class SAMSegmenter:
    def __init__(self, checkpoint_path: str, model_type: str = "vit_h", device: str | None = None):
        self.checkpoint_path = checkpoint_path
        self.model_type = model_type
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.sam = sam_model_registry[model_type](checkpoint=checkpoint_path)
        self.sam.to(device=self.device)
        self.predictor = SamPredictor(self.sam)

    def segment_from_point(self, image_bgr: np.ndarray, point_xy: tuple[int, int]) -> np.ndarray:
        """
        Returns a uint8 mask (0/255) of the object containing the clicked point.
        """
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        self.predictor.set_image(image_rgb)

        point_coords = np.array([[point_xy[0], point_xy[1]]])
        point_labels = np.array([1], dtype=np.int32)   # 1: foreground

        masks, scores, _ = self.predictor.predict(
            point_coords=point_coords,
            point_labels=point_labels,
            multimask_output=True
        )

        # Choose the mask with highest score
        best_idx = int(np.argmax(scores))
        best_mask = masks[best_idx].astype(np.uint8) * 255  # 0/255
        return best_mask
