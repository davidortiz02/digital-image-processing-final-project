import unittest
import torch
import torch.nn as nn
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deoldify.fastai_compat import (
    conv_layer,
    NormType,
    relu,
    res_block,
    MergeLayer,
    SequentialEx,
)


class TestFastAICompat(unittest.TestCase):
    def test_conv_layer(self):
        # Test basic convolution layer creation
        l = conv_layer(3, 64, ks=3, stride=1)
        self.assertIsInstance(l, nn.Sequential)
        # Expect Conv2d, ReLU, BatchNorm2d
        self.assertEqual(len(l), 3)
        self.IsInstance(l[0], nn.Conv2d)

    def test_relu(self):
        r = relu(leaky=0.1)
        self.IsInstance(r, nn.LeakyReLU)
        self.assertEqual(r.negative_slope, 0.1)

    def test_merge_layer(self):
        m = MergeLayer(dense=False)
        x = torch.randn(1, 10)
        x.orig = torch.randn(1, 10)
        out = m(x)
        self.assertEqual(out.shape, (1, 10))  # Added

        m_dense = MergeLayer(dense=True)
        out_dense = m_dense(x)
        self.assertEqual(out_dense.shape, (1, 20))  # Concatenated

    def test_sequential_ex(self):
        # Test that SequentialEx handles .orig attribute
        l1 = nn.Identity()
        l2 = nn.Identity()
        seq = SequentialEx(l1, l2)

        x = torch.randn(1, 10)
        out = seq(x)
        self.assertEqual(out.shape, x.shape)

    def IsInstance(self, obj, cls):
        self.assertTrue(isinstance(obj, cls))


if __name__ == "__main__":
    unittest.main()
