import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import api from '../api/axiosInstance';

const errorValue = (err, fallback) => err.response?.data?.detail || err.response?.data || fallback;

export const fetchFiles = createAsyncThunk('files/fetchFiles', async (userId = null, { rejectWithValue }) => {
  try { return (await api.get(userId ? `/files/?user_id=${encodeURIComponent(userId)}` : '/files/')).data; }
  catch (err) { return rejectWithValue(errorValue(err, 'Ошибка загрузки файлов')); }
});
export const uploadFile = createAsyncThunk('files/uploadFile', async ({ formData }, { rejectWithValue }) => {
  try { return (await api.post('/files/', formData)).data; }
  catch (err) { return rejectWithValue(errorValue(err, 'Ошибка при загрузке файла')); }
});
export const deleteFile = createAsyncThunk('files/deleteFile', async (fileId, { rejectWithValue }) => {
  try { await api.delete(`/files/${fileId}/`); return fileId; }
  catch (err) { return rejectWithValue(errorValue(err, 'Ошибка при удалении файла')); }
});
export const updateFile = createAsyncThunk('files/updateFile', async ({ id, data }, { rejectWithValue }) => {
  try { return (await api.patch(`/files/${id}/`, data)).data; }
  catch (err) { return rejectWithValue(errorValue(err, 'Ошибка при обновлении файла')); }
});

const fileSlice = createSlice({ name: 'files', initialState: { items: [], loading: false, error: null }, reducers: {}, extraReducers: (builder) => builder
  .addCase(fetchFiles.pending, (s) => { s.loading = true; s.error = null; })
  .addCase(fetchFiles.fulfilled, (s, a) => { s.items = a.payload; s.loading = false; })
  .addCase(fetchFiles.rejected, (s, a) => { s.loading = false; s.error = a.payload; })
  .addCase(uploadFile.fulfilled, (s, a) => { const added = Array.isArray(a.payload) ? a.payload : [a.payload]; s.items = [...added, ...s.items]; })
  .addCase(uploadFile.rejected, (s, a) => { s.error = a.payload; })
  .addCase(deleteFile.fulfilled, (s, a) => { s.items = s.items.filter((i) => Number(i.id) !== Number(a.payload)); })
  .addCase(updateFile.fulfilled, (s, a) => { const i = s.items.findIndex((x) => x.id === a.payload.id); if (i >= 0) s.items[i] = a.payload; })
});
export default fileSlice.reducer;
