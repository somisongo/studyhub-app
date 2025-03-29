import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import notesReducer from './slices/notesSlice';
import coursesReducer from './slices/coursesSlice';
import revisionsReducer from './slices/revisionsSlice';
import sharesReducer from './slices/sharesSlice';
import uiReducer from './slices/uiSlice';

// Configure le magasin Redux avec tous les réducteurs
export const store = configureStore({
  reducer: {
    auth: authReducer,
    notes: notesReducer,
    courses: coursesReducer,
    revisions: revisionsReducer,
    shares: sharesReducer,
    ui: uiReducer,
  },
  // Active les outils de développement Redux uniquement en développement
  devTools: process.env.NODE_ENV !== 'production',
});

// Types d'inférence pour useSelector et useDispatch
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
