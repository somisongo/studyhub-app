import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

// Types
export interface Course {
  id: string;
  name: string;
  description?: string;
  tags: string[];
  color?: string;
  icon?: string;
  user_id: string;
  created_at: string;
  updated_at?: string;
}

interface CoursesState {
  courses: Course[];
  currentCourse: Course | null;
  loading: boolean;
  error: string | null;
}

// État initial
const initialState: CoursesState = {
  courses: [],
  currentCourse: null,
  loading: false,
  error: null,
};

// Thunks
export const fetchCourses = createAsyncThunk(
  'courses/fetchCourses',
  async (_, { rejectWithValue }) => {
    try {
      // Dans une implémentation réelle, appel API pour récupérer les cours
      // Pour le développement, simulez des données
      const courses: Course[] = [
        {
          id: '1',
          name: 'Développement Web Frontend',
          description: 'Apprentissage des technologies web modernes côté client',
          tags: ['web', 'frontend', 'javascript'],
          color: '#4287f5',
          icon: 'code',
          user_id: '1',
          created_at: new Date().toISOString(),
        },
        {
          id: '2',
          name: 'Intelligence Artificielle',
          description: 'Introduction aux concepts fondamentaux de l\'IA',
          tags: ['ai', 'machine-learning', 'computer-science'],
          color: '#42f5b3',
          icon: 'psychology',
          user_id: '1',
          created_at: new Date().toISOString(),
        },
      ];
      return courses;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.message || 'Échec du chargement des cours');
    }
  }
);

// Slice
const coursesSlice = createSlice({
  name: 'courses',
  initialState,
  reducers: {
    setCurrentCourse: (state, action: PayloadAction<Course>) => {
      state.currentCourse = action.payload;
    },
    clearCurrentCourse: (state) => {
      state.currentCourse = null;
    },
    resetCoursesError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchCourses.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCourses.fulfilled, (state, action: PayloadAction<Course[]>) => {
        state.loading = false;
        state.courses = action.payload;
      })
      .addCase(fetchCourses.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload as string;
      });
  },
});

export const { setCurrentCourse, clearCurrentCourse, resetCoursesError } = coursesSlice.actions;
export default coursesSlice.reducer;
