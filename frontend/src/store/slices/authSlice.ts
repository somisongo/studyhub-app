import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import axios from 'axios';
import jwtDecode from 'jwt-decode';

// Types
interface User {
  id: string;
  name: string;
  email: string;
  is_active: boolean;
  is_superuser: boolean;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
  token: string | null;
}

interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterCredentials {
  name: string;
  email: string;
  password: string;
}

interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// Actions asynchrones
export const login = createAsyncThunk(
  'auth/login',
  async (credentials: LoginCredentials, { rejectWithValue }) => {
    try {
      const formData = new FormData();
      formData.append('username', credentials.email); // API utilise 'username' mais nous utilisons 'email'
      formData.append('password', credentials.password);

      const response = await axios.post<AuthResponse>(
        '/api/v1/auth/token',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      // Stockage des tokens dans localStorage
      localStorage.setItem('accessToken', response.data.access_token);
      localStorage.setItem('refreshToken', response.data.refresh_token);

      // Configuration d'Axios pour inclure le token dans les futures requêtes
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;

      // Décodage du token pour obtenir les informations utilisateur
      const decodedToken = jwtDecode<{ sub: string }>(response.data.access_token);
      const userResponse = await axios.get<User>(`/api/v1/users/${decodedToken.sub}`);

      return {
        user: userResponse.data,
        token: response.data.access_token,
      };
    } catch (error: any) {
      return rejectWithValue(
        error.response?.data?.detail || 'Erreur lors de la connexion'
      );
    }
  }
);

export const register = createAsyncThunk(
  'auth/register',
  async (credentials: RegisterCredentials, { rejectWithValue, dispatch }) => {
    try {
      // Enregistrement de l'utilisateur
      await axios.post('/api/v1/auth/register', credentials);

      // Connexion automatique après enregistrement
      const loginResult = await dispatch(
        login({ email: credentials.email, password: credentials.password })
      );

      // Si la connexion échoue, rejeter l'enregistrement
      if (login.rejected.match(loginResult)) {
        return rejectWithValue(loginResult.payload || 'Erreur lors de la connexion après enregistrement');
      }

      return loginResult.payload;
    } catch (error: any) {
      return rejectWithValue(
        error.response?.data?.detail || 'Erreur lors de l\'enregistrement'
      );
    }
  }
);

export const logout = createAsyncThunk('auth/logout', async () => {
  // Suppression des tokens du localStorage
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');

  // Suppression du token d'authorization dans Axios
  delete axios.defaults.headers.common['Authorization'];
});

export const checkAuth = createAsyncThunk(
  'auth/checkAuth',
  async (_, { rejectWithValue, dispatch }) => {
    // Récupération du token depuis localStorage
    const token = localStorage.getItem('accessToken');
    const refreshToken = localStorage.getItem('refreshToken');

    if (!token || !refreshToken) {
      return rejectWithValue('Non authentifié');
    }

    try {
      // Configuration d'Axios pour inclure le token
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

      // Vérification de la validité du token en récupérant l'utilisateur
      const decodedToken = jwtDecode<{ sub: string; exp: number }>(token);

      // Vérification de l'expiration du token
      const isExpired = decodedToken.exp * 1000 < Date.now();

      if (isExpired) {
        // Rafraîchissement du token
        try {
          const response = await axios.post<AuthResponse>('/api/v1/auth/refresh', {
            refresh_token: refreshToken,
          });

          localStorage.setItem('accessToken', response.data.access_token);
          localStorage.setItem('refreshToken', response.data.refresh_token);
          axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`;

          // Récupération des informations utilisateur
          const userResponse = await axios.get<User>(`/api/v1/users/${decodedToken.sub}`);

          return {
            user: userResponse.data,
            token: response.data.access_token,
          };
        } catch (refreshError) {
          // Si le rafraîchissement échoue, déconnexion
          dispatch(logout());
          return rejectWithValue('Session expirée');
        }
      }

      // Récupération des informations utilisateur
      const userResponse = await axios.get<User>(`/api/v1/users/${decodedToken.sub}`);

      return {
        user: userResponse.data,
        token,
      };
    } catch (error) {
      // En cas d'erreur, déconnexion
      dispatch(logout());
      return rejectWithValue('Erreur d\'authentification');
    }
  }
);

// État initial
const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  loading: false,
  error: null,
  token: null,
};

// Slice
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    // Autres réducteurs si nécessaire
  },
  extraReducers: (builder) => {
    builder
      // Login
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
      })
      // Register
      .addCase(register.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(register.fulfilled, (state, action: PayloadAction<any>) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.user = action.payload?.user;
        state.token = action.payload?.token;
      })
      .addCase(register.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      })
      // Logout
      .addCase(logout.fulfilled, (state) => {
        state.user = null;
        state.isAuthenticated = false;
        state.token = null;
      })
      // Check Auth
      .addCase(checkAuth.pending, (state) => {
        state.loading = true;
      })
      .addCase(checkAuth.fulfilled, (state, action: PayloadAction<{ user: User; token: string }>) => {
        state.loading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.token = action.payload.token;
      })
      .addCase(checkAuth.rejected, (state) => {
        state.loading = false;
        state.isAuthenticated = false;
        state.user = null;
        state.token = null;
      });
  },
});

export const { clearError } = authSlice.actions;

export default authSlice.reducer;
