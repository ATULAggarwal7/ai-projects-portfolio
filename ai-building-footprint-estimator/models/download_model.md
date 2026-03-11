## Model Download

This project uses the **Segment Anything Model (SAM)** for automatic building segmentation.

The pretrained model is too large to store in this repository, so it must be downloaded separately.

Download the model from the official source:

https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth

After downloading, place the file inside the **models/** directory.

### Expected Folder Structure

```
autobuilding
│
├── models
│   └── sam_vit_h.pth
│
├── src
├── app.py
└── requirements.txt
```

If the **models** folder does not exist, create it manually before placing the model file.
