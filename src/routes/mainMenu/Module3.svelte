<script lang="ts">
  import { onMount } from 'svelte';
  import Handsontable from 'handsontable';
  import 'handsontable/dist/handsontable.full.min.css';

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
  let colorTimeout: ReturnType<typeof setTimeout> | null = null;
  let colorsApplied = false;
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
      checkResult = '❌ Not quite! Make sure you wrote CUT in column A and filled the rest of the row in red for both green promo rows in SEG. 3.';
    }
  }

  let checkResult2 = '';
  function checkStep2() {
    // Find the two target rows by their unique values
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
      checkResult2 = '❌ Not quite! Make sure you wrote CUT in column A and filled the rest of the row in red for both target promo rows.';
    }
  }

  let checkResult3 = '';
  function checkStep3() {
    // Find the source row to copy
    const source = {
      time: '09:23:02 PM',
      eventType: 'Commercial',
      title: 'OLD TRAPPER : CAMPING CATASTROPHES',
      advertiser: 'OLD TRAPPER',
      houseNumber: '602584',
      orderedAs: 'ROS 24 HOUR',
      spotEndTime: '05:59:00 AM'
    };
    // Find the row to insert after
    const afterRowIdx = data.findIndex(row => row[1] === '09:33:40 PM' && row[2] && row[2].toLowerCase() === 'promo' && row[4] && row[4].toLowerCase() === 'mm sweet 16 thursday');
    if (afterRowIdx === -1) {
      checkResult3 = '❌ Could not find the MM SWEET 16 THURSDAY row.';
      return;
    }
    // The new row should be after afterRowIdx
    const newRowIdx = afterRowIdx + 1;
    // Check if the new row matches the source data (except for possible column A, which could be blank or CUT)
    const newRow = data[newRowIdx];
    if (!newRow) {
      checkResult3 = '❌ No new row found after MM SWEET 16 THURSDAY.';
      return;
    }
    // Check columns 1-8 (skip column 0)
    const matches =
      newRow[1] === source.time &&
      newRow[2] && newRow[2].toLowerCase() === source.eventType.toLowerCase() &&
      newRow[3] === '00:00:30' &&
      newRow[4] && newRow[4].toLowerCase() === source.title.toLowerCase() &&
      newRow[5] && newRow[5].toLowerCase() === source.advertiser.toLowerCase() &&
      newRow[6] === source.houseNumber &&
      newRow[7] === source.orderedAs &&
      newRow[8] === source.spotEndTime;
    if (!matches) {
      checkResult3 = '❌ The new row does not match the copied OLD TRAPPER row.';
      return;
    }
    // Check if all cells in the new row are filled blue
    let allBlue = true;
    for (let col = 0; col < newRow.length; col++) {
      const cellKey = `${newRowIdx}-${col}`;
      const color = (cellColors[cellKey] || '').toLowerCase();
      if (
        color !== '#0070c0' &&
        color !== 'rgb(0,112,192)' &&
        color !== '#00b0f0' &&
        color !== 'rgb(0,176,240)'
      ) {
        allBlue = false;
        break;
      }
    }
    if (!allBlue) {
      checkResult3 = '❌ The new row is not filled blue.';
      return;
    }
    checkResult3 = '✅ Correct! You copied and pasted the row and filled it blue.';
    setTimeout(() => { goToStep4(); }, 800); // Navigate to step 4 after short delay
  }

  let checkResult4 = '';
  function checkStep4() {
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
      checkResult4 = '❌ In the original OLD TRAPPER row, column A must say: moved to B1 of 9:30';
      return;
    }
    // Check column A of blue row
    const blueA = (data[blueIdx][0] || '').trim().toLowerCase();
    if (blueA !== 'moved from b3 of 9p.') {
      checkResult4 = '❌ In the new blue row, column A must say: moved from b3 of 9p.';
      return;
    }
    checkResult4 = '✅ Correct! You annotated both rows as required.';
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
              
              // Apply color directly to cell element
              const cellElement = hot?.getCell(row, col);
              if (cellElement) {
                cellElement.style.backgroundColor = selectedColor;
                cellElement.style.setProperty('background-color', selectedColor, 'important');
                cellElement.setAttribute('style', `background-color: ${selectedColor} !important`);
              }
            }
          }
        });
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

              // Clear color from cell element
              const cell = hot?.getCell(row, col);
              if (cell) {
                cell.style.backgroundColor = '';
                cell.style.removeProperty('background-color');
                cell.removeAttribute('style');
              }
            }
          }
        });
      }
    }
    showColorPicker = false;
  }

  function showCustomColor() {
    // For now, just close the picker. Could implement custom color picker later
    showColorPicker = false;
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
    ["Real Time", "Hit Time", "Event Type", "Length", "Title", "Advertiser", "House Number", "Ordered As", "Spot End Time"],
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
    ["", "09:22:22 PM", "Promo", "00:00:10", "REESES COLLEGE ASG APRIL 5", "CBS SPORTS NETWORK", "809797", "", ""],
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
      contextMenu: true,
      stretchH: 'none',
      className: '', // Remove 'htCenter' to left-align content
      colWidths: [80, 90, 80, 60, 400, 100, 100, 120, 100],
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
      afterRender: () => {
        // Use a flag to prevent multiple applications
        if (hot && !hot.isDestroyed && !colorsApplied) {
          colorsApplied = true;
          
          // Apply base colors first (event type colors)
          const eventTypeCol = 2;
          for (let row = 1; row < data.length; row++) {
            for (let col = 0; col < data[row].length; col++) {
              const cellKey = `${row}-${col}`;
              const cellElement = hot?.getCell(row, col);
              if (!cellElement) continue;
              
              // Skip if cell is cleared or has persistent color
              if (clearedCells.has(cellKey) || cellColors[cellKey]) continue;
              
              // Apply event type colors
              if (data[row][eventTypeCol]) {
                const eventType = data[row][eventTypeCol].toLowerCase();
                if (eventType === 'commercial' && col !== 0) {
                  cellElement.style.setProperty('background-color', '#FFFF00', 'important');
                  cellElement.style.removeProperty('color');
                } else if (eventType === 'local' && col !== 0) {
                  cellElement.style.setProperty('background-color', '#7030A0', 'important');
                  cellElement.style.setProperty('color', '#fff', 'important');
                } else if (eventType === 'program' && col !== 0) {
                  cellElement.style.setProperty('background-color', '#d9d9d9', 'important');
                  cellElement.style.setProperty('font-weight', 'bold', 'important');
                } else if (eventType === 'promo' && col !== 0) {
                  cellElement.style.setProperty('background-color', '#375623', 'important');
                  cellElement.style.setProperty('color', '#fff', 'important');
                }
              }
            }
          }
          
          // Apply persistent colors (user-applied colors)
          Object.keys(cellColors).forEach(cellKey => {
            if (clearedCells.has(cellKey)) {
              delete cellColors[cellKey];
              return;
            }
            const [row, col] = cellKey.split('-').map(Number);
            const cellElement = hot?.getCell(row, col);
            if (cellElement) {
              cellElement.style.setProperty('background-color', cellColors[cellKey], 'important');
              if (cellColors[cellKey] === '#375623' || cellColors[cellKey] === '#7030A0') {
                cellElement.style.setProperty('color', '#fff', 'important');
              }
            }
          });
          
          // Apply header styling (row 0)
          for (let col = 0; col < data[0].length; col++) {
            const cellElement = hot?.getCell(0, col);
            if (cellElement) {
              cellElement.style.setProperty('background-color', '#d9d9d9', 'important');
              cellElement.style.setProperty('color', '#0000ff', 'important');
              cellElement.style.setProperty('font-weight', 'bold', 'important');
            }
          }
          
          // Apply special column A styling
          for (let row = 1; row < data.length; row++) {
            const cellElement = hot?.getCell(row, 0);
            if (cellElement && typeof data[row][0] === 'string') {
              const cellValue = data[row][0].toLowerCase().trim();
              if (cellValue === 'start time' || cellValue === 'end time' || cellValue === 'start time 9:00:00') {
                cellElement.style.setProperty('background-color', '#d9d9d9', 'important');
                cellElement.style.setProperty('color', '#0000ff', 'important');
                cellElement.style.setProperty('font-weight', 'bold', 'important');
              } else if (!cellColors[`${row}-0`] && !clearedCells.has(`${row}-0`)) {
                cellElement.style.setProperty('background-color', '#fff', 'important');
                cellElement.style.removeProperty('color');
              }
            }
          }
        }
      },
      cells: (row, col, prop) => {
        // This allows for custom cell styling
        return {
          className: ''
        };
      }
    });
    
    hot.render();
    return () => hot?.destroy();
  });
