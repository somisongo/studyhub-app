import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

// Types
export interface Revision {
  id: string;
  note_id: string;
  scheduled_date: string;
  status: 'pending' | 'completed' | 'missed';
  difficulty?: number;
  user_id: string;
  created_at: string;
  completed_at?: string;
  feedback?: string;
}

interface RevisionsState {
  revisions: Revision[];
  upcomingRevisions: Revision[];
  loading: boolean;
  error: string | null;
}

// État initial
const initialState: RevisionsState = {
  revisions: [],
  upcomingRevisions: [],
  loading: false,
  error: null,
};

// Thunks
export const fetchRevisions = createAsyncThunk(
  'revisions/fetchRevisions',
  async (_, { rejectWithValue }) => {
    try {
      // Dans une implémentation réelle, appel API pour récupérer les révisions
      // Pour le développement, simulez des données
      const today = new Date();
      const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);
      
      const revisions: Revision[] = [
        {
          id: '1',
          note_id: '1',
          scheduled_date: today.toISOString(),
          status: 'pending',
          user_id: '1',
          created_at: new Date(today.getTime() - 86400000).toISOString(),
        },
        {
          id: '2',
          note_id: '2',
          scheduled_date: tomorrow.toISOString(),
          status: 'pending',
          user_id: '1',
          created_at: new Date(today.getTime() - 86400000 * 2).toISOString(),
        },
      ];
      return revisions;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Échec du chargement des révisions');
    }
  }
);

export const fetchUpcomingRevisions = createAsyncThunk(
  'revisions/fetchUpcomingRevisions',
  async (days: number = 7, { rejectWithValue }) => {
    try {
      // Dans une implémentation réelle, appel API pour récupérer les révisions à venir
      // Pour le développement, simulez des données
      const today = new Date();
      const revisions: Revision[] = [];
      
      for (let i = 0; i < 5; i++) {
        const scheduledDate = new Date(today);
        scheduledDate.setDate(scheduledDate.getDate() + i);
        
        revisions.push({
          id: `upcoming-${i}`,
          note_id: `${i + 1}`,
          scheduled_date: scheduledDate.toISOString(),
          status: 'pending',
          user_id: '1',
          created_at: new Date(today.getTime() - 86400000).toISOString(),
        });
      }
      
      return revisions;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Échec du chargement des révisions à venir');
    }
  }
);

// Slice
const revisionsSlice = createSlice({
  name: 'revisions',
  initialState,
  reducers: {
    resetRevisionsError: (state) => {
      state.error = null;
    },
    markRevisionAsCompleted: (state, action: PayloadAction<{ id: string, difficulty?: number, feedback?: string }>) => {
      const { id, difficulty, feedback } = action.payload;
      const revision = state.revisions.find(rev => rev.id === id);
      if (revision) {
        revision.status = 'completed';
        revision.completed_at = new Date().toISOString();
        if (difficulty !== undefined) revision.difficulty = difficulty;
        if (feedback) revision.feedback = feedback;
      }
      
      const upcomingRevision = state.upcomingRevisions.find(rev => rev.id === id);
      if (upcomingRevision) {
        upcomingRevision.status = 'completed';
        upcomingRevision.completed_at = new Date().toISOString();
        if (difficulty !== undefined) upcomingRevision.difficulty = difficulty;
        if (feedback) upcomingRevision.feedback = feedback;
      }
    },
    markRevisionAsMissed: (state, action: PayloadAction<string>) => {
      const revision = state.revisions.find(rev => rev.id === action.payload);
      if (revision) {
        revision.status = 'missed';
      }
      
      const upcomingRevision = state.upcomingRevisions.find(rev => rev.id === action.payload);
      if (upcomingRevision) {
        upcomingRevision.status = 'missed';
      }
    },
  },
  extraReducers: (builder) => {
    // Fetch all revisions
    builder
      .addCase(fetchRevisions.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchRevisions.fulfilled, (state, action: PayloadAction<Revision[]>) => {
        state.loading = false;
        state.revisions = action.payload;
      })
      .addCase(fetchRevisions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
    
    // Fetch upcoming revisions
    builder
      .addCase(fetchUpcomingRevisions.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUpcomingRevisions.fulfilled, (state, action: PayloadAction<Revision[]>) => {
        state.loading = false;
        state.upcomingRevisions = action.payload;
      })
      .addCase(fetchUpcomingRevisions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { resetRevisionsError, markRevisionAsCompleted, markRevisionAsMissed } = revisionsSlice.actions;
export default revisionsSlice.reducer;
