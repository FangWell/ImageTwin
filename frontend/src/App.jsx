import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'
import './App.css'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [searchDirectory, setSearchDirectory] = useState('')
  const [similarityThreshold, setSimilarityThreshold] = useState(0.8)
  const [ignoreResolution, setIgnoreResolution] = useState(false)
  const [ignoreMetadata, setIgnoreMetadata] = useState(false)
  const [lockIgnoreResolution, setLockIgnoreResolution] = useState(false)
  const [lockIgnoreMetadata, setLockIgnoreMetadata] = useState(false)
  const [results, setResults] = useState([])
  const [isSearching, setIsSearching] = useState(false)
  const [isIndexing, setIsIndexing] = useState(false)
  const [status, setStatus] = useState({ total_indexed_images: 0 })

  // 文件拖拽处理
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setSelectedFile(acceptedFiles[0])
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.webp', '.tiff']
    },
    maxFiles: 1
  })

  // 获取系统状态
  const fetchStatus = async () => {
    try {
      const response = await axios.get('/api/status')
      setStatus(response.data)
    } catch (error) {
      console.error('获取状态失败:', error)
    }
  }

  // 索引目录
  const handleIndexDirectory = async () => {
    if (!searchDirectory.trim()) {
      alert('请输入搜索目录')
      return
    }

    setIsIndexing(true)
    try {
      const response = await axios.post('/api/index', {
        directories: [searchDirectory.trim()]
      })
      alert(response.data.message)
      await fetchStatus() // 更新状态
    } catch (error) {
      alert(`索引失败: ${error.response?.data?.detail || error.message}`)
    } finally {
      setIsIndexing(false)
    }
  }

  // 搜索相似图片
  const handleSearch = async () => {
    if (!selectedFile) {
      alert('请选择一张图片')
      return
    }
    if (!searchDirectory.trim()) {
      alert('请输入搜索目录')
      return
    }

    setIsSearching(true)
    setResults([])

    try {
      const formData = new FormData()
      formData.append('file', selectedFile)
      formData.append('directory', searchDirectory.trim())
      formData.append('similarity_threshold', similarityThreshold.toString())
      formData.append('ignore_resolution', ignoreResolution.toString())
      formData.append('ignore_metadata', ignoreMetadata.toString())

      const response = await axios.post('/api/search', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      setResults(response.data.results)
    } catch (error) {
      alert(`搜索失败: ${error.response?.data?.detail || error.message}`)
    } finally {
      setIsSearching(false)
    }
  }

  // 复制路径到剪贴板
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      alert('路径已复制到剪贴板')
    }).catch(() => {
      alert('复制失败')
    })
  }

  // 打开文件夹
  const openFolder = (filePath) => {
    const folderPath = filePath.substring(0, filePath.lastIndexOf('\\'))
    // 在实际应用中，这需要通过后端API来实现
    alert(`请手动打开文件夹: ${folderPath}`)
  }

  React.useEffect(() => {
    fetchStatus()
  }, [])

  return (
    <div className="App">
      <h1>🔍 图片相似度搜索工具</h1>
      
      {/* 状态信息 */}
      <div className="status">
        <p>已索引图片: {status.total_indexed_images} 张</p>
      </div>

      {/* 搜索目录设置 */}
      <div className="control-group">
        <label htmlFor="directory">搜索目录:</label>
        <input
          id="directory"
          type="text"
          className="input"
          value={searchDirectory}
          onChange={(e) => setSearchDirectory(e.target.value)}
          placeholder="例如: C:\Pictures"
          style={{ width: '400px' }}
        />
        <button 
          className="button" 
          onClick={handleIndexDirectory}
          disabled={isIndexing}
        >
          {isIndexing ? '索引中...' : '索引目录'}
        </button>
      </div>

      {/* 图片上传区域 */}
      <div 
        {...getRootProps()} 
        className={`upload-area ${isDragActive ? 'dragover' : ''}`}
      >
        <input {...getInputProps()} />
        {selectedFile ? (
          <div>
            <p>已选择: {selectedFile.name}</p>
            <img 
              src={URL.createObjectURL(selectedFile)} 
              alt="预览" 
              style={{ maxWidth: '200px', maxHeight: '200px' }}
            />
          </div>
        ) : (
          <p>
            {isDragActive ? 
              '拖放图片到这里...' : 
              '拖放图片到这里，或点击选择图片'
            }
          </p>
        )}
      </div>

      {/* 搜索控制参数 */}
      <div className="controls">
        <div className="control-group">
          <label>相似度阈值: {similarityThreshold.toFixed(2)}</label>
          <div className="slider-container">
            <input
              type="range"
              min="0.1"
              max="1.0"
              step="0.01"
              value={similarityThreshold}
              onChange={(e) => setSimilarityThreshold(parseFloat(e.target.value))}
            />
            <input
              type="number"
              className="input"
              min="0.1"
              max="1.0"
              step="0.01"
              value={similarityThreshold}
              onChange={(e) => setSimilarityThreshold(parseFloat(e.target.value))}
              style={{ width: '80px' }}
            />
          </div>
        </div>

        <div className="control-group">
          <label>
            <input
              type="checkbox"
              className="checkbox"
              checked={ignoreResolution}
              onChange={(e) => !lockIgnoreResolution && setIgnoreResolution(e.target.checked)}
              disabled={lockIgnoreResolution}
            />
            忽略分辨率差异
            <button
              className="button"
              onClick={() => setLockIgnoreResolution(!lockIgnoreResolution)}
              style={{ marginLeft: '0.5rem', padding: '0.2rem 0.5rem' }}
            >
              {lockIgnoreResolution ? '🔒' : '🔓'}
            </button>
          </label>
        </div>

        <div className="control-group">
          <label>
            <input
              type="checkbox"
              className="checkbox"
              checked={ignoreMetadata}
              onChange={(e) => !lockIgnoreMetadata && setIgnoreMetadata(e.target.checked)}
              disabled={lockIgnoreMetadata}
            />
            忽略图片元数据
            <button
              className="button"
              onClick={() => setLockIgnoreMetadata(!lockIgnoreMetadata)}
              style={{ marginLeft: '0.5rem', padding: '0.2rem 0.5rem' }}
            >
              {lockIgnoreMetadata ? '🔒' : '🔓'}
            </button>
          </label>
        </div>
      </div>

      {/* 搜索按钮 */}
      <button 
        className="button" 
        onClick={handleSearch}
        disabled={isSearching}
        style={{ fontSize: '1.2rem', padding: '0.8rem 2rem' }}
      >
        {isSearching ? '搜索中...' : '🔍 搜索相似图片'}
      </button>

      {/* 搜索结果 */}
      {results.length > 0 && (
        <div className="results">
          <h2>搜索结果 ({results.length} 张相似图片)</h2>
          {results.map((result, index) => (
            <div key={index} className="result-item">
              <div className="result-similarity">
                相似度: {(result.similarity * 100).toFixed(1)}%
              </div>
              <div className="result-path">{result.path}</div>
              <div>
                <button 
                  className="button"
                  onClick={() => copyToClipboard(result.path)}
                >
                  📋 复制路径
                </button>
                <button 
                  className="button"
                  onClick={() => openFolder(result.path)}
                >
                  📁 打开文件夹
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default App