import os
import imagehash
from PIL import Image
from pathlib import Path
from typing import Optional, List
import mimetypes

class ImageProcessor:
    # 支持的图片格式
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    
    def __init__(self):
        """初始化图片处理器"""
        pass
    
    def is_image_file(self, file_path: str) -> bool:
        """判断文件是否为支持的图片格式"""
        return Path(file_path).suffix.lower() in self.SUPPORTED_FORMATS
    
    def calculate_hash(self, image_path: str, ignore_resolution: bool = False, 
                      ignore_metadata: bool = False) -> str:
        """计算图片的感知哈希值"""
        try:
            with Image.open(image_path) as img:
                # 如果需要忽略分辨率，先调整为标准尺寸
                if ignore_resolution:
                    # 保持宽高比，调整到256x256以内
                    img.thumbnail((256, 256), Image.Resampling.LANCZOS)
                
                # 如果需要忽略元数据，移除EXIF信息
                if ignore_metadata:
                    # 创建新图片，不包含元数据
                    if img.mode in ('RGBA', 'LA'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                
                # 计算感知哈希
                phash = imagehash.phash(img, hash_size=16)
                return str(phash)
                
        except Exception as e:
            raise Exception(f"计算图片哈希失败 {image_path}: {str(e)}")
    
    def get_image_info(self, image_path: str) -> dict:
        """获取图片基本信息"""
        try:
            stat = os.stat(image_path)
            with Image.open(image_path) as img:
                return {
                    'width': img.width,
                    'height': img.height,
                    'size': stat.st_size,
                    'modified_time': stat.st_mtime,
                    'format': img.format
                }
        except Exception as e:
            return {
                'width': 0,
                'height': 0,
                'size': os.path.getsize(image_path) if os.path.exists(image_path) else 0,
                'modified_time': os.path.getmtime(image_path) if os.path.exists(image_path) else 0,
                'format': 'unknown'
            }
    
    def scan_directory(self, directory: str) -> List[str]:
        """扫描目录中的所有图片文件"""
        image_files = []
        directory_path = Path(directory)
        
        if not directory_path.exists():
            return image_files
        
        # 递归搜索所有图片文件
        for file_path in directory_path.rglob('*'):
            if file_path.is_file() and self.is_image_file(str(file_path)):
                image_files.append(str(file_path))
        
        return image_files
    
    def index_directory(self, directory: str, db_manager) -> int:
        """索引指定目录中的所有图片"""
        image_files = self.scan_directory(directory)
        indexed_count = 0
        
        for image_path in image_files:
            try:
                # 获取图片信息
                info = self.get_image_info(image_path)
                
                # 计算哈希值
                hash_value = self.calculate_hash(image_path)
                
                # 保存到数据库
                db_manager.add_image_hash(
                    file_path=image_path,
                    hash_value=hash_value,
                    file_size=info['size'],
                    modified_time=info['modified_time'],
                    width=info['width'],
                    height=info['height']
                )
                
                indexed_count += 1
                
            except Exception as e:
                print(f"索引图片失败 {image_path}: {str(e)}")
                continue
        
        return indexed_count
    
    def compare_images(self, image1_path: str, image2_path: str, 
                      ignore_resolution: bool = False, 
                      ignore_metadata: bool = False) -> float:
        """比较两张图片的相似度"""
        try:
            hash1 = self.calculate_hash(image1_path, ignore_resolution, ignore_metadata)
            hash2 = self.calculate_hash(image2_path, ignore_resolution, ignore_metadata)
            
            hash1_obj = imagehash.hex_to_hash(hash1)
            hash2_obj = imagehash.hex_to_hash(hash2)
            
            # 计算汉明距离
            hamming_distance = hash1_obj - hash2_obj
            max_distance = len(hash1) * 4  # 每个hex字符代表4位
            
            # 转换为相似度 (0-1)
            similarity = 1.0 - (hamming_distance / max_distance)
            return max(0.0, min(1.0, similarity))
            
        except Exception as e:
            raise Exception(f"比较图片失败: {str(e)}")