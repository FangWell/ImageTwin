import unittest
import tempfile
import os
from database import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # 使用临时数据库文件
        self.db_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.db_file.close()
        self.db = DatabaseManager(self.db_file.name)
        self.db.init_db()
    
    def tearDown(self):
        # 清理临时数据库文件
        if os.path.exists(self.db_file.name):
            os.unlink(self.db_file.name)
    
    def test_init_db(self):
        """测试数据库初始化"""
        # 数据库应该已经被初始化，且没有错误
        total = self.db.get_total_images()
        self.assertEqual(total, 0)
    
    def test_add_image_hash(self):
        """测试添加图片哈希"""
        test_path = '/test/image.jpg'
        test_hash = 'abcd1234'
        
        self.db.add_image_hash(test_path, test_hash, 1024, 1234567890, 800, 600)
        
        total = self.db.get_total_images()
        self.assertEqual(total, 1)
    
    def test_find_similar_images(self):
        """测试相似图片查找"""
        # 添加测试数据
        test_dir = '/test'
        self.db.add_image_hash(f'{test_dir}/image1.jpg', 'abcd1234', 1024, 1234567890, 800, 600)
        self.db.add_image_hash(f'{test_dir}/image2.jpg', 'abcd1235', 1024, 1234567890, 800, 600)
        self.db.add_image_hash(f'{test_dir}/image3.jpg', 'ffff0000', 1024, 1234567890, 800, 600)
        
        # 搜索相似图片
        results = self.db.find_similar_images('abcd1234', test_dir, 0.8)
        
        # 应该找到相似的图片
        self.assertGreater(len(results), 0)
        
        # 第一个结果应该是完全匹配的
        if results:
            path, hash_val, similarity = results[0]
            self.assertEqual(path, f'{test_dir}/image1.jpg')
            self.assertEqual(similarity, 1.0)
    
    def test_clear_all(self):
        """测试清空数据库"""
        # 添加一些数据
        self.db.add_image_hash('/test/image.jpg', 'abcd1234', 1024, 1234567890, 800, 600)
        self.assertEqual(self.db.get_total_images(), 1)
        
        # 清空数据库
        self.db.clear_all()
        self.assertEqual(self.db.get_total_images(), 0)

if __name__ == '__main__':
    unittest.main()