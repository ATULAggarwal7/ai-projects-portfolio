import torch
import torchvision.transforms as T
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ---- CONFIG ----
MODEL_PATH = 'segmentation_model.pth'
IMAGE_PATH = 'data/jammu_009.jpg'  # Change as needed
NUM_CLASSES = 17

# ---- CLASS DEFINITIONS ----
class_names = [
    "background", "building", "wood_area", "water", "road", "agriculture", "grass", "railway",
    "bareland", "river", "manmade", "mountain", "airport", "bridge", "parking_lot", "stadium", "port"
]

label_colors = np.array([
    [0, 0, 0],         # 0 background
    [128, 0, 0],       # 1 building
    [0, 128, 0],       # 2 wood_area
    [128, 128, 0],     # 3 water
    [0, 0, 128],       # 4 road
    [128, 0, 128],     # 5 agriculture
    [0, 128, 128],     # 6 grass
    [128, 128, 128],   # 7 railway
    [64, 0, 0],        # 8 bareland
    [192, 0, 0],       # 9 river
    [64, 128, 0],      # 10 manmade
    [192, 128, 0],     # 11 mountain
    [64, 0, 128],      # 12 airport
    [192, 0, 128],     # 13 bridge
    [64, 128, 128],    # 14 parking_lot
    [192, 128, 128],   # 15 stadium
    [0, 64, 0]         # 16 port
], dtype=np.uint8)

# ---- 1. Load Model ----
model = torch.hub.load('pytorch/vision:v0.13.1', 'fcn_resnet50', weights=None)
model.classifier[4] = torch.nn.Conv2d(512, NUM_CLASSES, kernel_size=1)
model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
model.eval()

# ---- 2. Preprocess Image ----
transform = T.Compose([
    T.Resize((512, 512)),
    T.ToTensor(),
])

original_image = Image.open(IMAGE_PATH).convert("RGB")
input_tensor = transform(original_image).unsqueeze(0)

# ---- 3. Run Inference ----
with torch.no_grad():
    output = model(input_tensor)['out']
pred = torch.argmax(output.squeeze(), dim=0).cpu().numpy()

# ---- 4. Decode Segmentation ----
def decode_segmap(mask):
    return label_colors[mask]

colored_mask = decode_segmap(pred)

# Resize to original image size
colored_mask = cv2.resize(colored_mask, original_image.size, interpolation=cv2.INTER_NEAREST)

# Overlay
overlay = cv2.addWeighted(np.array(original_image), 0.6, colored_mask, 0.4, 0)

# ---- 5. Display ----
plt.figure(figsize=(15, 5))

plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(original_image)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Segmented Overlay")
plt.imshow(overlay)
plt.axis('off')

plt.tight_layout()
plt.show()

# ---- 6. Show Class Legend ----
legend_patches = [
    mpatches.Patch(color=np.array(color)/255.0, label=class_name)
    for class_name, color in zip(class_names, label_colors)
]

plt.figure(figsize=(12, 3))
plt.legend(handles=legend_patches, loc='center', ncol=4, frameon=False)
plt.axis('off')
plt.title("Class Color Legend")
plt.tight_layout()
plt.show()

# ---- 7. Save Outputs ----
cv2.imwrite('segmented_overlay.png', cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
cv2.imwrite('colored_mask.png', cv2.cvtColor(colored_mask, cv2.COLOR_RGB2BGR))
cv2.imwrite('raw_mask.png', pred.astype(np.uint8))  # grayscale labels

# ---- 8. Save per-class binary masks ----
for i in range(NUM_CLASSES):
    binary_mask = (pred == i).astype(np.uint8) * 255
    cv2.imwrite(f'class_{i}_{class_names[i]}.png', binary_mask)
    