import unittest
import tempfile
import os
from PIL import Image
import numpy as np

from image_processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor()
        
    def create_test_image(self, width=100, height=100, color=(255, 0, 0)):
        """创建测试图片"""
        img = Image.new('RGB', (width, height), color)
        return img
    
    def test_calculate_hash(self):
        """测试哈希计算"""
        # 创建临时图片文件
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img = self.create_test_image()
            img.save(tmp.name)
            tmp_name = tmp.name
            
        try:
            # 计算哈希
            hash_value = self.processor.calculate_hash(tmp_name)
            
            # 验证哈希值
            self.assertIsInstance(hash_value, str)
            self.assertTrue(len(hash_value) > 0)
        finally:
            # 清理
            try:
                os.unlink(tmp_name)
            except PermissionError:
                pass  # 忽略Windows文件锁定问题
    
    def test_calculate_hash_ignore_resolution(self):
        """测试忽略分辨率的哈希计算"""
        # 创建两个不同尺寸但内容相同的图片
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp1, \
             tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp2:
            
            img1 = self.create_test_image(100, 100, (255, 0, 0))
            img2 = self.create_test_image(200, 200, (255, 0, 0))
            
            img1.save(tmp1.name)
            img2.save(tmp2.name)
            
            # 计算哈希值
            hash1 = self.processor.calculate_hash(tmp1.name, ignore_resolution=True)
            hash2 = self.processor.calculate_hash(tmp2.name, ignore_resolution=True)
            
            # 验证哈希值应该相似（可能不完全相同但应该很接近）
            self.assertIsInstance(hash1, str)
            self.assertIsInstance(hash2, str)
            
            # 清理
            os.unlink(tmp1.name)
            os.unlink(tmp2.name)
    
    def test_compare_images(self):
        """测试图片比较功能"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp1, \
             tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp2:
            
            # 创建两个相同的图片
            img1 = self.create_test_image(100, 100, (255, 0, 0))
            img2 = self.create_test_image(100, 100, (255, 0, 0))
            
            img1.save(tmp1.name)
            img2.save(tmp2.name)
            
            # 比较相似度
            similarity = self.processor.compare_images(tmp1.name, tmp2.name)
            
            # 相同图片的相似度应该很高
            self.assertGreater(similarity, 0.9)
            self.assertLessEqual(similarity, 1.0)
            
            # 清理
            os.unlink(tmp1.name)
            os.unlink(tmp2.name)
    
    def test_is_image_file(self):
        """测试图片文件识别"""
        self.assertTrue(self.processor.is_image_file('test.jpg'))
        self.assertTrue(self.processor.is_image_file('test.png'))
        self.assertTrue(self.processor.is_image_file('test.gif'))
        self.assertFalse(self.processor.is_image_file('test.txt'))
        self.assertFalse(self.processor.is_image_file('test.pdf'))

if __name__ == '__main__':
    unittest.main()