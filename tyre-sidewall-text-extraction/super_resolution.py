import cv2
import os
import numpy as np
from realesrgan import RealESRGANer
from basicsr.archs.rrdbnet_arch import RRDBNet

def enhance_image(image_path):
    print("[INFO] Enhancing image using Real-ESRGAN...")

    # Load image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Create model
    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64,
                    num_block=23, num_grow_ch=32, scale=2)

    # Download model manually once and put in weights folder
    model_path = os.path.join("weights", "RealESRGAN_x2plus.pth")

    # Create upsampler
    upsampler = RealESRGANer(
        scale=2,
        model_path=model_path,
        model=model,
        tile=0,
        tile_pad=10,
        pre_pad=0,
        half=False
    )

    # Enhance
    sr_img, _ = upsampler.enhance(img, outscale=2)
    return sr_img
