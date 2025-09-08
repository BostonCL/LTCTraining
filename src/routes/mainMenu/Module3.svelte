<script lang="ts">
  import { onMount } from 'svelte';
  import Handsontable from 'handsontable';
  import 'handsontable/dist/handsontable.full.min.css';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  // Placeholder for navigation logic
  let showStep1 = false;
  let showStep2 = false;
  let showStep2Popup = false;
  let showStep3 = false;
  function goToStep3() {
    showStep3 = true;
  }
  let showStep4 = false;
  function goToStep4() {
    showStep4 = true;
  }
  let step1Snapshot: { data: any[]; cellColors: { [key: string]: string } } | null = null;
  function goToStep1() {
    showStep1 = true;
  }
  function goBackInstructions() {
    showStep1 = false;
  }
  function goToStep2() {
    // Deep copy data and cellColors
    step1Snapshot = {
      data: JSON.parse(JSON.stringify(data)),
      cellColors: JSON.parse(JSON.stringify(cellColors))
    };
    showStep2 = true;
    showStep2Popup = false;
  }

  let container: HTMLDivElement;
  let hot: Handsontable | null = null;
  let selectedColor = '#F2DCDB'; // Default light red
  let showColorPicker = false;
  let cellColors: { [key: string]: string } = {
    // Default colors for the header row (row 0) - Standard grey
    '0-0': '#A5A5A5', // Real Time - Grey
    '0-1': '#A5A5A5', // Hit Time - Grey
    '0-2': '#A5A5A5', // Event Type - Grey
    '0-3': '#A5A5A5', // Length - Grey
    '0-4': '#A5A5A5', // Title - Grey
    '0-5': '#A5A5A5', // Advertiser - Grey
    '0-6': '#A5A5A5', // House Number - Grey
    '0-7': '#A5A5A5', // Ordered As - Grey
    '0-8': '#A5A5A5', // Spot End Time - Grey
    
    // Default colors for the first data row (row 1) - Standard grey
    '1-0': '#A5A5A5', // Start Time - Grey
    '1-1': '#A5A5A5', // 8:00:00 AM - Grey
    '1-2': '#A5A5A5', // Program - Grey
    '1-3': '#A5A5A5', // 00:05:00 - Grey
    '1-4': '#A5A5A5', // That Other Pregame Show... - Grey
    '1-5': '#A5A5A5', // (empty) - Grey
    '1-6': '#A5A5A5', // 327301 - Grey
    '1-7': '#A5A5A5', // (empty) - Grey
    '1-8': '#A5A5A5'  // (empty) - Grey
  }; // Store persistent cell colors