</script>

<!-- Remove Step 2 Navigation Popup -->

<div class="excel-wrapper">
  <div class="excel-instructions">
    {#if !showStep1 && !showStep2 && !showStep3 && !showStep4}
      <div class="flex justify-between items-center mb-1">
        <div></div>
        <button class="excel-nav-btn excel-nav-btn-next" aria-label="Go to Step 1" on:click={goToStep1}>
          Next →
        </button>
      </div>
      <h1 class="excel-instructions-title">Interactive Live Coverage Sheet</h1>
      <p class="excel-subtitle">Below is an interactive live coverage sheet. You can edit cells, drag rows, and use right-click for more options.</p>
      <h2 class="excel-instructions-subtitle">Instructions</h2>
      <div class="excel-instructions-body">
        The producer wants to cut 1 minute from break 3. Perform the actions to do this on the interactive excel sheet!
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
        <div class="excel-step-hint">Look for any <span class="excel-green">Green Promo</span> in SEG. 3 which is unsold inventory to <span class="excel-red">CUT</span>.</div>
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
          Find <b>30 more seconds</b> to cut, still focusing on the event type <span class="excel-green">Promo</span>.<br>
          <br>
          <b>Instructions:</b> CUT two more promos by filling them in <span class="excel-red">Red</span> and writing <span class="excel-red">CUT</span> next to them in column A.
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
          Copy the row with <b>09:23:02 PM</b> Commercial <i>OLD TRAPPER : CAMPING CATASTROPHES</i>.<br>
          Add a new row directly under <b>09:33:40 PM</b> Promo <i>MM SWEET 16 THURSDAY</i>.<br>
          Paste the copied row’s data into the new row.<br>
          Fill the new row <span style="color:#0070c0;font-weight:bold">Blue</span>.
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
          In the original <b>09:23:02 PM</b> Commercial <i>OLD TRAPPER : CAMPING CATASTROPHES</i> row, write in column A: <b>moved to B1 of 9:30</b>.<br>
          In the new blue row you added, write in column A: <b>moved from b3 of 9p.</b>
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
              <button type="button" class="excel-color-item" style="background-color: #0070C0" aria-label="Fill blue" on:click={() => pickColor('#0070C0')}></button>
              <button type="button" class="excel-color-item" style="background-color: #FFFF00" aria-label="Fill yellow" on:click={() => pickColor('#FFFF00')}></button>
              <button type="button" class="excel-color-item" style="background-color: #7030A0" aria-label="Fill magenta" on:click={() => pickColor('#7030A0')}></button>
              <button type="button" class="excel-color-item" style="background-color: #00B0F0" aria-label="Fill cyan" on:click={() => pickColor('#00B0F0')}></button>
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

  .excel-subtitle {
    font-size: 14px;
    color: #666;
    margin: 0 0 12px 0;
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

  .excel-green {
    color: #375623;
    font-weight: bold;
  }
  .excel-red {
    color: #E53E3E;
    font-weight: bold;
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
</style> 