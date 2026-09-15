import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { checkAuth } from './store/authSlice';

import './App.css';

import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Storage from './pages/Storage';
import PublicDownload from './pages/PublicDownload';
import AdminPanel from './pages/AdminPanel'; 

function ProtectedRoute({ children, adminOnly = false }) {
  const { user, isAuthenticated, loading } = useSelector((state) => state.auth);

  if (loading) return <div className="container loading-container">Загрузка...</div>;
  if (!isAuthenticated) return <Navigate to="/login" replace />;

  const isAdmin = user?.is_admin || user?.is_superuser || user?.is_staff;
  if (adminOnly && !isAdmin) return <Navigate to="/storage" replace />;

  return children;
}

export default function App() {
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(checkAuth());
  }, [dispatch]);

  return (
    <BrowserRouter>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/share/:special_link" element={<PublicDownload />} />
          <Route path="/storage" element={
            <ProtectedRoute>
              <Storage />
            </ProtectedRoute>
          } />
          <Route path="/admin" element={
            <ProtectedRoute adminOnly={true}>
              <AdminPanel />
            </ProtectedRoute>
          } />
        </Routes>
      </div>
    </BrowserRouter>
  );
}