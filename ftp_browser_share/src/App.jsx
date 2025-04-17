import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [files, setFiles] = useState([])
  const [sharedFiles, setSharedFiles] = useState([])

  useEffect(() => {
    fetchFiles()
  }, [])

  const fetchFiles = async () => {
    try {
      const response = await axios.get('/api/files')
      setFiles(response.data.files)
    } catch (error) {
      console.error('Error fetching files:', error)
    }
  }

  const shareFile = async (filename) => {
    try {
      const response = await axios.post('/api/share', { filename })
      setSharedFiles([...sharedFiles, {
        name: filename,
        url: response.data.url
      }])
    } catch (error) {
      console.error('Error sharing file:', error)
    }
  }

  return (
    <div className="app">
      <h1>ESP32 FTP Browser Share</h1>
      
      <div className="file-browser">
        <h2>Files on ESP32</h2>
        <ul>
          {files.map((file, index) => (
            <li key={index}>
              {file}
              <button onClick={() => shareFile(file)}>Share</button>
            </li>
          ))}
        </ul>
      </div>

      <div className="shared-files">
        <h2>Shared Files</h2>
        <ul>
          {sharedFiles.map((file, index) => (
            <li key={index}>
              <a href={file.url} target="_blank" rel="noopener noreferrer">
                {file.name}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default App
