import { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box, CircularProgress } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';

import Dashboard from '@pages/Dashboard';
import Login from '@pages/auth/Login';
import Register from '@pages/auth/Register';
import NotesPage from '@pages/notes/NotesPage';
import NoteEditor from '@pages/notes/NoteEditor';
import NoteView from '@pages/notes/NoteView';
import CoursesPage from '@pages/courses/CoursesPage';
import CourseView from '@pages/courses/CourseView';
import RevisionsPage from '@pages/revisions/RevisionsPage';
import SettingsPage from '@pages/settings/SettingsPage';
import Layout from '@components/layout/Layout';
import ProfilePage from '@pages/profile/ProfilePage';
import SharedWithMePage from '@pages/shared/SharedWithMePage';

import { AppDispatch, RootState } from '@store/index';
import { checkAuth } from '@store/slices/authSlice';

// Route protégée qui vérifie l'authentification
const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const { isAuthenticated, loading } = useSelector((state: RootState) => state.auth);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return children;
};

const App = () => {
  const dispatch = useDispatch<AppDispatch>();

  // Vérifier l'authentification au chargement
  useEffect(() => {
    dispatch(checkAuth());
  }, [dispatch]);

  return (
    <Routes>
      {/* Routes publiques */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      
      {/* Routes protégées */}
      <Route path="/" element={
        <ProtectedRoute>
          <Layout />
        </ProtectedRoute>
      }>
        <Route index element={<Dashboard />} />
        <Route path="notes" element={<NotesPage />} />
        <Route path="notes/new" element={<NoteEditor />} />
        <Route path="notes/:id" element={<NoteView />} />
        <Route path="notes/:id/edit" element={<NoteEditor />} />
        <Route path="courses" element={<CoursesPage />} />
        <Route path="courses/:id" element={<CourseView />} />
        <Route path="revisions" element={<RevisionsPage />} />
        <Route path="shared" element={<SharedWithMePage />} />
        <Route path="profile" element={<ProfilePage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>
      
      {/* Route de fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default App;
