import torch
import torch.nn as nn
import torchvision.models as models
from torchvision.models import resnet50, ResNet50_Weights
from skimage.color import rgb2lab

class ResNetColorizer(nn.Module):
    def __init__(self):
        super().__init__()

        resnet = resnet50(weights=ResNet50_Weights.DEFAULT) #using a resnet model as a more modern architecture

        resnet.conv1 = nn.Conv2d(
            1, #since input images are BW, use only one channel instead of three for the first layer
            64,
            kernel_size=7,
            stride=2,
            padding=3,
            bias=False
            )

        self.encoder = nn.Sequential(
            resnet.conv1, #the first convolutional layer that's been modified to handle BW images
            resnet.bn1,
            resnet.relu,
            resnet.maxpool,

            resnet.layer1,
            resnet.layer2,
            resnet.layer3,
            resnet.layer4
        )

        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(2048, 1024, 4, 2, 1),
            nn.ReLU(True),

            nn.ConvTranspose2d(1024, 512, 4, 2, 1),
            nn.ReLU(True),

            nn.ConvTranspose2d(512, 256, 4, 2, 1),
            nn.ReLU(True),

            nn.ConvTranspose2d(256, 128, 4, 2, 1),
            nn.ReLU(True),

            nn.ConvTranspose2d(128, 2, 4, 2, 1),
            nn.Tanh()
        )

    def forward(self, x):
        features = self.encoder(x)
        out = self.decoder(features)
        #print(out.shape)

        return out
    
def resnet50_colorizer(pretrained=False):
    model = ResNetColorizer()
    if pretrained:
        model.load_state_dict(torch.load('models/resnet50_colorizer.pth')) #load the pretrained model, easier for us instead of having to train a model ourselves, though the option is there

    return model