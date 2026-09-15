import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../api/axiosInstance';

export const checkAuth = createAsyncThunk('auth/checkAuth', async (_, { rejectWithValue }) => {
  try {
    await api.get('/auth/csrf/');
    const response = await api.get('/auth/me/');
    return response.data;
  } catch (err) {
    return rejectWithValue(err.response?.data || 'Не авторизован');
  }
});

export const loginUser = createAsyncThunk('auth/loginUser', async (credentials, { rejectWithValue }) => {
  try {
    const response = await api.post('/auth/login/', credentials);
    return response.data;
  } catch (err) {
    return rejectWithValue(err.response?.data || 'Ошибка входа');
  }
});

export const registerUser = createAsyncThunk('auth/registerUser', async (userData, { rejectWithValue }) => {
  try {
    const response = await api.post('/auth/register/', userData);
    return response.data;
  } catch (err) {
    return rejectWithValue(err.response?.data || 'Ошибка при регистрации');
  }
});

export const logoutUser = createAsyncThunk('auth/logoutUser', async () => {
  await api.post('/auth/logout/');
  return null;
});

// Вспомогательная функция для безопасного формирования текста ошибки
const formatError = (payload) => {
  if (!payload) return 'Произошла ошибка';
  if (typeof payload === 'string') return payload;
  if (typeof payload === 'object') {
    if (payload.detail) return payload.detail;
    return Object.entries(payload)
      .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join(' ') : val}`)
      .join(' | ');
  }
  return String(payload);
};

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    user: null,
    isAuthenticated: false,
    loading: true,
    error: null,
  },
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // checkAuth
      .addCase(checkAuth.pending, (state) => {
        state.loading = true;
      })
      .addCase(checkAuth.fulfilled, (state, action) => {
        state.user = action.payload;
        state.isAuthenticated = true;
        state.loading = false;
      })
      .addCase(checkAuth.rejected, (state) => {
        state.user = null;
        state.isAuthenticated = false;
        state.loading = false;
      })
      // loginUser
      .addCase(loginUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.user = action.payload;
        state.isAuthenticated = true;
        state.loading = false;
        state.error = null;
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.loading = false;
        state.error = formatError(action.payload);
      })
      // registerUser
      .addCase(registerUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(registerUser.fulfilled, (state) => {
        state.loading = false;
        state.error = null;
      })
      .addCase(registerUser.rejected, (state, action) => {
        state.loading = false;
        state.error = formatError(action.payload);
      })
      // logoutUser
      .addCase(logoutUser.fulfilled, (state) => {
        state.user = null;
        state.isAuthenticated = false;
        state.loading = false;
        state.error = null;
      });
  },
});

export const { clearError } = authSlice.actions;
export default authSlice.reducer;