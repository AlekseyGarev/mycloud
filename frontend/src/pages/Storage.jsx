import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useSearchParams } from 'react-router-dom';
import { fetchFiles, uploadFile, deleteFile, updateFile } from '../store/fileSlice';
import api from '../api/axiosInstance';

export default function Storage() {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const { items: files, loading, error } = useSelector((state) => state.files);
  const [searchParams] = useSearchParams();
  const requestedUserId = searchParams.get('user_id');
  const requestedUsername = searchParams.get('username');
  const isAdmin = Boolean(user?.is_admin || user?.is_superuser);
  const targetUserId = isAdmin && requestedUserId ? requestedUserId : null;
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [customName, setCustomName] = useState('');
  const [comment, setComment] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editOriginalName, setEditOriginalName] = useState('');
  const [editComment, setEditComment] = useState('');
  const [generatedLink, setGeneratedLink] = useState('');

  useEffect(() => { dispatch(fetchFiles(targetUserId)); }, [dispatch, targetUserId]);

  const handleFileChange = (e) => {
    const arr = Array.from(e.target.files || []);
    setSelectedFiles(arr);
    if (arr.length === 1) setCustomName(arr[0].name);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFiles.length) return;
    const formData = new FormData();
    selectedFiles.forEach((file) => formData.append('files', file));
    if (customName.trim()) formData.append('original_name', customName.trim());
    if (comment.trim()) formData.append('comment', comment.trim());
    if (targetUserId) formData.append('user_id', targetUserId);
    const result = await dispatch(uploadFile({ formData, userId: targetUserId }));
    if (uploadFile.fulfilled.match(result)) {
      setSelectedFiles([]); setCustomName(''); setComment('');
      const input = document.getElementById('file-input'); if (input) input.value = '';
    }
  };

  const handleDelete = (id) => { if (window.confirm('Удалить файл?')) dispatch(deleteFile(id)); };
  const startEdit = (file) => { setEditingId(file.id); setEditOriginalName(file.original_name); setEditComment(file.comment || ''); };
  const saveEdit = async (id) => {
    const result = await dispatch(updateFile({ id, data: { original_name: editOriginalName, comment: editComment } }));
    if (updateFile.fulfilled.match(result)) setEditingId(null);
  };
  const handleDownload = async (id, fileName) => {
    try {
      const response = await api.get(`/files/${id}/download/`, { responseType: 'blob' });
      const url = URL.createObjectURL(response.data); const link = document.createElement('a');
      link.href = url; link.download = fileName; document.body.appendChild(link); link.click(); link.remove(); URL.revokeObjectURL(url);
      dispatch(fetchFiles(targetUserId));
    } catch { alert('Ошибка при скачивании файла'); }
  };
  const handleShare = async (id) => {
    try { const response = await api.post(`/files/${id}/share/`); setGeneratedLink(response.data.public_url || `${window.location.origin}/share/${response.data.special_link}`); }
    catch { alert('Ошибка при получении публичной ссылки'); }
  };
  const formatSize = (bytes) => bytes < 1024 ? `${bytes} B` : bytes < 1048576 ? `${(bytes/1024).toFixed(1)} KB` : `${(bytes/1048576).toFixed(1)} MB`;
  const formatDate = (value) => value ? new Date(value).toLocaleString('ru-RU') : 'Никогда';

  return (
    <div className="container">
      <h2 className="home-title">{targetUserId ? `Хранилище пользователя ${requestedUsername || `#${targetUserId}`}` : 'Моё хранилище файлов'}</h2>
      <div className="file-upload-card">
        <h3>Загрузить новый файл</h3>
        <form onSubmit={handleUpload} className="mt-15">
          <div className="upload-grid">
            <div className="form-group"><label>Выберите файл(ы):</label><input id="file-input" type="file" multiple className="form-input" onChange={handleFileChange} required /></div>
            <div className="form-group"><label>Имя файла (для одного файла):</label><input type="text" className="form-input" value={customName} onChange={(e) => setCustomName(e.target.value)} disabled={selectedFiles.length > 1} /></div>
          </div>
          <div className="form-group"><label>Комментарий:</label><input type="text" className="form-input" value={comment} onChange={(e) => setComment(e.target.value)} /></div>
          <button type="submit" className="btn btn-primary mt-10 w-100">Загрузить на сервер</button>
        </form>
      </div>
      {generatedLink && <div className="share-link-box mb-15"><span>Специальная ссылка:</span><input className="share-input" value={generatedLink} readOnly /><button onClick={() => navigator.clipboard.writeText(generatedLink)} className="btn btn-success btn-sm">Скопировать</button></div>}
      {error && <div className="alert-error">{typeof error === 'string' ? error : JSON.stringify(error)}</div>}
      <div className="table-container table-responsive">
        <table className="data-table"><thead><tr><th>Имя файла</th><th>Размер</th><th>Дата загрузки</th><th>Последнее скачивание</th><th>Комментарий</th><th>Действия</th></tr></thead>
          <tbody>{loading ? <tr><td colSpan="6">Загрузка...</td></tr> : files.length === 0 ? <tr><td colSpan="6">Хранилище пустое</td></tr> : files.map((file) => (
            <tr key={file.id}>
              <td>{editingId === file.id ? <input className="form-input" value={editOriginalName} onChange={(e) => setEditOriginalName(e.target.value)} /> : file.original_name}</td>
              <td>{formatSize(file.size)}</td><td>{formatDate(file.uploaded_at)}</td><td>{formatDate(file.last_downloaded_at)}</td>
              <td>{editingId === file.id ? <input className="form-input" value={editComment} onChange={(e) => setEditComment(e.target.value)} /> : (file.comment || '—')}</td>
              <td><div className="action-buttons">{editingId === file.id ? <button onClick={() => saveEdit(file.id)} className="btn btn-success btn-sm">Сохранить</button> : <>
                <button onClick={() => handleDownload(file.id, file.original_name)} className="btn btn-primary btn-sm">Скачать</button>
                <button onClick={() => startEdit(file)} className="btn btn-warning btn-sm">Редактировать</button>
                <button onClick={() => handleShare(file.id)} className="btn btn-secondary btn-sm">Поделиться</button>
                <button onClick={() => handleDelete(file.id)} className="btn btn-danger btn-sm">Удалить</button>
              </>}</div></td>
            </tr>))}</tbody>
        </table>
      </div>
    </div>
  );
}
