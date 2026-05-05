import torch
import torch.nn as nn
import torchvision.models as models
from skimage import color

class ResNetColorizer(nn.Module):
    def __init__(self, pretrained=True):
        super().__init__()

        # ---- ResNet Backbone (Encoder) ----
        resnet = models.resnet50(pretrained=pretrained)

        # remove classification head
        self.encoder = nn.Sequential(*list(resnet.children())[:-2])

        # ---- Decoder (upsample to ab channels) ----
        self.decoder = nn.Sequential(
            nn.Conv2d(2048, 1024, 3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(1024, 512, 3, padding=1),
            nn.ReLU(inplace=True),

            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),

            nn.Conv2d(512, 256, 3, padding=1),
            nn.ReLU(inplace=True),

            nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),

            nn.Conv2d(256, 128, 3, padding=1),
            nn.ReLU(inplace=True),

            nn.Conv2d(128, 2, 1),  # ab output
            nn.Tanh()
        )

    def forward(self, L):
        # L: grayscale input (1 channel)
        x = self.encoder(L)
        ab = self.decoder(x)
        return ab