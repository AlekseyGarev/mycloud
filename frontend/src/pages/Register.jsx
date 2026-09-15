import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, Link } from "react-router-dom";
import { registerUser } from "../store/authSlice";

export default function Register() {
  const [username, setUsername] = useState("");
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [validationError, setValidationError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { loading, error } = useSelector((state) => state.auth);

  const validate = () => {
    if (!/^[A-Za-z][A-Za-z0-9]{3,19}$/.test(username))
      return "Логин: 4–20 символов, только латинские буквы и цифры, первый символ — буква.";
    if (!fullName.trim()) return "Укажите полное имя.";
    if (!/^\S+@\S+\.\S+$/.test(email)) return "Введите корректный email.";
    if (
      password.length < 6 ||
      !/[A-Z]/.test(password) ||
      !/\d/.test(password) ||
      !/[^A-Za-z0-9]/.test(password)
    ) {
      return "Пароль: минимум 6 символов, заглавная буква, цифра и специальный символ.";
    }
    return "";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const message = validate();
    setValidationError(message);
    if (message) return;
    const result = await dispatch(
      registerUser({
        username,
        full_name: fullName.trim(),
        email: email.trim(),
        password,
      })
    );
    if (registerUser.fulfilled.match(result)) navigate("/login");
  };

  return (
    <div className="auth-container">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h2 className="auth-title">Регистрация</h2>
        {(error || validationError) && (
          <div className="auth-error-message">{validationError || error}</div>
        )}
        <div className="form-group">
          <label className="form-label">Логин:</label>
          <input
            type="text"
            required
            minLength={4}
            maxLength={20}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="form-input"
          />
          <small className="field-hint">
            4–20 символов: латинские буквы и цифры, первый символ — буква.
          </small>
        </div>
        <div className="form-group">
          <label className="form-label">Полное имя:</label>
          <input
            type="text"
            required
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            className="form-input"
          />
        </div>
        <div className="form-group">
          <label className="form-label">Email:</label>
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="form-input"
          />
        </div>
        <div className="form-group">
          <label className="form-label">Пароль:</label>
          <div className="password-wrapper">
            <input
              type={showPassword ? "text" : "password"}
              required
              minLength={6}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="form-input password-input"
            />
            <button
              type="button"
              className="password-toggle-btn"
              onClick={() => setShowPassword((v) => !v)}
            >
              {showPassword ? "🙈" : "👁️"}
            </button>
          </div>
          <small className="field-hint">
            Минимум 6 символов: заглавная буква, цифра и специальный символ.
          </small>
        </div>
        <button type="submit" disabled={loading} className="auth-submit-btn">
          {loading ? "Регистрация..." : "Зарегистрироваться"}
        </button>
        <p className="auth-footer-text">
          Уже зарегистрированы?{" "}
          <Link to="/login" className="auth-link">
            Войти
          </Link>
        </p>
      </form>
    </div>
  );
}
