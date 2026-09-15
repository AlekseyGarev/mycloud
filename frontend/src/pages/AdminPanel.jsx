import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../api/axiosInstance';

export default function AdminPanel() {
  const [users, setUsers] = useState([]); const [loading, setLoading] = useState(true); const [error, setError] = useState('');
  const load = async () => { try { setLoading(true); setUsers((await api.get('/admin/users/')).data); setError(''); } catch { setError('Не удалось загрузить пользователей'); } finally { setLoading(false); } };
  useEffect(() => { load(); }, []);
  const toggleAdmin = async (u) => { try { const r = await api.patch(`/admin/users/${u.id}/`, { is_admin: !u.is_admin }); setUsers((xs) => xs.map((x) => x.id === u.id ? r.data : x)); } catch (e) { alert(e.response?.data?.detail || 'Не удалось изменить права'); } };
  const removeUser = async (u) => { if (!window.confirm(`Удалить пользователя ${u.username} и его файлы?`)) return; try { await api.delete(`/admin/users/${u.id}/`); setUsers((xs) => xs.filter((x) => x.id !== u.id)); } catch (e) { alert(e.response?.data?.detail || 'Не удалось удалить пользователя'); } };
  const size = (n) => n < 1024 ? `${n} B` : n < 1048576 ? `${(n/1024).toFixed(1)} KB` : `${(n/1048576).toFixed(1)} MB`;
  return <div className="container" style={{ marginTop: 30 }}><h2>Панель администратора</h2>{error && <div className="alert-error">{error}</div>}
    <div className="table-responsive mt-15"><table className="data-table"><thead><tr><th>Логин</th><th>Полное имя</th><th>Email</th><th>Администратор</th><th>Файлов</th><th>Объём</th><th>Хранилище</th><th>Действия</th></tr></thead><tbody>
      {loading ? <tr><td colSpan="8">Загрузка...</td></tr> : users.map((u) => <tr key={u.id}><td>{u.username}</td><td>{u.full_name}</td><td>{u.email}</td><td>{u.is_admin ? 'Да' : 'Нет'}</td><td>{u.files_count}</td><td>{size(u.total_size)}</td>
        <td><Link className="btn btn-primary btn-sm" to={`/storage?user_id=${u.id}&username=${encodeURIComponent(u.username)}`}>Управлять файлами</Link></td>
        <td><div className="action-buttons"><button className="btn btn-warning btn-sm" onClick={() => toggleAdmin(u)}>{u.is_admin ? 'Снять админа' : 'Сделать админом'}</button><button className="btn btn-danger btn-sm" onClick={() => removeUser(u)}>Удалить</button></div></td></tr>)}</tbody></table></div>
  </div>;
}
