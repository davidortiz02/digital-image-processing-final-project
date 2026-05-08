import argparse
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import torch
from pathlib import Path
from PIL import Image

from colorizers import *

DEOLDIFY_PATH = Path('./DeOldify')
sys.path.insert(0, str(DEOLDIFY_PATH))

from deoldify import device as deoldify_device
from deoldify.device_id import DeviceId
from deoldify.visualize import get_image_colorizer

parser = argparse.ArgumentParser()
<<<<<<< HEAD
parser.add_argument('-i', '--img_path', type=str, default='imgs/doctorwhogrey.png') # CHANGE IMAGE HERE
=======
parser.add_argument('-i', '--img_path', type=str, default='imgs/union.jpg') # CHANGE IMAGE HERE
>>>>>>> 0329b854f20728738d86b6c4219226ff92491c74
parser.add_argument('--use_gpu', action='store_true', help='whether to use GPU')
parser.add_argument('-o', '--save_prefix', type=str, default='saved', help='prefix for all saved output images')
parser.add_argument('--render_factor', type=int, default=35, help='DeOldify render factor (7-45). Lower=more vibrant, higher=more detail')
opt = parser.parse_args()

if opt.use_gpu:
    deoldify_device.set(device=DeviceId.GPU0)
else:
    deoldify_device.set(device=DeviceId.CPU)

colorizer_eccv16 = eccv16(pretrained=True).eval()
colorizer_siggraph17 = siggraph17(pretrained=True).eval()
if opt.use_gpu:
    colorizer_eccv16.cuda()
    colorizer_siggraph17.cuda()

<<<<<<< HEAD
print("Loading DeOldify:")
colorizer_deoldify = get_image_colorizer(root_folder=DEOLDIFY_PATH, artistic=True)

print("Running ECCV16 and SIGGRAPH17:")
img = load_img(opt.img_path)
(tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(512, 512))
=======
colorizer_deoldify = get_image_colorizer(root_folder=DEOLDIFY_PATH, artistic=True)

img = load_img(opt.img_path)
(tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(256,256))
>>>>>>> 0329b854f20728738d86b6c4219226ff92491c74
if opt.use_gpu:
    tens_l_rs = tens_l_rs.cuda()

img_bw = postprocess_tens(tens_l_orig, torch.cat((0 * tens_l_orig, 0 * tens_l_orig), dim=1))

with torch.no_grad():
    out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
    out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())

plt.imsave('%s_eccv16.png' % opt.save_prefix, out_img_eccv16)
plt.imsave('%s_siggraph17.png' % opt.save_prefix, out_img_siggraph17)

<<<<<<< HEAD
print(f"Running DeOldify:")
=======
>>>>>>> 0329b854f20728738d86b6c4219226ff92491c74
deoldify_out_path = '%s_deoldify.png' % opt.save_prefix

out_img_deoldify = colorizer_deoldify.get_transformed_image(
    path=Path(opt.img_path),
    render_factor=opt.render_factor,
    watermarked=False,
    post_process=True,
)

out_img_deoldify = np.array(out_img_deoldify)

plt.imsave(deoldify_out_path, out_img_deoldify)

fig = plt.figure(figsize=(14, 8))
gs = gridspec.GridSpec(2, 4, figure=fig)

ax1 = fig.add_subplot(gs[0, :2])
ax1.imshow(img)
<<<<<<< HEAD
ax1.set_title('Original', fontsize=11)
=======
ax1.set_title('Original')
>>>>>>> 0329b854f20728738d86b6c4219226ff92491c74
ax1.axis('off')

ax2 = fig.add_subplot(gs[0, 2:])
ax2.imshow(img_bw)
<<<<<<< HEAD
ax2.set_title('Input', fontsize=11)
=======
ax2.set_title('Input')
>>>>>>> 0329b854f20728738d86b6c4219226ff92491c74
ax2.axis('off')

ax3 = fig.add_subplot(gs[1, 0])
ax3.imshow(out_img_eccv16)
<<<<<<< HEAD
ax3.set_title('Output (ECCV 16)', fontsize=11)
=======
ax3.set_title('Output (ECCV 16)')
>>>>>>> 0329b854f20728738d86b6c4219226ff92491c74
ax3.axis('off')

ax4 = fig.add_subplot(gs[1, 1])
ax4.imshow(out_img_siggraph17)
<<<<<<< HEAD
ax4.set_title('Output (SIGGRAPH 17)', fontsize=11)
=======
ax4.set_title('Output (SIGGRAPH 17)')
>>>>>>> 0329b854f20728738d86b6c4219226ff92491c74
ax4.axis('off')

ax5 = fig.add_subplot(gs[1, 2:])
ax5.imshow(out_img_deoldify)
<<<<<<< HEAD
ax5.set_title(f'Output (DeOldify)', fontsize=11)
ax5.axis('off')

plt.suptitle('Colorization Comparison', fontsize=13, fontweight='bold')
=======
ax5.set_title(f'Output (DeOldify)')
ax5.axis('off')

plt.suptitle('Colorization Comparison')
>>>>>>> 0329b854f20728738d86b6c4219226ff92491c74
plt.tight_layout()
plt.savefig('%s_comparison.png' % opt.save_prefix, dpi=150, bbox_inches='tight')
plt.show()