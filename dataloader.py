from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import numpy as np
import glob
import torchvision.transforms as transforms
import cv2
from PIL import Image

class FaceDataset(Dataset):
    def __init__(self, root, transforms_=None, img_size=128, mask_size=64, method="train"):
        self.transform = transforms.Compose(transforms_)
        self.img_size = img_size
        self.mask_size = mask_size
        self.mode = method
        self.root = root
        self.files = sorted(glob.glob("%s/*.png" % root))
        self.files = self.files[:-4000] if self.mode == "train" else self.files[-4000:]

        self.random_ff_setting = {'img_shape':[224,224],'mv':5, 'ma':4.0, 'ml':40, 'mbw':10}


    def apply_random_mask(self, img):
        """Randomly masks image"""
        mask = self.get_mask(self.random_ff_setting)
        masked_img = img.copy()
        masked_img[mask] = 1

        return masked_img, mask


    def __getitem__(self, index):
        img = Image.open(self.files[index % len(self.files)])
        img = self.transform(img)
        masked_img, aux = self.apply_random_mask(img)
        return img, masked_img, aux

    def __len__(self):
        return len(self.files)

    def get_mask(self, config):
        """Generate a random free form mask with configuration.

        Args:
            config: Config should have configuration including IMG_SHAPES,
                VERTICAL_MARGIN, HEIGHT, HORIZONTAL_MARGIN, WIDTH.

        Returns:
            tuple: (top, left, height, width)
        """

        h, w = config['img_shape']
        mask = np.zeros((h, w))
        num_v = 12 + np.random.randint(config['mv'])

        for i in range(num_v):
            start_x = np.random.randint(w)
            start_y = np.random.randint(h)
            for j in range(1 + np.random.randint(5)):
                angle = 0.01 + np.random.randint(config['ma'])
                if i % 2 == 0:
                    angle = 2 * 3.1415926 - angle
                length = 10 + np.random.randint(config['ml'])
                brush_w = 10 + np.random.randint(config['mbw'])
                end_x = (start_x + length * np.sin(angle)).astype(np.int32)
                end_y = (start_y + length * np.cos(angle)).astype(np.int32)

                cv2.line(mask, (start_y, start_x), (end_y, end_x), 1.0, brush_w)
                start_x, start_y = end_x, end_y

        mask = mask.reshape(mask.shape + (1,)).astype(np.float32)
        return Image.fromarray(np.tile(mask,(1,1,3)).astype(np.uint8))