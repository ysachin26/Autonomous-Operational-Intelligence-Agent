import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, File, Trash2 } from 'lucide-react';

const FileUploadSection = ({ onFilesUpload }) => {
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const onDrop = useCallback((acceptedFiles) => {
    setUploadedFiles(prev => [...prev, ...acceptedFiles]);
    onFilesUpload(acceptedFiles);
  }, [onFilesUpload]);

  const removeFile = (fileToRemove) => {
    const newFiles = uploadedFiles.filter(file => file !== fileToRemove);
    setUploadedFiles(newFiles);
    onFilesUpload(newFiles);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div className="file-upload-section card">
      <h3><UploadCloud size={20} /> Attach Files</h3>
      <div {...getRootProps({ className: `dropzone ${isDragActive ? 'active' : ''}` })}>
        <input {...getInputProps()} />
        <p>Drag & drop files here, or click to select</p>
      </div>
      {uploadedFiles.length > 0 && (
        <div className="file-list">
          <h4>Uploaded Files:</h4>
          <ul>
            {uploadedFiles.map((file, index) => (
              <li key={index}>
                <File size={16} />
                <span>{file.name}</span>
                <button onClick={() => removeFile(file)} className="remove-file-btn">
                  <Trash2 size={16} />
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FileUploadSection;