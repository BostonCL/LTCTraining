import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export interface ProgressState {
  // Introduction
  introduction: boolean;
  
  // Module 1
  module1_intro: boolean;
  module1_programline: boolean;
  module1_starttimerealtime: boolean;
  module1_starttimerealtime_quiz: boolean;
  module1_hittime: boolean;
  module1_eventtype: boolean;
  module1_length: boolean;
  module1_length_quiz: boolean;
  module1_title: boolean;
  module1_advertiser: boolean;
  module1_housenumber: boolean;
  module1_housenumber_quiz: boolean;
  module1_orderedas: boolean;
  module1_spotendtime: boolean;
  module1_endtime: boolean;
  module1_floaters: boolean;
  module1_keytab: boolean;
  module1_test: boolean;
  
  // Module 2
  module2_intro: boolean;
  module2_sellingtitle: boolean;
  module2_yellowunit: boolean;
  module2_unitprioritizationdetails: boolean;
  module2_greenpurpleunits: boolean;
  module2_test: boolean;
  
  // Module 3
  module3_intro: boolean;
  module3_brandsep: boolean;
  module3_advertiserconflicts: boolean;
  module3_standalonerule: boolean;
  module3_commercialtimes: boolean;
  module3_swaps: boolean;
  module3_mastercontrolemail: boolean;
  module3_localswaps: boolean;
  module3_excelsheet: boolean;
  module3_unitcutpractice: boolean;
  module3_mcemailpractice: boolean;
  module3_timeoutpractice: boolean;
  
  // Final Exam
  finalexam: boolean;
}

const STORAGE_KEY = 'ltc_training_progress';

// Default progress state - everything locked except introduction
const defaultProgress: ProgressState = {
  introduction: false,
  
  module1_intro: false,
  module1_programline: false,
  module1_starttimerealtime: false,
  module1_starttimerealtime_quiz: false,
  module1_hittime: false,
  module1_eventtype: false,
  module1_length: false,
  module1_length_quiz: false,
  module1_title: false,
  module1_advertiser: false,
  module1_housenumber: false,
  module1_housenumber_quiz: false,
  module1_orderedas: false,
  module1_spotendtime: false,
  module1_endtime: false,
  module1_floaters: false,
  module1_keytab: false,
  module1_test: false,
  
  module2_intro: false,
  module2_sellingtitle: false,
  module2_yellowunit: false,
  module2_unitprioritizationdetails: false,
  module2_greenpurpleunits: false,
  module2_test: false,
  
  module3_intro: false,
  module3_brandsep: false,
  module3_advertiserconflicts: false,
  module3_standalonerule: false,
  module3_commercialtimes: false,
  module3_swaps: false,
  module3_mastercontrolemail: false,
  module3_localswaps: false,
  module3_excelsheet: false,
  module3_unitcutpractice: false,
  module3_mcemailpractice: false,
  module3_timeoutpractice: false,
  
  finalexam: false
};

// Load progress from localStorage
function loadProgress(): ProgressState {
  if (browser) {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const loadedProgress = { ...defaultProgress, ...JSON.parse(stored) };
        console.log('📂 Progress Store: Loaded from localStorage:', loadedProgress);
        return loadedProgress;
      }
    } catch (e) {
      console.error('Failed to load progress from localStorage:', e);
    }
  }
  console.log('📂 Progress Store: Using default progress (fresh start)');
  return defaultProgress;
}

// Save progress to localStorage
function saveProgress(progress: ProgressState) {
  if (browser) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
      console.log('💾 Progress Store: Saved to localStorage:', progress);
    } catch (e) {
      console.error('Failed to save progress to localStorage:', e);
    }
  }
}