// This is excel where I left off. Im working on the nofill color feature. 
// Next will be working on step 2 for the check
  let clearedCells = new Set<string>();

    //Step 1 Check. Done for now
  let checkResult = '';
  function checkStep1() {
    if (developerMode) {
      checkResult = '🔧 DEV MODE: Step 1 automatically passed!';
      setTimeout(() => { goToStep2(); }, 800);
      return;
    }

    // Find the two target rows by their unique values
    const targets = [
      { time: '09:22:22 PM', promo: 'Promo' },
      { time: '09:24:32 PM', promo: 'Promo' }
    ];
    let allCorrect = true;
    for (const target of targets) {
      const rowIdx = data.findIndex(row => row[1] === target.time && row[2] && row[2].toLowerCase() === target.promo.toLowerCase());
      if (rowIdx === -1) {
        allCorrect = false;
        break;
      }
      // Check column A for 'CUT' (case insensitive, trimmed)
      if (!data[rowIdx][0] || data[rowIdx][0].trim().toLowerCase() !== 'cut') {
        allCorrect = false;
        break;
      }
      // Check if all columns except A are filled red
      for (let col = 1; col < data[rowIdx].length; col++) {
        const cellKey = `${rowIdx}-${col}`;
        const color = (cellColors[cellKey] || '').toLowerCase();
        if (
          color !== '#e53e3e' &&
          color !== '#ff0000' &&
          color !== '#E53E3E'.toLowerCase() &&
          color !== '#FF0000'.toLowerCase() &&
          color !== 'rgb(229,62,62)' &&
          color !== 'rgb(255,0,0)'
        ) {
          allCorrect = false;
          break;
        }
      }
      if (!allCorrect) break;
    }
    if (allCorrect) {
      checkResult = '✅ Correct! You found and marked the unsold green promos to CUT.';
      // No popup, just show button in instructions
    } else {
      checkResult = '❌ Not quite! Are you looking in break 3? Did you write CUT in column A next to the promos? Are those Promos filled red?';
    }
  }

  let checkResult2 = '';
  function checkStep2() {
    if (developerMode) {
      checkResult2 = '🔧 DEV MODE: Step 2 automatically passed!';
      setTimeout(() => { goToStep3(); }, 800);
      return;
    }

    // Find the two target rows by their unique values (the promos to cut)
    const targets = [
      { time: '09:32:00 PM', title: 'BRACKET BREAKDOWN FRIDAY 3 REV. 1' },
      { time: '09:33:40 PM', title: 'MM SWEET 16 THURSDAY' }
    ];
    let allCorrect = true;
    for (const target of targets) {
      const rowIdx = data.findIndex(row => row[1] === target.time && row[2] && row[2].toLowerCase() === 'promo' && row[4] && row[4].toLowerCase() === target.title.toLowerCase());
      if (rowIdx === -1) {
        allCorrect = false;
        break;
      }
      // Check column A for 'CUT' (case insensitive, trimmed)
      if (!data[rowIdx][0] || data[rowIdx][0].trim().toLowerCase() !== 'cut') {
        allCorrect = false;
        break;
      }
      // Check if all columns except A are filled red
      for (let col = 1; col < data[rowIdx].length; col++) {
        const cellKey = `${rowIdx}-${col}`;
        const color = (cellColors[cellKey] || '').toLowerCase();
        if (
          color !== '#e53e3e' &&
          color !== '#ff0000' &&
          color !== '#E53E3E'.toLowerCase() &&
          color !== '#FF0000'.toLowerCase() &&
          color !== 'rgb(229,62,62)' &&
          color !== 'rgb(255,0,0)'
        ) {
          allCorrect = false;
          break;
        }
      }
      if (!allCorrect) break;
    }
    if (allCorrect) {
      checkResult2 = '✅ Correct! You found and marked the two target promos to CUT.';
      setTimeout(() => { goToStep3(); }, 800); // Navigate to step 3 after short delay
    } else {
      checkResult2 = '❌ Not quite! Are both promos red with CUT next to them? Did you insert the row and paste the swap there?';
    }
  }

  let checkResult3 = '';
  function checkStep3() {
    if (developerMode) {
      checkResult3 = '🔧 DEV MODE: Step 3 automatically passed!';
      setTimeout(() => { goToStep4(); }, 800);
      return;
    }

    // Find the two target rows by their unique values (the promos to cut)
    const targets = [
      { time: '09:32:00 PM', title: 'BRACKET BREAKDOWN FRIDAY 3 REV. 1' },
      { time: '09:33:40 PM', title: 'MM SWEET 16 THURSDAY' }
    ];
    let allCorrect = true;
    for (const target of targets) {
      const rowIdx = data.findIndex(row => row[1] === target.time && row[2] && row[2].toLowerCase() === 'promo' && row[4] && row[4].toLowerCase() === target.title.toLowerCase());
      if (rowIdx === -1) {
        allCorrect = false;
        break;
      }
      // Check column A for 'CUT' (case insensitive, trimmed)
      if (!data[rowIdx][0] || data[rowIdx][0].trim().toLowerCase() !== 'cut') {
        allCorrect = false;
        break;
      }
      // Check if all columns except A are filled red
      for (let col = 1; col < data[rowIdx].length; col++) {
        const cellKey = `${rowIdx}-${col}`;
        const color = (cellColors[cellKey] || '').toLowerCase();
        if (
          color !== '#e53e3e' &&
          color !== '#ff0000' &&
          color !== '#E53E3E'.toLowerCase() &&
          color !== '#FF0000'.toLowerCase() &&
          color !== 'rgb(229,62,62)' &&
          color !== 'rgb(255,0,0)'
        ) {
          allCorrect = false;
          break;
        }
      }
      if (!allCorrect) break;
    }
    if (!allCorrect) {
      checkResult3 = '❌ Not quite! Are both promos red with CUT next to them?';
      return;
    }

    // Now check if the OLD TRAPPER unit has been inserted into a new row
    // Find the MM SWEET 16 THURSDAY promo row
    const mmSweetRowIdx = data.findIndex(row => row[1] === '09:33:40 PM' && row[2] && row[2].toLowerCase() === 'promo' && row[4] && row[4].toLowerCase() === 'mm sweet 16 thursday');
    
    if (mmSweetRowIdx === -1) {
      checkResult3 = '❌ Could not find the MM SWEET 16 THURSDAY promo row.';
      return;
    }

    // Check if there's a row after MM SWEET 16 THURSDAY that contains the OLD TRAPPER unit
    const insertedRowIdx = mmSweetRowIdx + 1;
    if (!data[insertedRowIdx] || !data[insertedRowIdx][4]) {
      checkResult3 = '❌ Did you insert a new row after MM SWEET 16 THURSDAY?';
      return;
    }

    // Check if the inserted row contains the OLD TRAPPER unit
    const insertedTitle = (data[insertedRowIdx][4] || '').toLowerCase();
    if (!insertedTitle.includes('old trapper') && !insertedTitle.includes('camping catastrophes')) {
      checkResult3 = '❌ Did you copy and paste the OLD TRAPPER unit into the new row?';
      return;
    }

    // Check if the inserted row has the correct data structure
    const expectedData = [
      '', // Column A (empty)
      '09:23:02 PM', // Hit Time
      'Commercial', // Event Type
      '00:00:30', // Length
      'OLD TRAPPER : CAMPING CATASTROPHES', // Title
      'OLD TRAPPER', // Advertiser
      '602584', // House Number
      'ROS 24 HOUR', // Ordered As
      '05:59:00 AM' // Spot End Time
    ];

    let dataMatches = true;
    for (let col = 1; col < expectedData.length; col++) {
      if (data[insertedRowIdx][col] !== expectedData[col]) {
        dataMatches = false;
        break;
      }
    }

    if (!dataMatches) {
      checkResult3 = '❌ The inserted row data doesn\'t match the OLD TRAPPER unit. Make sure you copied all the data correctly.';
      return;
    }

    checkResult3 = '✅ Correct! You found and marked the two target promos to CUT, and inserted the OLD TRAPPER unit into a new row.';
    setTimeout(() => { goToStep4(); }, 800); // Navigate to step 4 after short delay
  }

  let checkResult4 = '';
  function checkStep4() {
    if (developerMode) {
      checkResult4 = '🔧 DEV MODE: Step 4 automatically passed!';
      setTimeout(() => { showCongratulationsCard(); }, 800);
      return;
    }

    // Find the original OLD TRAPPER row
    const origIdx = data.findIndex(row => row[1] === '09:23:02 PM' && row[2] && row[2].toLowerCase() === 'commercial' && row[4] && row[4].toLowerCase() === 'old trapper : camping catastrophes');
    // Find the blue row (should be after MM SWEET 16 THURSDAY)
    const afterRowIdx = data.findIndex(row => row[1] === '09:33:40 PM' && row[2] && row[2].toLowerCase() === 'promo' && row[4] && row[4].toLowerCase() === 'mm sweet 16 thursday');
    const blueIdx = afterRowIdx + 1;
    if (origIdx === -1 || !data[blueIdx]) {
      checkResult4 = '❌ Could not find the required rows.';
      return;
    }
    // Check column A of original row
    const origA = (data[origIdx][0] || '').trim().toLowerCase();
    if (origA !== 'moved to b1 of 9:30') {
      checkResult4 = '❌ Did you mark the OLD TRAPPER unit blue and write "moved from b3 of the 9PM"?';
      return;
    }
    // Check column A of blue row
    const blueA = (data[blueIdx][0] || '').trim().toLowerCase();
    if (blueA !== 'moved from b3 of 9p.') {
      checkResult4 = '❌ In the new blue row, column A must say: moved from b3 of 9p.';
      return;
    }
    checkResult4 = '✅ Correct! You annotated both rows as required.';
    setTimeout(() => { showCongratulationsCard(); }, 800);
  }

  // Fill color functions
  function selectColor(color: string) {
    selectedColor = color;
    showColorPicker = false;
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
              // Store color persistently
              const cellKey = `${row}-${col}`;
              cellColors[cellKey] = selectedColor;
              clearedCells.delete(cellKey); // If user fills, remove from cleared
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
          // Normalize selection
          const startRow = Math.min(range[0], range[2]);
          const endRow = Math.max(range[0], range[2]);
          const startCol = Math.min(range[1], range[3]);
          const endCol = Math.max(range[1], range[3]);
          for (let row = startRow; row <= endRow; row++) {
            for (let col = startCol; col <= endCol; col++) {
              // Remove color from persistent storage
              const cellKey = `${row}-${col}`;
              delete cellColors[cellKey];
              clearedCells.add(cellKey); // Mark as user cleared
            }
          }
        });
        // Trigger re-render to apply the cleared colors
        hot.render();
      }
    }
    showColorPicker = false;
  }

  function showCustomColor() {
    // For now, just close the picker. Could implement custom color picker later
    showColorPicker = false;
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
        if (cellValue === 'start time' || cellValue === 'end time' || cellValue === 'start time 9:00:00') {
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

  function pickColor(color: string) {
    selectedColor = color;
    showColorPicker = false;
    applyFillColor();
  }

  // Row coloring functions
  function colorSelectedRows(color: string) {
    if (hot) {
      const selected = hot.getSelected();
      if (selected && selected.length > 0) {
        selected.forEach(range => {
          for (let row = range[0]; row <= range[2]; row++) {
            for (let col = range[1]; col <= range[3]; col++) {
              const cell = hot?.getCell(row, col);
              if (cell) {
                cell.style.backgroundColor = color;
              }
            }
          }
        });
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
              const cell = hot?.getCell(row, col);
              if (cell) {
                cell.style.backgroundColor = '';
              }
            }
          }
        });
      }
    }
  }


  // Sample data for demonstration
  let data = [
    ["Real Time 9:00:00", "Hit Time", "Event Type", "Length", "Title", "Advertiser", "House Number", "Ordered As", "Spot End Time"],
    ["Start Time 9:00:00", "09:00:00 PM", "Program", "00:04:40", "Original Encore 22 [Home Court: Brian Dutcher]: SEG. 1", "", "245911", "", ""],
    ["9:03:54", "09:04:40 PM", "Promo", "00:00:20", "MM 360 TOMORROW", "CBS SPORTS NETWORK", "809812", "", ""],
    ["", "09:05:00 PM", "Commercial", "00:00:30", "BELFOR: BELFOR_RESTORING HOPE_30", "BELFOR", "604284", "NCAA REBOUND", "05:59:00 AM"],
    ["", "09:05:30 PM", "Commercial", "00:00:30", "CHASE: PM36829_CHASE 2024 INK_MICO'S HOT CHICKEN_TVC_30", "CHASE", "605237", "NCAA REBOUND", "05:59:00 AM"],
    ["", "09:06:00 PM", "Commercial", "00:00:15", "HERSHEY'S: YES!", "HERSHEY'S", "605495", "NCAA REBOUND", "05:59:00 AM"],
    ["", "09:06:15 PM", "Commercial", "00:00:15", "DOMINOS: PAN SECRET WLC OFFER :15", "DOMINOS", "608796", "NCAA REBOUND", "12:00:00 AM"],
    ["", "09:06:30 PM", "Commercial", "00:00:30", "BMW: BMW_2024 SUPER BOWL_TALKIN LIKE WALKEN_MY24 I5 M60_30", "BMW", "609815", "NCAA REBOUND", "05:59:00 AM"],
    ["", "09:07:00 PM", "Promo", "00:00:10", "WOMENS HISTORY MONTH", "CBS SPORTS NETWORK", "809715", "", ""],
    ["", "09:07:10 PM", "Program", "00:05:40", "Original Encore 22 [Home Court: Brian Dutcher]: SEG. 2", "", "245912", "", ""],
    ["9:15:32", "09:12:50 PM", "Commercial", "00:00:30", "NISSAN: 23_Q4_NNA_MARCHMADNESS_TVC_FITNESS_30_16X9_SLATED_ER_", "NISSAN", "607258", "NCAA REBOUND", "05:59:00 AM"],
    ["", "09:13:20 PM", "Commercial", "00:00:30", "SQUARESPACE: 'HELLO DOWN THERE' REV 2 :30", "SQUARESPACE", "609931", "NCAA REBOUND", "05:59:00 AM"],
    ["", "09:13:50 PM", "Commercial", "00:00:15", "ACE HARDWARE: OPE/‘THE PLACE FOR EVERYTHING’/BATTERY/2024", "ACE HARDWARE", "607226", "NCAA REBOUND", "05:59:00 AM"],
    ["", "09:14:05 PM", "Commercial", "00:00:15", "CHASE: PM36829_CHASE 2024 INK_MICO'S HOT CHICKEN_ATTENTION_TVC_15", "CHASE", "605238", "NCAA REBOUND", "05:59:00 AM"],
    ["", "09:14:20 PM", "Local", "Local", "Local", "Local", "Local", "Local", "Local"],
    ["", "09:15:50 PM", "Program", "00:06:32", "Original Encore 22 [Home Court: Brian Dutcher]: SEG. 3", "", "245913", "", ""],
    ["", "09:22:22 PM", "Promo", "00:00:20", "REESES COLLEGE ASG APRIL 5", "CBS SPORTS NETWORK", "809797", "", ""],
    ["", "09:22:32 PM", "Commercial", "00:00:30", "AT&T: TRUST AGAIN :30 V3 BUY NOW", "AT&T", "603354", "NCAA REBOUND", "05:59:00 AM"],
    ["", "09:23:02 PM", "Commercial", "00:00:30", "OLD TRAPPER : CAMPING CATASTROPHES", "OLD TRAPPER", "602584", "ROS 24 HOUR", "05:59:00 AM"],
    ["", "09:23:32 PM", "Commercial", "00:00:15", "HERSHEY'S: YES!", "HERSHEY'S", "605495", "NCAA REBOUND", "05:59:00 AM"],
    ["", "09:23:47 PM", "Commercial", "00:00:15", "CHRYSLER: INNER PEACE V1 REV/VANLIGHTENMENT/CHRYSLER/COMBO/15", "CHRYSLER", "600282", "NCAA REBOUND", "05:59:00 AM"],
    ["", "09:24:02 PM", "Commercial", "00:00:30", "WERNER LADDER: 2024 BASKETBALL REACH NEW HEIGHTS 30", "WERNER LADDER", "601487", "ROS 24 HOUR", "05:59:00 AM"],
    ["", "09:24:32 PM", "Promo", "00:00:10", "PGA CHAMP COMING IN MAY", "CBS Broadcast", "809562", "", ""],
    ["End Time", "09:24:42 PM", "Program", "00:05:18", "Original Encore 22 [Home Court: Brian Dutcher]: SEG. 4", "", "245914", "", ""],
    ["", "", "", "", "", "", "", "", ""],
    ["Start Time", "09:30:00 PM", "Program", "00:02:00", "Post Season Basketball Women's P2 [2024 NCAA Women's Basketball Division II Championship: Semifinal # 2 - 3/27/24]: SEG. 1", "", "316701", "", ""],
    ["", "09:32:00 PM", "Promo", "00:00:10", "BRACKET BREAKDOWN FRIDAY 3 REV. 1", "CBS SPORTS NETWORK", "809804", "", ""],
    ["", "09:32:10 PM", "Commercial", "00:00:30", "WERNER LADDER: 2024 BASKETBALL REACH NEW HEIGHTS 30", "WERNER LADDER", "608790", "COLLEGE BBALL: WMN'S POST SEASON", "11:30:00 PM"],
    ["", "09:32:40 PM", "Commercial", "00:00:30", "CHASE: BANKING LEADERSHIP 2023_ADVICE_THE JENNIFERS_EN_TVC_30", "CHASE", "605750", "COLLEGE BBALL: WMN'S POST SEASON", "05:59:00 AM"],
    ["", "09:33:10 PM", "Commercial", "00:00:30", "HONDA: RETAIL - SPRING INTO PERFORMANCE - 'FULL-LINE' - TAGGABLE OFFER AND NON-OFFER - :23/:07 - HACN3491000H", "HONDA", "608364", "COLLEGE BBALL: WMN'S POST SEASON", "05:59:00 AM"],
    ["", "09:33:40 PM", "Promo", "00:00:20", "MM SWEET 16 THURSDAY", "CBS Broadcast", "809815", "", ""],
    ["", "09:34:00 PM", "Program", "00:08:30", "Post Season Basketball Women's P2 [2024 NCAA Women's Basketball Division II Championship: Semifinal # 2 - 3/27/24]: SEG. 2", "", "316702", "", ""],
    ["", "09:42:30 PM", "Commercial", "00:00:30", "ALLSTATE INSURANCE: FILL IN THE RATE 16X9 BROADCAST HD :30", "ALLSTATE INSURANCE", "601036", "COLLEGE BBALL: WMN'S POST SEASON", "05:59:00 AM"],
    ["", "09:43:00 PM", "Commercial", "00:00:30", "TITLEIST: 2023 WORLDWIDE WRAP UP", "TITLEIST", "609507", "COLLEGE BBALL: WMN'S POST SEASON", "05:59:00 AM"],
    ["", "09:43:30 PM", "Local", "Local", "Local", "Local", "Local", "Local", "Local"],
    ["", "09:45:00 PM", "Program", "00:10:00", "Post Season Basketball Women's P2 [2024 NCAA Women's Basketball Division II Championship: Semifinal # 2 - 3/27/24]: SEG. 3", "", "316703", "", ""],
    ["", "09:55:00 PM", "Commercial", "00:00:30", "NCAA DII WOMEN'S BASKETBALL CHAMPIONSHIP: OLYMPIANS MADE HERE", "NCAA DII Women's Basketball Championship", "608803", "COLLEGE BBALL: WMN'S POST SEASON", "11:30:00 PM"],
    ["", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", "", ""]
  ];
  // Remove rows 38 to 47 (inclusive)
  data.splice(38, 10);

  // Developer mode toggle
  let developerMode = false;

  // Congratulations state
  let showCongratulations = false;

  function showCongratulationsCard() {
    showCongratulations = true;
    // Reset all step states to prevent rendering conflicts
    showStep1 = false;
    showStep2 = false;
    showStep3 = false;
    showStep4 = false;
  }

  function toggleDeveloperMode() {
    developerMode = !developerMode;
    if (developerMode) {
      console.log('🔧 Developer Mode: ENABLED - All checks will automatically pass');
    } else {
      console.log('🔧 Developer Mode: DISABLED - Normal validation active');
    }
  }

  onMount(() => {
    hot = new Handsontable(container, {
      data,
      rowHeaders: true,
      colHeaders: true,
      width: '100%',
      height: '100%',
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
      className: '', // Remove 'htCenter' to left-align content
      colWidths: [120, 90, 80, 60, 400, 100, 100, 120, 100],
      minSpareRows: 0,
      minSpareCols: 0,
      rowHeights: 25,
      columnSorting: true,
      filters: true,
      dropdownMenu: true,
      selectionMode: 'range', // Enable range selection mode
      outsideClickDeselects: false, // Keep selection when clicking outside
      afterChange: (changes, source) => {
        // Optionally handle changes here
        hot?.render(); // Trigger re-render after changes
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
  });
</script>

<!-- Remove Step 2 Navigation Popup -->

<div class="excel-wrapper">
  <div class="excel-instructions">
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

    {#if showCongratulations}
      <div class="excel-congratulations">
        <h2 class="excel-instructions-title">🎉 Congratulations!</h2>
        <div class="excel-instructions-body">
          <p>You've successfully completed the Live Coverage Sheet exercise!</p>
          <button class="excel-next-practice-btn" on:click={() => dispatch('navigateToNextSubmodule')}>
            Continue to Unit Cut Practice →
          </button>
        </div>
      </div>
    {:else if !showStep1 && !showStep2 && !showStep3 && !showStep4}
      <div class="flex justify-between items-center mb-1">
        <div></div>
        <button class="excel-nav-btn excel-nav-btn-next" aria-label="Go to Step 1" on:click={goToStep1}>
          Next →
        </button>
      </div>
      <h1 class="excel-instructions-title">Interactive Live Coverage Sheet</h1>
      <h2 class="excel-instructions-subtitle">Instructions</h2>
      <div class="excel-instructions-body">
        The producer wants to cut 1 minute from break 3 of the 9PM window. This is an Interactive Excel Live Coverage Sheet. Let's perform the actions. You can edit cells, drag rows, use the paint can in the upper left hand corner to correctly mark colors and right-click for more options.
      </div>
    {:else if showStep1 && !showStep2 && !showStep3 && !showStep4}
      <div class="flex justify-between items-center mb-4">
        <button class="excel-nav-btn excel-nav-btn-prev" aria-label="Back to Instructions" on:click={goBackInstructions}>
          ← Previous
        </button>
        <div></div>
      </div>
      <h2 class="excel-instructions-title">Step 1</h2>
      <div class="excel-instructions-body">
        <div class="excel-step-hint">Identify the break you are working in. Next, check the Ordered As column. Which units can you CUT (Mark as Dead)? Are there any? Maybe green inventory? When you find the inventory you can CUT, correctly mark it on the sheet. NOTE: there is a little paint can in the upper left hand corner of the interactive sheet. And a no fill button within that to clean up the column where you make notes.</div>
        <button class="excel-check-btn" on:click={checkStep1}>Check</button>
        {#if checkResult}
          <div class="excel-check-result">{checkResult}</div>
          {#if checkResult.startsWith('✅')}
            <button class="excel-step2-next-btn" on:click={goToStep2} style="margin-top: 16px;">Go to Step 2</button>
          {/if}
        {/if}
      </div>
    {:else if showStep2 && !showStep3 && !showStep4}
      <h2 class="excel-instructions-title">Step 2</h2>
      <div class="excel-instructions-body">
        <div class="excel-step-hint">
          Now you need to CUT two promos from Break 1 of the 9:30PM window to make room for the unit you're moving. Find the two promos: "BRACKET BREAKDOWN FRIDAY 3 REV. 1" at 9:32:00 PM and "MM SWEET 16 THURSDAY" at 9:33:40 PM. Mark both of them as CUT in column A and fill all their cells red (except column A).
        </div>
        <button class="excel-check-btn" on:click={checkStep2}>Check</button>
        {#if checkResult2}
          <div class="excel-check-result">{checkResult2}</div>
        {/if}
      </div>
    {:else if showStep3 && !showStep4}
      <h2 class="excel-instructions-title">Step 3</h2>
      <div class="excel-instructions-body">
        <div class="excel-step-hint">
          What inventory can you CUT from Break 1 of the 9:30PM window? Are there any promos? Did you mark them as red with "CUT" written next to them? When that's done insert a row and copy and paste your "ROS 24 HOUR- OLD TRAPPER" unit from B3 of the 9PM window there.
        </div>
        <button class="excel-check-btn" on:click={checkStep3}>Check</button>
        {#if checkResult3}
          <div class="excel-check-result">{checkResult3}</div>
        {/if}
      </div>
    {:else if showStep4}
      <h2 class="excel-instructions-title">Step 4</h2>
      <div class="excel-instructions-body">
        <div class="excel-step-hint">
          Look at the row you just moved. Color fill that row and write where you moved it from.
        </div>
        <button class="excel-check-btn" on:click={checkStep4}>Check</button>
        {#if checkResult4}
          <div class="excel-check-result">{checkResult4}</div>
        {/if}
      </div>
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
              <button type="button" class="excel-color-item" style="background-color: #FFFFFF" aria-label="Fill white" on:click={() => pickColor('#FFFFFF')}></button>
              <button type="button" class="excel-color-item" style="background-color: #000000" aria-label="Fill black" on:click={() => pickColor('#000000')}></button>
              <button type="button" class="excel-color-item" style="background-color: #FF0000" aria-label="Fill red" on:click={() => pickColor('#FF0000')}></button>
              <button type="button" class="excel-color-item" style="background-color: #00B050" aria-label="Fill green" on:click={() => pickColor('#00B050')}></button>
              <button type="button" class="excel-color-item" style="background-color: #00B0F0" aria-label="Fill cyan" on:click={() => pickColor('#00B0F0')}></button>
              <button type="button" class="excel-color-item" style="background-color: #FFFF00" aria-label="Fill yellow" on:click={() => pickColor('#FFFF00')}></button>
              <button type="button" class="excel-color-item" style="background-color: #7030A0" aria-label="Fill magenta" on:click={() => pickColor('#7030A0')}></button>
              <button type="button" class="excel-color-item" style="background-color: #ED7D31" aria-label="Fill orange" on:click={() => pickColor('#ED7D31')}></button>
              <button type="button" class="excel-color-item" style="background-color: #A5A5A5" aria-label="Fill gray" on:click={() => pickColor('#A5A5A5')}></button>
            </div>
          </div>
          <div class="excel-color-actions">
            <button class="excel-no-fill" on:click={clearFillColor}>No Fill</button>
            <button class="excel-more-colors" on:click={showCustomColor}>More Colors...</button>
          </div>
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
    height: 100vh;
    min-height: 100vh;
    width: 100%;
    min-width: 0;
    padding: 0;
    font-family: 'Calibri', 'Segoe UI', sans-serif;
    display: flex;
    flex-direction: column;
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
    min-width: 200px;
  }

  .excel-color-palette {
    margin-bottom: 8px;
  }

  .excel-color-row {
    display: flex;
    gap: 2px;
    margin-bottom: 2px;
  }

  .excel-color-item {
    width: 20px;
    height: 20px;
    border: 1px solid #c3c3c3;
    cursor: pointer;
    border-radius: 2px;
    padding: 0;
    margin: 0;
  }

  .excel-color-item:hover {
    border-color: #0078d4;
    transform: scale(1.1);
  }

  .excel-color-actions {
    display: flex;
    flex-direction: column;
    gap: 4px;
    border-top: 1px solid #e0e0e0;
    padding-top: 8px;
  }

  .excel-no-fill,
  .excel-more-colors {
    padding: 4px 8px;
    border: 1px solid #c3c3c3;
    background: white;
    cursor: pointer;
    border-radius: 3px;
    font-size: 12px;
    text-align: left;
  }

  .excel-no-fill:hover,
  .excel-more-colors:hover {
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
  
  .excel-step-hint {
    color: #1a2a3a;
  }



  
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .excel-check-btn {
    margin-top: 16px;
    background: #0074D9;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 8px 22px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
    box-shadow: 0 2px 6px rgba(0,0,0,0.07);
  }
  .excel-check-btn:hover {
    background: #005fa3;
  }
  .excel-check-result {
    margin-top: 12px;
    font-size: 1.08rem;
    font-weight: 500;
  }
  .excel-step2-next-btn {
    background: #0074D9;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 10px 28px;
    font-size: 1.1rem;
    font-weight: 600;
    margin: 16px 8px 0 0;
    cursor: pointer;
    transition: background 0.2s;
  }
  .excel-step2-next-btn:hover {
    background: #005fa3;
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
  .excel-nav-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
  .excel-nav-btn-prev {
    background: #f1f5f9;
    color: #64748b;
    border: 1px solid #e2e8f0;
  }
  .excel-nav-btn-prev:hover:not(:disabled) {
    background: #e2e8f0;
  }
  .excel-nav-btn-next {
    background: #2563eb;
    color: white;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  .excel-nav-btn-next:hover:not(:disabled) {
    background: #1d4ed8;
  }
  .developer-mode-toggle {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 15px;
    padding: 8px 12px;
    background-color: #e0e0e0;
    border-radius: 5px;
    border: 1px solid #c3c3c3;
  }
  .dev-mode-btn {
    background-color: #0074D9;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.2s;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
  }
  .dev-mode-btn:hover {
    background-color: #005fa3;
  }
  .dev-mode-btn.dev-mode-active {
    background-color: #4CAF50; /* A different green for active */
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  }
  .dev-mode-notice {
    font-size: 0.85rem;
    color: #555;
    margin-left: 8px;
  }
  .excel-congratulations {
    border: 2px solid #4CAF50;
    background: #e8f5e9;
    border-radius: 6px;
    padding: 15px 25px;
    margin: 10px 0 10px 0;
    max-width: 900px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    position: relative;
  }
  .excel-next-practice-btn {
    margin-top: 16px;
    background: #4CAF50;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 10px 28px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
  }
  .excel-next-practice-btn:hover {
    background: #388E3C;
  }
</style> 