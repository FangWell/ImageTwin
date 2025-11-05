from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from contextlib import asynccontextmanager
import os
import json
import sqlite3
from pathlib import Path
import tempfile
import shutil

from image_processor import ImageProcessor
from database import DatabaseManager

# 初始化组件
image_processor = ImageProcessor()
db_manager = DatabaseManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    db_manager.init_db()
    yield
    # 关闭时的清理工作（如果需要）

app = FastAPI(title="ImageTwin - 图片相似度搜索工具", version="1.0.0", lifespan=lifespan)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "file://", "*"],  # 支持本地文件和Vite
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    directory: str
    similarity_threshold: float = 0.8
    ignore_resolution: bool = False
    ignore_metadata: bool = False

class IndexRequest(BaseModel):
    directories: List[str]

@app.get("/")
async def root():
    return {"message": "ImageTwin API - 图片相似度搜索工具"}

@app.post("/api/search")
async def search_similar_images(
    file: UploadFile = File(...),
    directory: str = Form(...),
    similarity_threshold: float = Form(0.8),
    ignore_resolution: bool = Form(False),
    ignore_metadata: bool = Form(False)
):
    """搜索相似图片"""
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="文件必须是图片格式")
    
    # 保存上传的图片到临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        temp_path = tmp_file.name
    
    try:
        # 计算上传图片的哈希
        upload_hash = image_processor.calculate_hash(temp_path, ignore_resolution, ignore_metadata)
        
        # 搜索相似图片
        similar_images = db_manager.find_similar_images(
            upload_hash, 
            directory, 
            similarity_threshold
        )
        
        results = []
        for image_path, stored_hash, similarity in similar_images:
            if os.path.exists(image_path):
                results.append({
                    "path": image_path,
                    "similarity": similarity,
                    "exists": True
                })
        
        return {
            "results": results,
            "total": len(results),
            "query_hash": str(upload_hash)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)

@app.post("/api/index")
async def index_directory(request: IndexRequest):
    """索引指定目录中的图片"""
    try:
        total_indexed = 0
        for directory in request.directories:
            if not os.path.exists(directory):
                continue
                
            indexed_count = image_processor.index_directory(directory, db_manager)
            total_indexed += indexed_count
            
            # 保存最后索引的目录
            try:
                settings = {"last_directory": directory}
                with open("settings.json", "w", encoding="utf-8") as f:
                    json.dump(settings, f, ensure_ascii=False, indent=2)
            except:
                pass
        
        return {
            "message": f"成功索引 {total_indexed} 张图片",
            "indexed_count": total_indexed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"索引失败: {str(e)}")

@app.get("/api/status")
async def get_status():
    """获取系统状态"""
    total_images = db_manager.get_total_images()
    # 读取上次索引的目录
    last_directory = ""
    try:
        if os.path.exists("settings.json"):
            with open("settings.json", "r", encoding="utf-8") as f:
                settings = json.load(f)
                last_directory = settings.get("last_directory", "")
    except:
        pass
    
    return {
        "total_indexed_images": total_images,
        "status": "running",
        "last_directory": last_directory
    }

@app.delete("/api/clear-index")
async def clear_index():
    """清空索引"""
    try:
        db_manager.clear_all()
        return {"message": "索引已清空"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"清空索引失败: {str(e)}")

@app.get("/api/image/{image_path:path}")
async def get_image(image_path: str):
    """获取图片文件"""
    from fastapi.responses import FileResponse
    import urllib.parse
    
    # URL解码
    decoded_path = urllib.parse.unquote(image_path)
    
    if not os.path.exists(decoded_path):
        raise HTTPException(status_code=404, detail="图片文件不存在")
    
    # 检查是否为图片文件
    if not image_processor.is_image_file(decoded_path):
        raise HTTPException(status_code=400, detail="不是有效的图片文件")
    
    return FileResponse(decoded_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)