function createProgressStore() {
  const { subscribe, set, update } = writable<ProgressState>(loadProgress());

  return {
    subscribe,
    
    // Mark a slide/module as completed
    markCompleted: (key: keyof ProgressState) => {
      console.log('✅ Progress: Marking as completed:', key);
      update(state => {
        const newState = { ...state, [key]: true };
        saveProgress(newState);
        console.log('✅ Progress: Updated state for', key, '- New state:', newState);
        return newState;
      });
    },
    
    // Check if a slide/module is completed
    isCompleted: (key: keyof ProgressState, currentState: ProgressState) => {
      return currentState[key] || false;
    },
    
    // Check if a slide/module is unlocked (can be accessed)
    isUnlocked: (key: keyof ProgressState, currentState: ProgressState) => {
      // Introduction is always unlocked
      if (key === 'introduction') return true;
      
      // Define the progression order
      const progressionOrder: (keyof ProgressState)[] = [
        'introduction',
        'module1_intro',
        'module1_programline',
        'module1_starttimerealtime',
        'module1_starttimerealtime_quiz',
        'module1_hittime',
        'module1_eventtype',
        'module1_length',
        'module1_length_quiz',
        'module1_title',
        'module1_advertiser',
        'module1_housenumber',
        'module1_housenumber_quiz',
        'module1_orderedas',
        'module1_spotendtime',
        'module1_endtime',
        'module1_floaters',
        'module1_keytab',
        'module1_test',
        'module2_intro',
        'module2_sellingtitle',
        'module2_yellowunit',
        'module2_unitprioritizationdetails',
        'module2_greenpurpleunits',
        'module2_test',
        'module3_intro',
        'module3_brandsep',
        'module3_advertiserconflicts',
        'module3_standalonerule',
        'module3_commercialtimes',
        'module3_swaps',
        'module3_mastercontrolemail',
        'module3_localswaps',
        'module3_excelsheet',
        'module3_unitcutpractice',
        'module3_mcemailpractice',
        'module3_timeoutpractice',
        'finalexam'
      ];
      
      const currentIndex = progressionOrder.indexOf(key);
      if (currentIndex === -1) return false;
      
      // Check if all previous items are completed
      for (let i = 0; i < currentIndex; i++) {
        if (!currentState[progressionOrder[i]]) {
          return false;
        }
      }
      
      return true;
    },
    
    // Get the next unlocked slide/module
    getNextUnlocked: (currentState: ProgressState): keyof ProgressState | null => {
      const progressionOrder: (keyof ProgressState)[] = [
        'introduction',
        'module1_intro',
        'module1_programline',
        'module1_starttimerealtime',
        'module1_starttimerealtime_quiz',
        'module1_hittime',
        'module1_eventtype',
        'module1_length',
        'module1_length_quiz',
        'module1_title',
        'module1_advertiser',
        'module1_housenumber',
        'module1_housenumber_quiz',
        'module1_orderedas',
        'module1_spotendtime',
        'module1_endtime',
        'module1_floaters',
        'module1_keytab',
        'module1_test',
        'module2_intro',
        'module2_sellingtitle',
        'module2_yellowunit',
        'module2_unitprioritizationdetails',
        'module2_greenpurpleunits',
        'module2_test',
        'module3_intro',
        'module3_brandsep',
        'module3_advertiserconflicts',
        'module3_standalonerule',
        'module3_commercialtimes',
        'module3_swaps',
        'module3_mastercontrolemail',
        'module3_localswaps',
        'module3_excelsheet',
        'module3_unitcutpractice',
        'module3_mcemailpractice',
        'module3_timeoutpractice',
        'finalexam'
      ];
      
      for (const item of progressionOrder) {
        if (!currentState[item]) {
          return item;
        }
      }
      
      return null; // All completed
    },
    
    // Reset all progress
    reset: () => {
      set(defaultProgress);
      saveProgress(defaultProgress);
    },
    
    // Reset progress for a specific module (for testing/debugging)
    resetModule: (modulePrefix: string) => {
      update(state => {
        const newState = { ...state };
        Object.keys(newState).forEach(key => {
          if (key.startsWith(modulePrefix)) {
            (newState as any)[key] = false;
          }
        });
        saveProgress(newState);
        return newState;
      });
    }
  };
}

export const progressStore = createProgressStore();



