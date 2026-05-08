
import argparse
import matplotlib.pyplot as plt

from colorizers import *

parser = argparse.ArgumentParser()
parser.add_argument('-i','--img_path', type=str, default='imgs/union.jpg')
parser.add_argument('--use_gpu', action='store_true', help='whether to use GPU')
parser.add_argument('-o','--save_prefix', type=str, default='saved', help='will save into this file with {eccv16.png, siggraph17.png} suffixes')
opt = parser.parse_args()

# load colorizers
colorizer_eccv16 = eccv16(pretrained=True).eval()
colorizer_siggraph17 = siggraph17(pretrained=True).eval()
colorizer_resnet50 = resnet50_colorizer(pretrained=True).eval()
if(opt.use_gpu):
	colorizer_eccv16.cuda()
	colorizer_siggraph17.cuda()
	colorizer_resnet50.cuda()

# default size to process images is 256x256
# grab L channel in both original ("orig") and resized ("rs") resolutions
img = load_img(opt.img_path)
(tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(256,256))
if(opt.use_gpu):
	tens_l_rs = tens_l_rs.cuda()

tens_l_input = tens_l_rs / 50.0 - 1.0  # match training normalization
out_ab = colorizer_resnet50(tens_l_input).cpu() * 110.0  # denormalize output

# colorizer outputs 256x256 ab map
# resize and concatenate to original L channel
img_bw = postprocess_tens(tens_l_orig, torch.cat((0*tens_l_orig,0*tens_l_orig),dim=1))
out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())
out_img_resnet50 = postprocess_tens(tens_l_orig, out_ab)

plt.imsave('%s_eccv16.png'%opt.save_prefix, out_img_eccv16)
plt.imsave('%s_siggraph17.png'%opt.save_prefix, out_img_siggraph17)
plt.imsave('%s_resnet50.png'%opt.save_prefix, out_img_resnet50)

plt.figure(figsize=(12,8))
plt.subplot(2,3,1)
plt.imshow(img)
plt.title('Original')
plt.axis('off')

plt.subplot(2,3,2)
plt.imshow(img_bw)
plt.title('Input')
plt.axis('off')

plt.subplot(2,3,3)
plt.imshow(out_img_eccv16)
plt.title('Output (ECCV 16)')
plt.axis('off')

plt.subplot(2,3,4)
plt.imshow(out_img_siggraph17)
plt.title('Output (SIGGRAPH 17)')
plt.axis('off')
#plt.tight_layout()
#plt.savefig('%s_comparison_original.png' % opt.save_prefix, dpi=150, bbox_inches='tight')

plt.subplot(2,3,5)
plt.imshow(out_img_resnet50)
plt.title('Output (RESNET 50)')
plt.axis('off')
plt.tight_layout()
plt.savefig('%s_comparison_original.png' % opt.save_prefix, dpi=150, bbox_inches='tight')
plt.show()
