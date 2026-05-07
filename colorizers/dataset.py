import os
import torch
import numpy as np

from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms
from skimage.color import rgb2lab

class ColorizationDataset(Dataset):

    def __init__(self, image_dir):

        self.image_dir = image_dir

        self.image_paths = [
            os.path.join(image_dir, file)
            for file in os.listdir(image_dir)
            if file.endswith(('.jpg', '.png', '.jpeg'))
        ]

        self.transform = transforms.Compose([
            transforms.Resize((256,256))
        ])

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):

        img_path = self.image_paths[idx]

        img = Image.open(img_path).convert('RGB')

        img = self.transform(img)

        img = np.array(img)

        # RGB -> LAB
        lab = rgb2lab(img).astype(np.float32)

        # split channels
        L = lab[:,:,0]
        ab = lab[:,:,1:]

        # normalize
        L = L / 50.0 - 1.0
        ab = ab / 110.0

        # convert to tensors
        L = torch.tensor(L).unsqueeze(0)

        ab = torch.tensor(ab).permute(2,0,1)

        return L, ab