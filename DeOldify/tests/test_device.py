import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add parent directory to path to import deoldify
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from deoldify.device_id import DeviceId
from deoldify._device import _Device


class TestDevice(unittest.TestCase):
    def setUp(self):
        self.device_manager = _Device()

    @patch("torch.cuda.is_available")
    def test_init_device_cpu(self, mock_cuda_available):
        mock_cuda_available.return_value = False
        # Mock xpu availability if it exists in the environment
        with patch("torch.xpu.is_available", create=True) as mock_xpu_available:
            mock_xpu_available.return_value = False
            self.device_manager._init_device()
            self.assertEqual(self.device_manager._backend, "cpu")

    @patch("torch.cuda.is_available")
    def test_init_device_cuda(self, mock_cuda_available):
        mock_cuda_available.return_value = True
        # Ensure xpu is false so we fall through to cuda
        with patch("torch.xpu.is_available", create=True) as mock_xpu_available:
            mock_xpu_available.return_value = False
            self.device_manager._init_device()
            self.assertEqual(self.device_manager._backend, "cuda")

    def test_set_cpu(self):
        self.device_manager.set(DeviceId.CPU)
        self.assertEqual(self.device_manager.current(), DeviceId.CPU)
        self.assertEqual(os.environ.get("CUDA_VISIBLE_DEVICES"), "")

    @patch("torch.cuda.is_available")
    def test_set_gpu_cuda(self, mock_cuda_available):
        mock_cuda_available.return_value = True
        with patch("torch.xpu.is_available", create=True) as mock_xpu_available:
            mock_xpu_available.return_value = False
            self.device_manager._init_device()

            self.device_manager.set(DeviceId.GPU0)
            self.assertEqual(self.device_manager.current(), DeviceId.GPU0)
            self.assertEqual(os.environ.get("CUDA_VISIBLE_DEVICES"), "0")


if __name__ == "__main__":
    unittest.main()
