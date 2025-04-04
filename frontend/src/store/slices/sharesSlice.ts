import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

// Types
export interface Share {
  id: string;
  note_id: string;
  permissions: 'read' | 'edit';
  target_email?: string;
  target_user_id?: string;
  expiration_date?: string;
  message?: string;
  source_user_id: string;
  created_at: string;
  active: boolean;
}

interface SharesState {
  sharedByMe: Share[];
  sharedWithMe: Share[];
  loading: boolean;
  error: string | null;
}

// État initial
const initialState: SharesState = {
  sharedByMe: [],
  sharedWithMe: [],
  loading: false,
  error: null,
};

// Thunks
export const fetchSharedByMe = createAsyncThunk(
  'shares/fetchSharedByMe',
  async (_, { rejectWithValue }) => {
    try {
      // Dans une implémentation réelle, appel API pour récupérer les partages
      // Pour le développement, simulez des données
      const shares: Share[] = [
        {
          id: '1',
          note_id: '1',
          permissions: 'read',
          target_email: 'collaborator@example.com',
          source_user_id: '1',
          created_at: new Date().toISOString(),
          active: true,
        },
        {
          id: '2',
          note_id: '2',
          permissions: 'edit',
          target_email: 'teacher@example.com',
          source_user_id: '1',
          created_at: new Date().toISOString(),
          active: true,
        },
      ];
      return shares;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Échec du chargement des partages');
    }
  }
);

export const fetchSharedWithMe = createAsyncThunk(
  'shares/fetchSharedWithMe',
  async (_, { rejectWithValue }) => {
    try {
      // Dans une implémentation réelle, appel API pour récupérer les partages
      // Pour le développement, simulez des données
      const shares: Share[] = [
        {
          id: '3',
          note_id: '3',
          permissions: 'read',
          target_user_id: '1',
          source_user_id: '2',
          created_at: new Date().toISOString(),
          active: true,
        },
        {
          id: '4',
          note_id: '4',
          permissions: 'edit',
          target_user_id: '1',
          source_user_id: '3',
          created_at: new Date().toISOString(),
          active: true,
        },
      ];
      return shares;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Échec du chargement des partages');
    }
  }
);

// Slice
const sharesSlice = createSlice({
  name: 'shares',
  initialState,
  reducers: {
    resetSharesError: (state) => {
      state.error = null;
    },
    updateShareStatus: (state, action: PayloadAction<{ id: string; active: boolean }>) => {
      const { id, active } = action.payload;
      const share = state.sharedByMe.find(s => s.id === id);
      if (share) {
        share.active = active;
      }
    },
  },
  extraReducers: (builder) => {
    // Fetch shares by me
    builder
      .addCase(fetchSharedByMe.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSharedByMe.fulfilled, (state, action: PayloadAction<Share[]>) => {
        state.loading = false;
        state.sharedByMe = action.payload;
      })
      .addCase(fetchSharedByMe.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
    
    // Fetch shares with me
    builder
      .addCase(fetchSharedWithMe.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSharedWithMe.fulfilled, (state, action: PayloadAction<Share[]>) => {
        state.loading = false;
        state.sharedWithMe = action.payload;
      })
      .addCase(fetchSharedWithMe.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { resetSharesError, updateShareStatus } = sharesSlice.actions;
export default sharesSlice.reducer;
