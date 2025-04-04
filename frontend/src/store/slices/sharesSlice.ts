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
  async (activeOnly: boolean = true, { rejectWithValue }) => {
    try {
      // Dans une implémentation réelle, appel API pour récupérer les partages
      // Pour le développement, simulez des données
      const shares: Share[] = [
        {
          id: '1',
          note_id: '1',
          permissions: 'read',
          target_email: 'colleague@example.com',
          source_user_id: '1',
          created_at: new Date().toISOString(),
          active: true,
        },
        {
          id: '2',
          note_id: '2',
          permissions: 'edit',
          target_email: 'friend@example.com',
          source_user_id: '1',
          created_at: new Date().toISOString(),
          active: true,
        },
      ];
      
      return shares.filter(share => !activeOnly || share.active);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Échec du chargement des partages');
    }
  }
);

export const fetchSharedWithMe = createAsyncThunk(
  'shares/fetchSharedWithMe',
  async (activeOnly: boolean = true, { rejectWithValue }) => {
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
      
      return shares.filter(share => !activeOnly || share.active);
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
    deactivateShare: (state, action: PayloadAction<string>) => {
      const shareId = action.payload;
      
      const sharedByMeIndex = state.sharedByMe.findIndex(share => share.id === shareId);
      if (sharedByMeIndex !== -1) {
        state.sharedByMe[sharedByMeIndex].active = false;
      }
      
      const sharedWithMeIndex = state.sharedWithMe.findIndex(share => share.id === shareId);
      if (sharedWithMeIndex !== -1) {
        state.sharedWithMe[sharedWithMeIndex].active = false;
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

export const { resetSharesError, deactivateShare } = sharesSlice.actions;
export default sharesSlice.reducer;
