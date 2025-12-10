import sqlite3
import os
from typing import List, Tuple
from pathlib import Path
import imagehash

class DatabaseManager:
    def __init__(self, db_path: str = "image_index.db"):
        self.db_path = db_path
        
    def init_db(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS image_hashes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT UNIQUE NOT NULL,
                hash_value TEXT NOT NULL,
                file_size INTEGER,
                modified_time REAL,
                width INTEGER,
                height INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建索引以提高查询性能
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_hash_value ON image_hashes(hash_value)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_file_path ON image_hashes(file_path)')
        
        conn.commit()
        conn.close()
    
    def add_image_hash(self, file_path: str, hash_value: str, file_size: int, 
                      modified_time: float, width: int, height: int):
        """添加或更新图片哈希"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO image_hashes 
            (file_path, hash_value, file_size, modified_time, width, height)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (file_path, hash_value, file_size, modified_time, width, height))
        
        conn.commit()
        conn.close()
    
    def find_similar_images(self, query_hash: str, directory: str, 
                          threshold: float) -> List[Tuple[str, str, float]]:
        """查找相似图片"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取指定目录下的所有图片
        cursor.execute('''
            SELECT file_path, hash_value FROM image_hashes 
            WHERE file_path LIKE ?
        ''', (f"{directory}%",))
        
        results = []
        query_hash_obj = imagehash.hex_to_hash(query_hash)
        
        for file_path, stored_hash in cursor.fetchall():
            try:
                stored_hash_obj = imagehash.hex_to_hash(stored_hash)
                # 计算汉明距离，转换为相似度
                hamming_distance = query_hash_obj - stored_hash_obj
                max_distance = len(query_hash) * 4  # 每个hex字符代表4位
                similarity = 1.0 - (hamming_distance / max_distance)
                
                if similarity >= threshold:
                    results.append((file_path, stored_hash, similarity))
            except Exception:
                continue
        
        # 按相似度降序排序
        results.sort(key=lambda x: x[2], reverse=True)
        conn.close()
        
        return results
    
    def get_total_images(self) -> int:
        """获取索引中的图片总数"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM image_hashes')
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def clear_all(self):
        """清空所有索引"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM image_hashes')
        conn.commit()
        conn.close()
    
    def remove_missing_files(self):
        """删除不存在的文件记录"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, file_path FROM image_hashes')
        to_remove = []
        
        for image_id, file_path in cursor.fetchall():
            if not os.path.exists(file_path):
                to_remove.append(image_id)
        
        if to_remove:
            cursor.execute(f'DELETE FROM image_hashes WHERE id IN ({",".join("?" * len(to_remove))})', to_remove)
            conn.commit()
        
        conn.close()
        return len(to_remove)
    
    def get_images_in_directory(self, directory: str) -> List[Tuple[str, str]]:
        """获取指定目录中已索引的图片"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT file_path, hash_value FROM image_hashes 
            WHERE file_path LIKE ?
        ''', (f"{directory}%",))
        
        results = cursor.fetchall()
        conn.close()
        return results