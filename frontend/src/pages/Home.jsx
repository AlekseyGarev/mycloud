import React from 'react';
import { Link, Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux';

export default function Home() {
  const { isAuthenticated } = useSelector((state) => state.auth);

  // Вариант А: Автоматический редирект в хранилище, если пользователь уже залогинен
  if (isAuthenticated) {
    return <Navigate to="/storage" replace />;
  }

  return (
    <div className="home-container text-center">
      <h1>Добро пожаловать в My Cloud Storage!</h1>
      <p>
        Безопасное облачное хранилище для ваших файлов. Загружайте,
        скачивайте, переименовывайте и делитесь файлами по специальным
        публичным ссылкам.
      </p>

      <div className="home-buttons mt-20">
        <Link to="/register" className="btn btn-success mr-10">
          Зарегистрироваться
        </Link>
        <Link to="/login" className="btn btn-primary">
          Войти в аккаунт
        </Link>
      </div>
    </div>
  );
}