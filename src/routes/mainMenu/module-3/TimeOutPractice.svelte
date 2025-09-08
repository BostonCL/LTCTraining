<script lang="ts">
import { onMount } from 'svelte';
import Handsontable from 'handsontable';
import 'handsontable/dist/handsontable.full.min.css';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

let container: HTMLDivElement;
let hot: Handsontable | null = null;

let data = [
  ["Real Time 08:00:00 PM", "Hit Time", "Event Type", "Length", "Title", "Advertiser", "House Number", "Ordered As", "Spot End Time"],
  ["Start Time 08:00:00 PM", "08:00:00 PM", "Program", "00:45:00", "USL P1 [USL: First Round Match TBD - 11/3/24_8p]: SEG. 5", "", "327335", "", ""],
  ["09:34:27 PM", "09:35:00 PM", "Commercial", "00:00:15", "PEPSI (MOUNTAIN DEW): MTD T&R BAJA :15", "PEPSI", "600701", "ROS 24 HOUR", "05:59:00 AM"],
  ["", "09:35:15 PM", "Commercial", "00:00:30", "DRAFT KINGS: *NFL APPROVED* DRAFTKINGS / TD CELEBRATION ALL SB STATES BET 5 GET 200 LINEAR 1 - CBS + ESPN / QUARTER", "DRAFT KINGS", "600544", "STUDIO ENCORE", "05:59:00 AM"],
  ["", "09:35:45 PM", "Commercial", "00:00:30", "VERIZON: NPI202430S6X9SUSTAIN IPHONE 16 PRO IPADCCNC", "VERIZON", "601337", "STUDIO ENCORE", "05:59:00 AM"],
  ["", "09:36:15 PM", "Commercial", "00:00:15", "STANLEY STEEMER: AD EXPERT V2-15", "STANLEY STEEMER", "601124", "UNITED SOCCER LEAGUE", "05:59:00 AM"],
  ["", "09:36:30 PM", "Local", "Local", "Local", "Local", "Local", "Local", "Local"],
  ["", "09:38:00 PM", "Program", "00:17:30", "USL P1 [USL: First Round Match TBD - 11/3/24_8p]: SEG. 6", "", "327336", "", ""],
  ["09:58:14 PM", "09:55:30 PM", "Promo", "00:00:20", "UEFA MD4 THURSDAY", "CBS SPORTS NETWORK", "801865", "", ""],
  ["", "09:55:50 PM", "Commercial", "00:00:30", "UNITED SOCCER LEAGUE: CH_PLAYOFF_HYPE_24", "United Soccer League", "601582", "UNITED SOCCER LEAGUE", "10:00:00 PM"],
  ["", "09:56:20 PM", "Commercial", "00:00:30", "STELLANTIS: BLESSED/JDP/THE CALLING/RAM/TUNGSTEN/NATIONAL/30/25 RAM 1500 4,000/PD 20/PUBLIS/NOV24", "STELLANTIS", "601703", "STUDIO ENCORE", "05:59:00 AM"],
  ["", "09:56:50 PM", "Commercial", "00:00:30", "DR PEPPER: CFB 2024 LONG DISTANCE RIVALRY :30", "DR PEPPER", "600682", "STUDIO ENCORE", "05:59:00 AM"],
  ["", "09:57:20 PM", "Commercial", "00:00:30", "JAMRS: ADVENTURE :30", "JAMRS", "607010", "STUDIO ENCORE", "05:59:00 AM"],
  ["End Time 10:02:00", "09:57:50 PM", "Promo", "00:00:10", "NATIVE AMERICAN GENERIC 23", "CBS SPORTS NETWORK", "806035", "", ""],
  ["", "", "", "", "", "", "", "", ""],
  ["Start Time", "10:00:00 PM", "Program", "00:06:30", "Volleyball Special Event R5 [AVP Beach Volleyball: AVP League - Week 8]: SEG. 1", "", "327341", "", ""],
  ["", "10:06:30 PM", "Promo", "00:00:10", "INSIDE COLLEGE FOOTBALL TUES", "CBS SPORTS NETWORK", "801070", "", ""],
  ["", "10:06:40 PM", "National DR", "00:00:30", "NIC INDUSTRIES: CERAKOTE HEADLIGHT RESTORATION DRIVE TO RETAIL", "NIC INDUSTRIES", "600103", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:07:10 PM", "National DR", "00:00:30", "GRAINGER: THE BAKER II GRAG 30", "GRAINGER", "607123", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:08:00 PM", "Program", "00:06:00", "Volleyball Special Event R5 [AVP Beach Volleyball: AVP League - Week 8]: SEG. 2", "", "327342", "", ""],
  ["", "10:14:00 PM", "National DR", "00:00:15", "TRUST & WILL: MEET TRUST AND WILL II 30", "TRUST & WILL", "604177", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:14:30 PM", "National DR", "00:00:05", "DEALDASH, INC: DD REAL DEALS 2023 NEW TESTIMONIAL :30/DEALDASH.COM", "DEALDASH, INC", "607056", "DR ROS PRIME", "12:00:00 AM"],
  ["", "10:15:00 PM", "Local", "Local", "Local", "Local", "Local", "Local", "Local"],
  ["", "10:16:30 PM", "Program", "00:07:00", "Volleyball Special Event R5 [AVP Beach Volleyball: AVP League - Week 8]: SEG. 3", "", "327343", "", ""],
  ["", "10:23:30 PM", "National DR", "00:01:00", "BOSLEY: NOT 1970 QR 60", "BOSLEY", "606670", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:24:30 PM", "National DR", "00:00:05", "MIZUHO AMERICAS: MWW MIZUHO AMERICAS PAR 3", "MIZUHO AMERICAS", "600884", "DR 24 HOUR ROS", "11:59:00 PM"],
  ["", "10:25:00 PM", "Program", "00:09:30", "Volleyball Special Event R5 [AVP Beach Volleyball: AVP League - Week 8]: SEG. 4", "", "327344", "", ""]
];

let selectedColor = '#FF0000'; // Default red
let showColorPicker = false;
let cellColors: { [key: string]: string } = {};
let clearedCells = new Set<string>();

// --- Step-based instructions state ---
let showStep1 = false;
let showStep2 = false;
let intro = true;

function goToStep1() {
  showStep1 = true;
  showStep2 = false;
  intro = false;
}

function goToStep2() {
  showStep2 = true;
  showStep1 = false;
  intro = false;
}

function goBackIntro() {
  intro = true;
  showStep1 = false;
  showStep2 = false;
}

// --- Step check state ---
let checkResult1 = '';
let checkResult2 = '';

// Congratulations state
let showCongratulations = false;

function showCongratulationsCard() {
  showCongratulations = true;
}

// Developer mode toggle
let developerMode = false;

function toggleDeveloperMode() {
  developerMode = !developerMode;
}

function checkStep1() {
  if (developerMode) {
    checkResult1 = '🔧 DEV MODE: Step 1 automatically passed!';
    setTimeout(() => { goToStep2(); }, 800);
    return;
  }
  
  // Find the three National DR rows that add up to 2 minutes total
  const nicIndustriesIdx = data.findIndex(row => row[1] === '10:06:40 PM' && row[2] && row[2].toLowerCase() === 'national dr' && row[4] && row[4].toLowerCase().includes('nic industries'));
  const graingerIdx = data.findIndex(row => row[1] === '10:07:10 PM' && row[2] && row[2].toLowerCase() === 'national dr' && row[4] && row[4].toLowerCase().includes('grainger'));
  const bosleyIdx = data.findIndex(row => row[1] === '10:23:30 PM' && row[2] && row[2].toLowerCase() === 'national dr' && row[4] && row[4].toLowerCase().includes('bosley'));
  
  let nicIndustriesCut = false, nicIndustriesRed = false;
  let graingerCut = false, graingerRed = false;
  let bosleyCut = false, bosleyRed = false;
  
  // Check NIC INDUSTRIES row (30 seconds)
  if (nicIndustriesIdx !== -1) {
    nicIndustriesCut = typeof data[nicIndustriesIdx][0] === 'string' && data[nicIndustriesIdx][0].trim().toLowerCase() === 'cut';
    // Check if all columns except A are filled red
    let allRed = true;
    for (let col = 1; col < data[nicIndustriesIdx].length; col++) {
      const cellKey = `${nicIndustriesIdx}-${col}`;
      const color = (cellColors[cellKey] || '').toLowerCase();
      if (color !== '#e53e3e' && color !== '#ff0000' && color !== 'rgb(229,62,62)' && color !== 'rgb(255,0,0)') {
        allRed = false;
        break;
      }
    }
    nicIndustriesRed = allRed;
  }
  
  // Check GRAINGER row (30 seconds)
  if (graingerIdx !== -1) {
    graingerCut = typeof data[graingerIdx][0] === 'string' && data[graingerIdx][0].trim().toLowerCase() === 'cut';
    // Check if all columns except A are filled red
    let allRed = true;
    for (let col = 1; col < data[graingerIdx].length; col++) {
      const cellKey = `${graingerIdx}-${col}`;
      const color = (cellColors[cellKey] || '').toLowerCase();
      if (color !== '#e53e3e' && color !== '#ff0000' && color !== 'rgb(229,62,62)' && color !== 'rgb(255,0,0)') {
        allRed = false;
        break;
      }
    }
    graingerRed = allRed;
  }
  
  // Check BOSLEY row (1 minute)
  if (bosleyIdx !== -1) {
    bosleyCut = typeof data[bosleyIdx][0] === 'string' && data[bosleyIdx][0].trim().toLowerCase() === 'cut';
    // Check if all columns except A are filled red
    let allRed = true;
    for (let col = 1; col < data[bosleyIdx].length; col++) {
      const cellKey = `${bosleyIdx}-${col}`;
      const color = (cellColors[cellKey] || '').toLowerCase();
      if (color !== '#e53e3e' && color !== '#ff0000' && color !== 'rgb(229,62,62)' && color !== 'rgb(255,0,0)') {
        allRed = false;
        break;
      }
    }
    bosleyRed = allRed;
  }
  
  if (nicIndustriesCut && nicIndustriesRed && graingerCut && graingerRed && bosleyCut && bosleyRed) {
    checkResult1 = '✅ Correct! You CUT 2:00 minutes of inventory.';
  } else {
    checkResult1 = '❌ Not quite! You need to CUT 2 minutes total. Find the NIC INDUSTRIES (30s), GRAINGER (30s), and BOSLEY (1:00) National DR rows, write "CUT" in column A, and fill all other columns red.';
  }
}

let emailText = '';

function checkStep2() {
  if (developerMode) {
    checkResult2 = '🔧 DEV MODE: Step 2 automatically passed!';
    setTimeout(() => { showCongratulationsCard(); }, 800);
    return;
  }
  
  // Check if user has written email text
  if (emailText.trim().length > 0) {
    checkResult2 = '✅ Good Job! Now, check your own work in the reference email box.';
  } else {
    checkResult2 = '❌ Please write a detailed email to Master Control explaining the cuts you made to save 2 minutes.';
  }
}

function pickColor(color: string) {
  selectedColor = color;
  showColorPicker = false;
  applyFillColor();
}

function applyFillColor() {
  if (hot) {
    const selected = hot.getSelected();
    if (selected && selected.length > 0) {
      selected.forEach(range => {
        const startRow = Math.min(range[0], range[2]);
        const endRow = Math.max(range[0], range[2]);
        const startCol = Math.min(range[1], range[3]);
        const endCol = Math.max(range[1], range[3]);
        for (let row = startRow; row <= endRow; row++) {
          for (let col = startCol; col <= endCol; col++) {
            const cellKey = `${row}-${col}`;
            cellColors[cellKey] = selectedColor;
            clearedCells.delete(cellKey);
          }
        }
      });
      // Trigger re-render to apply the new colors
      hot.render();
    }
  }
}

function clearFillColor() {
  if (hot) {
    const selected = hot.getSelected();
    if (selected && selected.length > 0) {
      selected.forEach(range => {
        const startRow = Math.min(range[0], range[2]);
        const endRow = Math.max(range[0], range[2]);
        const startCol = Math.min(range[1], range[3]);
        const endCol = Math.max(range[1], range[3]);
        for (let row = startRow; row <= endRow; row++) {
          for (let col = startCol; col <= endCol; col++) {
            const cellKey = `${row}-${col}`;
            delete cellColors[cellKey];
            clearedCells.add(cellKey);
          }
        }
      });
      // Trigger re-render to apply the cleared colors
      hot.render();
    }
  }
}

// Function to insert a row at a specific index
function insertRowAtIndex(index: number) {
  if (hot && !hot.isDestroyed) {
    // Insert empty row in data array
    const emptyRow = new Array(data[0].length).fill('');
    data.splice(index, 0, emptyRow);
    
    // Update the table
    hot.loadData(data);
    
    // Trigger re-render after a short delay
    setTimeout(() => {
      hot?.render();
    }, 100);
  }
}

// Function to delete a row at a specific index
function deleteRowAtIndex(index: number) {
  if (hot && !hot.isDestroyed) {
    // Remove row from data array
    data.splice(index, 1);
    
    // Update the table
    hot.loadData(data);
    
    // Trigger re-render after a short delay
    setTimeout(() => {
      hot?.render();
    }, 100);
  }
}

// Row coloring functions
function colorSelectedRows(color: string) {
  if (hot) {
    const selected = hot.getSelected();
    if (selected && selected.length > 0) {
      selected.forEach(range => {
        for (let row = range[0]; row <= range[2]; row++) {
          for (let col = range[1]; col <= range[3]; col++) {
            const cellKey = `${row}-${col}`;
            cellColors[cellKey] = color;
            clearedCells.delete(cellKey);
          }
        }
      });
      hot.render();
    }
  }
}

function clearSelectedRowColors() {
  if (hot) {
    const selected = hot.getSelected();
    if (selected && selected.length > 0) {
      selected.forEach(range => {
        for (let row = range[0]; row <= range[2]; row++) {
          for (let col = range[1]; col <= range[3]; col++) {
            const cellKey = `${row}-${col}`;
            delete cellColors[cellKey];
            clearedCells.add(cellKey);
          }
        }
      });
      hot.render();
    }
  }
}

// Cell renderer function to handle all coloring logic
function cellRenderer(this: any, instance: any, td: HTMLTableCellElement, row: number, col: number, prop: string | number, value: any, cellProperties: any) {
  // Call the default renderer first
  Handsontable.renderers.TextRenderer.apply(this, [instance, td, row, col, prop, value, cellProperties]);
  
  const cellKey = `${row}-${col}`;
  
  // Reset any existing styling
  td.style.backgroundColor = '';
  td.style.color = '';
  td.style.fontWeight = '';
  td.style.removeProperty('background-color');
  td.style.removeProperty('color');
  td.style.removeProperty('font-weight');
  
  // Apply header styling (row 0)
  if (row === 0) {
    td.style.setProperty('background-color', '#d9d9d9', 'important');
    td.style.setProperty('color', '#0000ff', 'important');
    td.style.setProperty('font-weight', 'bold', 'important');
    return;
  }
  
  // Apply special column A styling
  if (col === 0) {
    if (typeof data[row][0] === 'string') {
      const cellValue = data[row][0].toLowerCase().trim();
      if (cellValue.startsWith('start time') || cellValue.startsWith('end time')) {
        td.style.setProperty('background-color', '#d9d9d9', 'important');
        td.style.setProperty('color', '#0000ff', 'important');
        td.style.setProperty('font-weight', 'bold', 'important');
        return;
      }
    }
    // Default white background for column A if not special case
    if (!cellColors[cellKey] && !clearedCells.has(cellKey)) {
      td.style.setProperty('background-color', '#fff', 'important');
    }
  }
  
  // Skip if cell is cleared
  if (clearedCells.has(cellKey)) {
    return;
  }
  
  // Apply user-applied persistent colors (highest priority)
  if (cellColors[cellKey]) {
    td.style.setProperty('background-color', cellColors[cellKey], 'important');
    if (cellColors[cellKey] === '#375623' || cellColors[cellKey] === '#7030A0') {
      td.style.setProperty('color', '#fff', 'important');
    }
    return;
  }
  
  // Apply event type colors (only for non-column A cells)
  if (col !== 0 && data[row][2]) {
    const eventType = data[row][2].toLowerCase();
    if (eventType === 'commercial') {
      td.style.setProperty('background-color', '#FFFF00', 'important');
    } else if (eventType === 'local') {
      td.style.setProperty('background-color', '#7030A0', 'important');
      td.style.setProperty('color', '#fff', 'important');
    } else if (eventType === 'program') {
      td.style.setProperty('background-color', '#d9d9d9', 'important');
      td.style.setProperty('font-weight', 'bold', 'important');
    } else if (eventType === 'promo') {
      td.style.setProperty('background-color', '#375623', 'important');
      td.style.setProperty('color', '#fff', 'important');
    } else if (eventType === 'national dr') {
      td.style.setProperty('background-color', '#375623', 'important');
      td.style.setProperty('color', '#fff', 'important');
    }
  }
}

onMount(() => {
  if (container) {
    hot = new Handsontable(container, {
      data: data,
      colHeaders: true,
      rowHeaders: true,
      height: '100%',
      width: '100%',
      licenseKey: 'non-commercial-and-evaluation',
      manualRowMove: true,
      manualColumnMove: true,
      manualColumnResize: true,
      manualRowResize: true,
      contextMenu: {
        items: {
          'row_above': {
            name: 'Insert row above',
            callback: function() {
              const selected = this.getSelected();
              if (selected && selected.length > 0) {
                const rowIndex = selected[0][0];
                insertRowAtIndex(rowIndex);
              }
            }
          },
          'row_below': {
            name: 'Insert row below',
            callback: function() {
              const selected = this.getSelected();
              if (selected && selected.length > 0) {
                const rowIndex = selected[0][0] + 1;
                insertRowAtIndex(rowIndex);
              }
            }
          },
          'remove_row': {
            name: 'Remove row',
            callback: function() {
              const selected = this.getSelected();
              if (selected && selected.length > 0) {
                const rowIndex = selected[0][0];
                deleteRowAtIndex(rowIndex);
              }
            }
          }
        }
      },
      stretchH: 'none',
      className: '',
      colWidths: [120, 90, 80, 60, 500, 100, 100, 120, 100],
      minSpareRows: 0,
      minSpareCols: 0,
      rowHeights: 25,
      columnSorting: true,
      filters: true,
      dropdownMenu: true,
      selectionMode: 'range',
      outsideClickDeselects: false,
      afterChange: function(changes, source) {
        // Trigger re-render after changes
        if (changes && source !== 'loadData') {
          hot?.render();
        }
      },
      afterCreateRow: (index, amount, source) => {
        // Handle row insertion - shift existing color mappings
        const newCellColors: { [key: string]: string } = {};
        Object.keys(cellColors).forEach(cellKey => {
          const [row, col] = cellKey.split('-').map(Number);
          if (row >= index) {
            // Shift rows down by the amount of inserted rows
            newCellColors[`${row + amount}-${col}`] = cellColors[cellKey];
          } else {
            // Keep rows above the insertion point unchanged
            newCellColors[cellKey] = cellColors[cellKey];
          }
        });
        cellColors = newCellColors;
        
        // Also shift cleared cells
        const newClearedCells = new Set<string>();
        clearedCells.forEach(cellKey => {
          const [row, col] = cellKey.split('-').map(Number);
          if (row >= index) {
            newClearedCells.add(`${row + amount}-${col}`);
          } else {
            newClearedCells.add(cellKey);
          }
        });
        clearedCells = newClearedCells;
        
        // Trigger re-render after a short delay to ensure DOM is updated
        setTimeout(() => {
          hot?.render();
        }, 100);
      },
      afterRemoveRow: (index, amount, source) => {
        // Handle row deletion - shift existing color mappings
        const newCellColors: { [key: string]: string } = {};
        Object.keys(cellColors).forEach(cellKey => {
          const [row, col] = cellKey.split('-').map(Number);
          if (row < index) {
            // Keep rows above the deletion point unchanged
            newCellColors[cellKey] = cellColors[cellKey];
          } else if (row >= index + amount) {
            // Shift rows above the deletion point down
            newCellColors[`${row - amount}-${col}`] = cellColors[cellKey];
          }
          // Rows within the deletion range are removed
        });
        cellColors = newCellColors;
        
        // Also shift cleared cells
        const newClearedCells = new Set<string>();
        clearedCells.forEach(cellKey => {
          const [row, col] = cellKey.split('-').map(Number);
          if (row < index) {
            newClearedCells.add(cellKey);
          } else if (row >= index + amount) {
            newClearedCells.add(`${row - amount}-${col}`);
          }
        });
        clearedCells = newClearedCells;
        
        // Trigger re-render after a short delay to ensure DOM is updated
        setTimeout(() => {
          hot?.render();
        }, 100);
      },
      beforeKeyDown: (event) => {
        // Keyboard shortcuts for row coloring
        if (event.ctrlKey || event.metaKey) {
          switch(event.key) {
            case '1':
              event.stopImmediatePropagation();
              colorSelectedRows('#ffebee'); // Light red
              break;
            case '2':
              event.stopImmediatePropagation();
              colorSelectedRows('#e3f2fd'); // Light blue
              break;
            case '3':
              event.stopImmediatePropagation();
              colorSelectedRows('#f3e5f5'); // Light purple
              break;
            case '0':
              event.stopImmediatePropagation();
              clearSelectedRowColors();
              break;
          }
        }
      },
      afterSelection: (row, col, row2, col2) => {
        // This ensures the selection is properly tracked
      },
      cells: function(row: number, col: number) {
        const cellProperties: any = {};
        cellProperties.renderer = cellRenderer;
        return cellProperties;
      }
    });
    
    return () => hot?.destroy();
  }
});
</script>

<div class="excel-wrapper">
  <div class="excel-instructions">
    {#if showCongratulations}
      <div class="excel-congratulations">
        <h2 class="excel-instructions-title">🎉 Congratulations!</h2>
        <div class="excel-instructions-body">
          <p>You've successfully completed the Time Out Practice exercise!</p>
          <button class="excel-next-practice-btn" on:click={() => dispatch('navigateToNextSubmodule')}>
            Continue to Final Exam →
          </button>
        </div>
      </div>
    {:else}
      <!-- Developer Mode Toggle -->
      <div class="developer-mode-toggle">
        <button
          class="dev-mode-btn"
          class:dev-mode-active={developerMode}
          on:click={toggleDeveloperMode}
          title="Toggle Developer Mode - Automatically pass all checks"
        >
          🔧 {developerMode ? 'DEV MODE: ON' : 'DEV MODE: OFF'}
        </button>
        {#if developerMode}
          <span class="dev-mode-notice">All checks will automatically pass!</span>
        {/if}
      </div>
      
      {#if intro}
        <div class="flex justify-between items-center mb-1">
          <div></div>
          <button class="excel-nav-btn excel-nav-btn-next" aria-label="Go to Step 1" on:click={goToStep1}>
            Next →
          </button>
        </div>
        <h1 class="excel-instructions-title">Time Out Practice</h1>
        <h2 class="excel-instructions-subtitle">Instructions</h2>
        <div class="excel-instructions-body">
          The Game went over by 2 minutes! The End Time for the 8:00:00PM window is 10:02:00 PM. Find 2 minutes to cut.
        </div>
      {:else if showStep1}
        <div class="flex justify-between items-center mb-4">
          <button class="excel-nav-btn excel-nav-btn-prev" aria-label="Back to Intro" on:click={goBackIntro}>
            ← Previous
          </button>
          <div></div>
        </div>
        <h2 class="excel-instructions-title">Step 1</h2>
        <div class="excel-instructions-body">
          <div class="excel-step-hint">Find 2 minutes to Cut.<br>Complete all necessary steps to make the CUT: Write "CUT" in column A and fill all other columns red for the three National DR units that total 2 minutes. P.S. Make your life easier, CUT the larger unsold inventory first.
          </div>
          <button class="excel-check-btn" on:click={checkStep1}>Check</button>
          {#if checkResult1}
            <div class="excel-check-result">{checkResult1}</div>
            {#if checkResult1.startsWith('✅')}
              <button class="excel-step2-next-btn" on:click={goToStep2} style="margin-top: 16px;">Go to Step 2</button>
            {/if}
          {/if}
        </div>
      {:else if showStep2}
        <div class="flex justify-between items-center mb-4">
          <button class="excel-nav-btn excel-nav-btn-prev" aria-label="Back to Step 1" on:click={goBackIntro}>
            ← Previous
          </button>
          <div></div>
        </div>
        <h2 class="excel-instructions-title">Step 2</h2>
        <div class="excel-instructions-body">
          <div class="excel-step-hint">Write an email to Master Control explaining the cuts you made to save 2 minutes.</div>
          <textarea
            bind:value={emailText}
            rows="6"
            style="width:100%;margin-bottom:10px;font-size:1rem;padding:8px;border-radius:4px;border:1px solid #ccc;resize:vertical;"
            placeholder="Type your practice email here..."
          ></textarea>
          {#if !checkResult2 || checkResult2.includes('❌')}
            <button class="excel-check-btn" on:click={checkStep2}>Check</button>
          {:else}
            <button class="excel-check-btn" on:click={() => showCongratulationsCard()}>Continue →</button>
          {/if}
          {#if checkResult2}
            <div class="excel-check-result">{checkResult2}</div>
          {/if}
          
          {#if checkResult2 === '✅ Good Job! Now, check your own work in the reference email box.'}
            <div class="excel-email-compare-wrapper">
              <div class="excel-email-compare-col">
                <div class="excel-email-compare-title">Your Email</div>
                <pre class="excel-email-compare-content">{emailText}</pre>
              </div>
              <div class="excel-email-compare-col">
                <div class="excel-email-compare-title">Reference Email</div>
                <pre class="excel-email-compare-content">Here are three different ways to write the email. They are all correct.

Here is 2 mins worth of inventory to cut.

10PM Volleyball
Break 1
CUT: 600103 and 607123
Break 3
CUT:606670

OR

10PM Volleyball
Break 1
CUT: 600103
CUT: 607123

Break 3
CUT:606670

OR

10PM Game
Break 1
CUT: 600103
CUT: 607123

Break 3
CUT:606670</pre>
              </div>
            </div>
          {/if}
        </div>
      {/if}
    {/if}
  </div>

  <div class="excel-toolbar">
          <div class="excel-tool-group">
        <div class="excel-fill-color">
          <button class="excel-fill-button" on:click={applyFillColor} aria-label="Fill Color">
            <svg class="excel-paint-bucket" viewBox="0 0 20 20" width="20" height="20" fill="none">
              <rect x="7" y="15" width="6" height="3" rx="1" fill="#F4B400" stroke="#B8860B" stroke-width="0.7"/>
              <path d="M7.5 13.5L3.5 9.5C3.1 9.1 3.1 8.5 3.5 8.1L8.1 3.5C8.5 3.1 9.1 3.1 9.5 3.5L13.5 7.5C13.9 7.9 13.9 8.5 13.5 8.9L8.9 13.5C8.5 13.9 7.9 13.9 7.5 13.5Z" fill="#B0B0B0" stroke="#444" stroke-width="0.7"/>
              <rect x="6.5" y="7.5" width="7" height="2" rx="1" transform="rotate(-45 6.5 7.5)" fill="#B0B0B0" stroke="#444" stroke-width="0.7"/>
              <ellipse cx="16.5" cy="16.5" rx="1.5" ry="1" fill="#F4B400" stroke="#B8860B" stroke-width="0.7"/>
            </svg>
            <div class="excel-color-bar" style="background-color: {selectedColor}"></div>
          </button>
          <button class="excel-fill-dropdown" on:click={() => showColorPicker = !showColorPicker} aria-label="Fill Color Dropdown">
            <svg width="10" height="10" viewBox="0 0 10 10"><path d="M0 3l5 5 5-5z" fill="#222"/></svg>
          </button>
          {#if showColorPicker}
          <div class="excel-color-dropdown">
            <div class="excel-color-palette">
              <div class="excel-color-row">
                <button class="excel-color-btn" style="background-color: #FFFFFF" on:click={() => pickColor('#FFFFFF')} aria-label="White"></button>
                <button class="excel-color-btn" style="background-color: #000000" on:click={() => pickColor('#000000')} aria-label="Black"></button>
                <button class="excel-color-btn" style="background-color: #FF0000" on:click={() => pickColor('#FF0000')} aria-label="Red"></button>
                <button class="excel-color-btn" style="background-color: #00B050" on:click={() => pickColor('#00B050')} aria-label="Green"></button>
                <button class="excel-color-btn" style="background-color: #FFFF00" on:click={() => pickColor('#FFFF00')} aria-label="Yellow"></button>
              </div>
              <div class="excel-color-row">
                <button class="excel-color-btn" style="background-color: #7030A0" on:click={() => pickColor('#7030A0')} aria-label="Magenta"></button>
                <button class="excel-color-btn" style="background-color: #00B0F0" on:click={() => pickColor('#00B0F0')} aria-label="Cyan"></button>
                <button class="excel-color-btn" style="background-color: #ED7D31" on:click={() => pickColor('#ED7D31')} aria-label="Orange"></button>
                <button class="excel-color-btn" style="background-color: #A5A5A0" on:click={() => pickColor('#A5A5A0')} aria-label="Gray"></button>
                <button class="excel-color-btn" style="background-color: #375623" on:click={() => pickColor('#375623')} aria-label="Dark Green"></button>
              </div>
            </div>
            <button class="excel-clear-btn" on:click={clearFillColor}>No Fill</button>
          </div>
          {/if}
        </div>
      </div>
  </div>
  
  <div class="excel-workspace">
    <div bind:this={container} class="excel-sheet"></div>
  </div>
</div>

<style>
  .excel-wrapper {
    background: #f0f0f0;
    width: 100%;
    min-width: 0;
    padding: 20px;
    font-family: 'Calibri', 'Segoe UI', sans-serif;
    display: flex;
    flex-direction: column;
  }

  .excel-instructions {
    border: 2px solid #0074D9;
    background: #f0f6ff;
    border-radius: 6px;
    padding: 8px 20px;
    margin: 10px 0 10px 0;
    max-width: 900px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    position: relative;
  }
  
  .excel-instructions-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: #0074D9;
    margin-bottom: 4px;
    margin-top: 0;
  }
  
  .excel-instructions-subtitle {
    font-size: 1.15rem;
    font-weight: bold;
    color: #0074D9;
    margin-bottom: 4px;
    margin-top: 0;
  }
  
  .excel-instructions-body {
    font-size: 1rem;
    color: #1a2a3a;
    margin-top: 0;
  }
  
  .excel-toolbar {
    margin-top: 8px;
    padding: 8px;
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 4px;
  }
  
  .excel-tool-group {
    display: flex;
    align-items: center;
    gap: 5px;
  }
  
  .excel-fill-color {
    position: relative;
    display: flex;
    align-items: center;
  }
  
  .excel-fill-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 4px;
    border: 1px solid #c3c3c3;
    background: white;
    cursor: pointer;
    border-radius: 3px;
    min-width: 32px;
    height: 32px;
  }
  
  .excel-fill-button:hover {
    background: #f0f0f0;
  }
  
  .excel-paint-bucket {
    color: #333;
    margin-bottom: 2px;
  }
  
  .excel-color-bar {
    width: 20px;
    height: 4px;
    border: 1px solid #999;
    border-radius: 1px;
  }
  
  .excel-fill-dropdown {
    padding: 4px 6px;
    border: 1px solid #c3c3c3;
    background: white;
    cursor: pointer;
    border-radius: 3px;
    height: 32px;
    display: flex;
    align-items: center;
  }
  
  .excel-fill-dropdown:hover {
    background: #f0f0f0;
  }
  
  .excel-color-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    z-index: 1000;
    background: white;
    border: 1px solid #c3c3c3;
    border-radius: 4px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    padding: 8px;
  }
  
  .excel-color-palette {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .excel-color-row {
    display: flex;
    gap: 4px;
  }
  
  .excel-color-btn {
    width: 24px;
    height: 24px;
    border: 1px solid #ccc;
    border-radius: 3px;
    cursor: pointer;
    transition: transform 0.1s;
  }
  
  .excel-color-btn:hover {
    transform: scale(1.1);
  }
  
  .excel-clear-btn {
    margin-top: 8px;
    width: 100%;
    padding: 4px 8px;
    border: 1px solid #ccc;
    background: white;
    border-radius: 3px;
    cursor: pointer;
    font-size: 12px;
  }
  
  .excel-clear-btn:hover {
    background: #f0f0f0;
  }
  
  
  .excel-workspace {
    background: #f0f0f0;
    border: 1px solid #c3c3c3;
    height: 100vh;
    width: 100%;
    min-width: 0;
    flex: 1 1 auto;
    display: flex;
    flex-direction: column;
  }

  .excel-sheet {
    background: white;
    border: 1px solid #c3c3c3;
    flex: 1 1 auto;
    width: 100%;
    min-width: 0;
    height: 100%;
    overflow: auto;
  }

  /* Basic Excel styling */
  :global(.handsontable) {
    font-family: 'Calibri', 'Segoe UI', sans-serif !important;
    font-size: 11px !important;
  }

  /* All cells same height */
  :global(.handsontable .htCore th),
  :global(.handsontable .htCore td) {
    height: 25px !important;
    box-sizing: border-box !important;
  }

  /* Headers */
  :global(.handsontable .htColHeaders th) {
    background: #f8f9fa !important;
    color: #000 !important;
    font-weight: 600 !important;
    border: 1px solid #c3c3c3 !important;
    border-bottom: 2px solid #c3c3c3 !important;
    text-align: center !important;
    vertical-align: middle !important;
  }

  :global(.handsontable .htRowHeaders th) {
    background: #f8f9fa !important;
    color: #000 !important;
    font-weight: 600 !important;
    border: 1px solid #c3c3c3 !important;
    border-right: 2px solid #c3c3c3 !important;
    text-align: center !important;
    vertical-align: middle !important;
    width: 40px !important;
  }

  /* Data cells */
  :global(.handsontable .htCore td) {
    border: 1px solid #c3c3c3 !important;
    background: white !important;
    vertical-align: middle !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
    max-width: 100%;
    text-align: left !important;
  }

  /* Corner cell */
  :global(.handsontable .htCore .corner) {
    background: #f8f9fa !important;
    border: 1px solid #c3c3c3 !important;
    border-right: 2px solid #c3c3c3 !important;
    border-bottom: 2px solid #c3c3c3 !important;
    width: 40px !important;
  }

  /* Current cell */
  :global(.handsontable .htCore .current) {
    border: 2px solid #0078d4 !important;
  }

  /* Hover effect */
  :global(.handsontable .htCore td:hover) {
    background: #f0f7ff !important;
  }
  
  .excel-step-hint {
    background: transparent;
    border: none;
    border-radius: 0;
    padding: 0;
    margin: 8px 0;
    color: #1a2a3a;
    font-style: normal;
    font-weight: 500;
  }
  
  .excel-check-btn {
    background: #0074D9;
    color: white;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    font-size: 0.9rem;
    margin-bottom: 10px;
  }
  
  .excel-check-btn:hover {
    background: #0056b3;
  }
  
  .excel-check-result {
    margin: 10px 0;
    padding: 8px 12px;
    border-radius: 4px;
    font-weight: 500;
  }
  
  .excel-step2-next-btn {
    background: #28a745;
    color: white;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    font-size: 0.9rem;
  }
  
  .excel-step2-next-btn:hover {
    background: #218838;
  }
  
  .excel-nav-btn {
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    font-size: 0.9rem;
  }
  
  .excel-nav-btn-prev {
    background: #f1f5f9;
    color: #64748b;
    border: 1px solid #e2e8f0;
  }
  
  .excel-nav-btn-prev:hover {
    background: #e2e8f0;
  }
  
  .excel-nav-btn-next {
    background: #0074D9;
    color: white;
    border: 1px solid #0056b3;
  }
  
  .excel-nav-btn-next:hover {
    background: #0056b3;
  }
  
  .excel-congratulations {
    border: 2px solid #4CAF50;
    background: #e8f5e9;
    border-radius: 6px;
    padding: 15px 20px;
    margin: 10px 0 10px 0;
    max-width: 900px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    position: relative;
  }
  
  .excel-next-practice-btn {
    background: #4CAF50;
    color: white;
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    font-size: 0.9rem;
    margin-top: 15px;
  }
  
  .excel-next-practice-btn:hover {
    background: #388E3C;
  }
  
  .developer-mode-toggle {
    margin-bottom: 15px;
    padding: 10px;
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 4px;
  }
  
  .dev-mode-btn {
    background: #6c757d;
    color: white;
    padding: 6px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: background-color 0.2s;
  }
  
  .dev-mode-btn:hover {
    background: #5a6268;
  }
  
  .dev-mode-active {
    background: #dc3545 !important;
  }
  
  .dev-mode-notice {
    display: block;
    margin-top: 8px;
    color: #dc3545;
    font-weight: 600;
    font-size: 0.9rem;
  }
  
  .flex {
    display: flex;
  }
  
  .justify-between {
    justify-content: space-between;
  }
  
  .items-center {
    align-items: center;
  }
  
  .mb-1 {
    margin-bottom: 0.25rem;
  }
  
  .mb-4 {
    margin-bottom: 1rem;
  }
  
  .excel-email-compare-wrapper {
    display: flex;
    gap: 24px;
    margin-top: 18px;
  }
  
  .excel-email-compare-col {
    flex: 1 1 0;
    min-width: 0;
    background: #f9f9f9;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    padding: 12px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
  }
  
  .excel-email-compare-title {
    font-weight: bold;
    color: #0074D9;
    margin-bottom: 8px;
    font-size: 1rem;
  }
  
  .excel-email-compare-content {
    font-family: 'Consolas', 'Menlo', 'Monaco', monospace;
    font-size: 0.98rem;
    white-space: pre-wrap;
    color: #222;
    background: #fff;
    border-radius: 4px;
    padding: 8px;
    min-height: 120px;
  }
</style> 