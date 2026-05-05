import torch
import torch.nn as nn
import torchvision.models as models

class ResNetColorizer(nn.Module):
    def __init__(self):
        super().__init__()

        resnet = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)

        self.encoder = nn.Sequential(*list(resnet.children())[:-2])

        self.decoder = nn.Sequential(
            nn.Conv2d(2048, 512, 3, padding=1),
            nn.ReLU(),

            nn.Upsample(scale_factor=2),

            nn.Conv2d(512, 256, 3, padding=1),
            nn.ReLU(),

            nn.Upsample(scale_factor=2),

            nn.Conv2d(256, 128, 3, padding=1),
            nn.ReLU(),

            nn.Conv2d(128, 2, 1),
            nn.Tanh()
        )

    def forward(self, L):
        x = L.repeat(1, 3, 1, 1)
        x = self.encoder(x)
        return self.decoder(x)