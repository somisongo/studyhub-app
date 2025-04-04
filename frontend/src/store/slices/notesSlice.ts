import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

// Types
export interface Note {
  id: string;
  title: string;
  content: string;
  tags: string[];
  course_id?: string;
  creator_id: string;
  created_at: string;
  updated_at?: string;
  version: number;
}

interface NotesState {
  notes: Note[];
  currentNote: Note | null;
  loading: boolean;
  error: string | null;
}

// État initial
const initialState: NotesState = {
  notes: [],
  currentNote: null,
  loading: false,
  error: null,
};

// Thunks
export const fetchNotes = createAsyncThunk(
  'notes/fetchNotes',
  async (_, { rejectWithValue }) => {
    try {
      // Dans une implémentation réelle, appel API pour récupérer les notes
      // Pour le développement, simulez des données
      const notes: Note[] = [
        {
          id: '1',
          title: 'Introduction à React',
          content: 'React est une bibliothèque JavaScript pour construire des interfaces utilisateur.',
          tags: ['react', 'javascript', 'frontend'],
          creator_id: '1',
          created_at: new Date().toISOString(),
          version: 1,
        },
        {
          id: '2',
          title: 'Les bases de TypeScript',
          content: 'TypeScript est un sur-ensemble typé de JavaScript qui compile vers du JavaScript pur.',
          tags: ['typescript', 'javascript', 'programming'],
          creator_id: '1',
          created_at: new Date().toISOString(),
          version: 1,
        },
      ];
      return notes;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Échec du chargement des notes');
    }
  }
);

// Slice
const notesSlice = createSlice({
  name: 'notes',
  initialState,
  reducers: {
    setCurrentNote: (state, action: PayloadAction<Note>) => {
      state.currentNote = action.payload;
    },
    clearCurrentNote: (state) => {
      state.currentNote = null;
    },
    resetNotesError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchNotes.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchNotes.fulfilled, (state, action: PayloadAction<Note[]>) => {
        state.loading = false;
        state.notes = action.payload;
      })
      .addCase(fetchNotes.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { setCurrentNote, clearCurrentNote, resetNotesError } = notesSlice.actions;
export default notesSlice.reducer;
