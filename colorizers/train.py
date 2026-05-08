import torch
import torch.nn as nn

from torch.utils.data import DataLoader

from dataset import ColorizationDataset
from resnet50 import *

device = torch.device(
    'cuda' if torch.cuda.is_available() else 'cpu'
)

# dataset
dataset = ColorizationDataset(
    './data/test_color'
)

train_loader = DataLoader(
    dataset,
    batch_size=4,
    shuffle=True
)

# model
model = resnet50_colorizer(
    pretrained=False
).to(device)

# loss
criterion = nn.L1Loss()

# optimizer
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=1e-4
)

num_epochs = 10

for epoch in range(num_epochs):

    model.train()

    running_loss = 0.0

    for L, ab in train_loader:

        L = L.to(device)
        ab = ab.to(device)

        # forward
        pred_ab = model(L)

        # loss
        loss = criterion(pred_ab, ab)

        # backward
        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    print(
        f"Epoch [{epoch+1}/{num_epochs}] "
        f"Loss: {running_loss/len(train_loader):.4f}"
    )

# save weights
torch.save(
    model.state_dict(),
    'resnet50_colorizer.pth'
)

print("Training complete.")