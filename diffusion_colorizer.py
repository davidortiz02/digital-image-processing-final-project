import torch
import torch.nn as nn
import torchvision.transforms as T

from diffusers import UNet2DConditionModel, DDPMScheduler

class DiffusionColorizer(nn.Module):
    def __init__(self, device="cuda"):
        super().__init__()

        self.device = device

        # ---- UNet (core diffusion model) ----
        self.unet = UNet2DConditionModel.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            subfolder="unet"
        ).to(device)

        # ---- diffusion scheduler ----
        self.scheduler = DDPMScheduler.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            subfolder="scheduler"
        )

        # simple conditioning projection (L -> latent condition)
        self.condition_encoder = nn.Conv2d(1, 4, kernel_size=1)

    def forward(self, L):
        """
        L: grayscale image tensor [1,1,H,W]
        returns: predicted ab channels
        """

        L = L.to(self.device)

        # ---- condition encoding ----
        cond = self.condition_encoder(L)

        # ---- initialize random noise ----
        noise = torch.randn_like(cond)

        self.scheduler.set_timesteps(20)

        x = noise

        # ---- diffusion sampling loop ----
        for t in self.scheduler.timesteps:
            model_input = torch.cat([x, cond], dim=1)

            noise_pred = self.unet(
                model_input,
                t
            ).sample

            x = self.scheduler.step(noise_pred, t, x).prev_sample

        # ---- map latent → ab channels ----
        ab = torch.tanh(x[:, :2, :, :])  # take 2 channels as color
        return ab