import { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate, Link } from 'react-router-dom';
import { loginUser, clearError } from '../store/authSlice';

export default function Login() {
  const [username, setUsername] = useState(''); const [password, setPassword] = useState(''); const [showPassword, setShowPassword] = useState(false);
  const dispatch = useDispatch(); const navigate = useNavigate(); const { error } = useSelector((s) => s.auth);
  const submit = async (e) => { e.preventDefault(); dispatch(clearError()); const r = await dispatch(loginUser({ username, password })); if (loginUser.fulfilled.match(r)) navigate(r.payload?.is_admin ? '/admin' : '/storage'); };
  return <div className="auth-form-container"><h2 className="auth-form-title">Вход в систему</h2>{error && <div className="alert-error">{error}</div>}<form onSubmit={submit}>
    <div className="form-group"><label>Логин:</label><input className="form-input" value={username} onChange={(e) => setUsername(e.target.value)} required /></div>
    <div className="form-group"><label>Пароль:</label><div className="password-wrapper"><input type={showPassword?'text':'password'} className="form-input password-input" value={password} onChange={(e) => setPassword(e.target.value)} required /><button type="button" className="password-toggle-btn" onClick={() => setShowPassword((v)=>!v)}>{showPassword?'🙈':'👁️'}</button></div></div>
    <button className="btn btn-primary w-100 mt-10">Войти</button></form><p className="mt-15 text-center text-sm">Ещё нет аккаунта? <Link to="/register">Зарегистрироваться</Link></p></div>;
}
