import { writable } from 'svelte/store';

export interface QuizResult {
  moduleId: string;
  score: number;
  passed: boolean;
  timeSpent: number;
  completedAt: Date;
  answers: (number | null)[];
}

export interface QuizProgress {
  [moduleId: string]: {
    completed: boolean;
    bestScore: number;
    attempts: number;
    lastAttempt?: Date;
  };
}

function createQuizStore() {
  const { subscribe, set, update } = writable<{
    results: QuizResult[];
    progress: QuizProgress;
  }>({
    results: [],
    progress: {}
  });

  return {
    subscribe,
    
    // Record a quiz result
    recordResult: (result: QuizResult) => {
      update(state => {
        const newResults = [...state.results, result];
        const moduleProgress = state.progress[result.moduleId] || {
          completed: false,
          bestScore: 0,
          attempts: 0
        };
        
        const newProgress = {
          ...state.progress,
          [result.moduleId]: {
            completed: result.passed,
            bestScore: Math.max(moduleProgress.bestScore, result.score),
            attempts: moduleProgress.attempts + 1,
            lastAttempt: result.completedAt
          }
        };
        
        return {
          results: newResults,
          progress: newProgress
        };
      });
    },
    
    // Get progress for a specific module
    getModuleProgress: (moduleId: string) => {
      let currentState: any;
      subscribe(state => currentState = state)();
      return currentState.progress[moduleId] || {
        completed: false,
        bestScore: 0,
        attempts: 0
      };
    },
    
    // Check if a module is completed
    isModuleCompleted: (moduleId: string) => {
      let currentState: any;
      subscribe(state => currentState = state)();
      return currentState.progress[moduleId]?.completed || false;
    },
    
    // Get all completed modules
    getCompletedModules: () => {
      let currentState: any;
      subscribe(state => currentState = state)();
      return Object.keys(currentState.progress).filter(
        moduleId => currentState.progress[moduleId].completed
      );
    },
    
    // Reset all progress
    resetProgress: () => {
      set({
        results: [],
        progress: {}
      });
    },
    
    // Reset progress for a specific module
    resetModuleProgress: (moduleId: string) => {
      update(state => {
        const newProgress = { ...state.progress };
        delete newProgress[moduleId];
        return {
          ...state,
          progress: newProgress
        };
      });
    }
  };
}

export const quizStore = createQuizStore(); 