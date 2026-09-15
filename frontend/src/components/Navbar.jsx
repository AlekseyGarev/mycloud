import { Link, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { logoutUser } from '../store/authSlice';

export default function Navbar() {
  const { user, isAuthenticated } = useSelector((state) => state.auth);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await dispatch(logoutUser());
    navigate('/');
  };

  return (
    <nav className="navbar">
      <h2>
        <Link to={isAuthenticated ? '/storage' : '/'} className="navbar-brand">
          My Cloud Storage
        </Link>
      </h2>
      <div className="navbar-links">
        {isAuthenticated ? (
          <>
            <span className="navbar-user">
              Привет, <strong>{user?.full_name || user?.username}</strong>
            </span>
            <Link to="/storage" className="nav-link">Моё хранилище</Link>
            {(user?.is_admin || user?.is_superuser) && (
              <Link to="/admin" className="nav-link admin">Админ-панель</Link>
            )}
            <button onClick={handleLogout} className="btn btn-danger">
              Выход
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="nav-link text-white">Вход</Link>
            <Link to="/register" className="btn btn-success">Регистрация</Link>
          </>
        )}
      </div>
    </nav>
  );
}