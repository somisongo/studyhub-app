import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import axios from 'axios';

// Types
interface User {
  id: string;
  name: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
}

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  loading: boolean;
  error: string | null;
  token: string | null;
}

// État initial
const initialState: AuthState = {
  isAuthenticated: false,
  user: null,
  loading: false,
  error: null,
  token: localStorage.getItem('token'),
};

// Thunks
export const login = createAsyncThunk(
  'auth/login',
  async ({ email, password }: { email: string; password: string }, { rejectWithValue }) => {
    try {
      // Dans une implémentation réelle, appel API pour la connexion
      // Présentement, simulez une connexion réussie en développement
      const user = {
        id: '1',
        name: 'Utilisateur Test',
        email,
        is_active: true,
        is_superuser: false,
      };
      const token = 'fake-jwt-token';
      localStorage.setItem('token', token);
      return { user, token };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Échec de connexion');
    }
  }
);

export const register = createAsyncThunk(
  'auth/register',
  async ({ name, email, password }: { name: string; email: string; password: string }, { rejectWithValue }) => {
    try {
      // Dans une implémentation réelle, appel API pour l'inscription
      // Présentement, simulez une inscription réussie en développement
      return { message: 'Inscription réussie' };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Échec d\'inscription');
    }
  }
);

export const logout = createAsyncThunk(
  'auth/logout',
  async (_, { rejectWithValue }) => {
    try {
      // Supprimer le token du stockage local
      localStorage.removeItem('token');
      return null;
    } catch (error: any) {
      return rejectWithValue(error.message || 'Échec de déconnexion');
    }
  }
);

export const checkAuth = createAsyncThunk(
  'auth/checkAuth',
  async (_, { rejectWithValue }) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        return null;
      }
      
      // Dans une implémentation réelle, vérifiez le token auprès du serveur
      // Pour le développement, simulez un utilisateur authentifié
      const user = {
        id: '1',
        name: 'Utilisateur Test',
        email: 'test@example.com',
        is_active: true,
        is_superuser: false,
      };
      return { user, token };
    } catch (error: any) {
      return rejectWithValue('Session expirée ou invalide');
    }
  }
);

// Slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    resetError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    // Login
    builder
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action: PayloadAction<{ user: User; token: string }>) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.token = action.payload.token;
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });

    // Register
    builder
      .addCase(register.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(register.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(register.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });

    // Logout
    builder
      .addCase(logout.fulfilled, (state) => {
        state.isAuthenticated = false;
        state.user = null;
        state.token = null;
      });

    // Check Auth
    builder
      .addCase(checkAuth.pending, (state) => {
        state.loading = true;
      })
      .addCase(checkAuth.fulfilled, (state, action) => {
        state.loading = false;
        if (action.payload) {
          state.isAuthenticated = true;
          state.user = action.payload.user;
          state.token = action.payload.token;
        } else {
          state.isAuthenticated = false;
          state.user = null;
          state.token = null;
        }
      })
      .addCase(checkAuth.rejected, (state) => {
        state.loading = false;
        state.isAuthenticated = false;
        state.user = null;
        state.token = null;
      });
  },
});

export const { resetError } = authSlice.actions;
export default authSlice.reducer;
