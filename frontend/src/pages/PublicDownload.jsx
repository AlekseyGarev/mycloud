import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api/axiosInstance';

export default function PublicDownload() {
  const { special_link } = useParams();
  const [fileInfo, setFileInfo] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get(`/public/files/${special_link}/`)
      .then((res) => setFileInfo(res.data))
      .catch(() => setError('Ссылка недействительна или файл был удалён.'));
  }, [special_link]);

  const handleDownload = () => {
    window.location.assign(`/api/public/files/${special_link}/download/`);
  };

  return (
    <div className="auth-form-container text-center">
      <h2>Публичное скачивание файла</h2>
      {error ? <div className="alert-error mt-15">{error}</div> : fileInfo ? (
        <div className="mt-15">
          <p><strong>Имя файла:</strong> {fileInfo.original_name}</p>
          <p><strong>Размер:</strong> {(fileInfo.size / 1024).toFixed(1)} KB</p>
          {fileInfo.comment && <p><strong>Описание:</strong> {fileInfo.comment}</p>}
          <button onClick={handleDownload} className="btn btn-success mt-15 w-100">Скачать файл</button>
        </div>
      ) : <p className="mt-15">Загрузка информации о файле...</p>}
    </div>
  );
}
