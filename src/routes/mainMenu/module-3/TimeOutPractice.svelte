<script lang="ts">
import { onMount } from 'svelte';
import Handsontable from 'handsontable';
import 'handsontable/dist/handsontable.full.min.css';
import { createEventDispatcher } from 'svelte';

const dispatch = createEventDispatcher();

// Props
export let nextButtonText: string = "Next";

function handleNext() {
  dispatch('navigateToNextSubmodule');
}

let container: HTMLDivElement;
let hot: Handsontable | null = null;

let data = [
  ["Real Time", "Hit Time", "Event Type", "Length", "Title", "Advertiser", "House Number", "Ordered As", "Spot End Time"],
  ["", "08:50:00 PM", "Program", "00:45:00", "USL P1 [USL: First Round Match TBD - 11/3/24_8p]: SEG. 5", "", "327335", "", ""],
  ["", "09:35:00 PM", "Commercial", "00:00:15", "PEPSI (MOUNTAIN DEW): MTD T&R BAJA :15", "PEPSI", "600701", "ROS 24 HOUR", "05:59:00 AM"],
  ["", "09:35:15 PM", "Commercial", "00:00:30", "DRAFT KINGS: *NFL APPROVED* DRAFTKINGS / TD CELEBRATION ALL SB STATES BET 5 GET 200 LINEAR 1 - CBS + ESPN / QUARTER", "DRAFT KINGS", "600544", "STUDIO ENCORE", "05:59:00 AM"],
  ["", "09:35:45 PM", "Commercial", "00:00:30", "VERIZON: NPI202430S6X9SUSTAIN IPHONE 16 PRO IPADCCNC", "VERIZON", "601337", "STUDIO ENCORE", "05:59:00 AM"],
  ["", "09:36:15 PM", "Commercial", "00:00:15", "STANLEY STEEMER: AD EXPERT V2-15", "STANLEY STEEMER", "601124", "UNITED SOCCER LEAGUE", "05:59:00 AM"],
  ["", "09:36:30 PM", "Local", "Local", "Local", "Local", "Local", "Local", "Local"],
  ["", "09:38:00 PM", "Program", "00:17:30", "USL P1 [USL: First Round Match TBD - 11/3/24_8p]: SEG. 6", "", "327336", "", ""],
  ["", "09:55:30 PM", "Promo", "00:00:20", "UEFA MD4 THURSDAY", "CBS SPORTS NETWORK", "801865", "", ""],
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
  ["", "10:07:40 PM", "Promo", "00:00:20", "NWSL PERFECT STADIUM", "CBS SPORTS NETWORK", "802620", "", ""],
  ["", "10:08:00 PM", "Program", "00:06:00", "Volleyball Special Event R5 [AVP Beach Volleyball: AVP League - Week 8]: SEG. 2", "", "327342", "", ""],
  ["", "10:14:00 PM", "National DR", "00:00:30", "TRUST & WILL: MEET TRUST AND WILL II 30", "TRUST & WILL", "604177", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:14:30 PM", "National DR", "00:00:30", "DEALDASH, INC: DD REAL DEALS 2023 NEW TESTIMONIAL :30/DEALDASH.COM", "DEALDASH, INC", "607056", "DR ROS PRIME", "12:00:00 AM"],
  ["", "10:15:00 PM", "Local", "Local", "Local", "Local", "Local", "Local", "Local"],
  ["", "10:16:30 PM", "Program", "00:07:00", "Volleyball Special Event R5 [AVP Beach Volleyball: AVP League - Week 8]: SEG. 3", "", "327343", "", ""],
  ["", "10:23:30 PM", "National DR", "00:01:00", "BOSLEY: NOT 1970 QR 60", "BOSLEY", "606670", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:24:30 PM", "National DR", "00:00:30", "MIZUHO AMERICAS: MWW MIZUHO AMERICAS PAR 3", "MIZUHO AMERICAS", "600884", "DR 24 HOUR ROS", "11:59:00 PM"],
  ["", "10:25:00 PM", "Program", "00:09:30", "Volleyball Special Event R5 [AVP Beach Volleyball: AVP League - Week 8]: SEG. 4", "", "327344", "", ""],
  ["", "10:34:30 PM", "Promo", "00:00:10", "CBB WICHITA ST VS W KENTUCKY TOM", "CBS SPORTS NETWORK", "802340", "", ""],
  ["", "10:34:40 PM", "National DR", "00:00:30", "FINANCEBUZZ: TWO MINUTES 30", "FINANCEBUZZ", "600655", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:35:10 PM", "National DR", "00:00:30", "TRUST & WILL: KIDS 30", "TRUST & WILL", "609802", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:35:40 PM", "National DR", "00:00:15", "GRAINGER: MOVING FORWARD 15", "GRAINGER", "600619", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:35:55 PM", "National DR", "00:00:30", "DEALDASH, INC: DD REAL DEALS 2023 NEW TESTIMONIAL :30/DEALDASH.COM", "DEALDASH, INC", "607056", "DR ROS PRIME", "12:00:00 AM"],
  ["", "10:36:25 PM", "National DR", "00:00:15", "INSTACART: IC-LINEAR-15S-EVERGREEN-BTS-BUNNYEARS STRATID-01", "INSTACART", "607537", "DR ROS PRIME", "12:00:00 AM"],
  ["", "10:36:40 PM", "Promo", "00:00:20", "LGBTQ FLAG FOOTBALL", "CBS SPORTS NETWORK", "809378", "", ""],
  ["", "10:37:00 PM", "Program", "00:05:00", "Volleyball Special Event R5 [AVP Beach Volleyball: AVP League - Week 8]: SEG. 5", "", "327345", "", ""],
  ["", "10:42:00 PM", "National DR", "00:00:30", "NIC INDUSTRIES: CERAKOTE TRIM COAT DRIVE TO RETAIL", "NIC INDUSTRIES", "601012", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:42:30 PM", "National DR", "00:00:15", "LUME : STARTER PACK NECKROLL - JACOB - SHOPMANDO - DEAL - V1", "LUME", "609735", "DR ROS PRIME", "12:00:00 AM"],
  ["", "10:42:45 PM", "National DR", "00:00:15", "DEALDASH, INC: DD REAL DEALS 2023 NEW TESTIMONIAL :15", "DEALDASH, INC", "607700", "DR ROS PRIME", "12:00:00 AM"],
  ["", "10:43:00 PM", "National DR", "00:00:30", "GRAINGER: THE EXTRAORDINARY 30", "GRAINGER", "607121", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:43:30 PM", "National DR", "00:00:15", "TRUST & WILL: KIDS 15", "TRUST & WILL", "607216", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:43:45 PM", "National DR", "00:00:15", "HARRY'S USA, INC.: HARRY'S MASH UP :15", "HARRY'S USA, INC.", "601702", "DR ROS PRIME", "12:00:00 AM"],
  ["", "10:44:00 PM", "National DR", "00:01:00", "CREDIT ASSOCIATES: THE PROGRAM 60", "CREDIT ASSOCIATES", "601357", "DR ROS PRIME", "12:00:00 AM"],
  ["", "10:45:00 PM", "National DR", "00:00:30", "GUSTO INC: TOP CAT :30", "GUSTO INC", "601067", "DR 24 HOUR ROS", "05:58:00 AM"],
  ["", "10:45:30 PM", "Program", "00:08:00", "Volleyball Special Event R5 [AVP Beach Volleyball: AVP League - Week 8]: SEG. 6", "", "327346", "", ""],
  ["", "10:53:30 PM", "National DR", "00:01:00", "BOSLEY: NOT 1970 QR TFN 60", "BOSLEY", "601231", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:54:30 PM", "National DR", "00:00:30", "GORJANA: GORJANA HOLIDAY 30", "GORJANA", "601354", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:55:00 PM", "National DR", "00:00:15", "TRUST & WILL: MATHEW AND KELLY RV OFFER TRWL 15", "TRUST & WILL", "607212", "DR ROS PRIME", "11:00:00 PM"],
  ["", "10:55:15 PM", "National DR", "00:00:15", "INSTACART: IC-LINEAR-15S-EVERGREEN-BTS-BUNNYEARS STRATID-01", "INSTACART", "607537", "DR ROS PRIME", "12:00:00 AM"],
  ["", "10:55:30 PM", "Local", "Local", "Local", "Local", "Local", "Local", "Local"],
  ["", "10:57:00 PM", "Program", "00:05:00", "Volleyball Special Event R5 [AVP Beach Volleyball: AVP League - Week 8]: SEG. 7", "", "327347", "", ""],
  ["", "11:02:00 PM", "Promo", "00:00:15", "UCL MD4 TUES & WED", "CBS SPORTS NETWORK", "802350", "", ""]
];

let selectedColor = '#F2DCDB'; // Default light red
let showColorPicker = false;
let colorTimeout: ReturnType<typeof setTimeout> | null = null;
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

// --- Step check state (placeholders) ---
let checkResult1 = '';
let checkResult2 = '';

function checkStep1() {
  // Find the BOSLEY and CREDIT ASSOCIATES rows
  const bosleyIdx = data.findIndex(row => row[1] === '10:23:30 PM' && row[2] && row[2].toLowerCase() === 'national dr' && row[4] && row[4].toLowerCase().includes('bosley'));
  const creditIdx = data.findIndex(row => row[1] === '10:44:00 PM' && row[2] && row[2].toLowerCase() === 'national dr' && row[4] && row[4].toLowerCase().includes('credit associates'));
  let bosleyCut = false, bosleyRed = false, creditCut = false, creditRed = false;
  // Check BOSLEY row
  if (bosleyIdx !== -1) {
    bosleyCut = typeof data[bosleyIdx][0] === 'string' && data[bosleyIdx][0].trim().toLowerCase() === 'cut';
    for (let col = 1; col < data[bosleyIdx].length; col++) {
      const cellKey = `${bosleyIdx}-${col}`;
      const color = (cellColors[cellKey] || '').toLowerCase();
      if (color === '#e53e3e' || color === '#ff0000' || color === 'rgb(229,62,62)' || color === 'rgb(255,0,0)') {
        bosleyRed = true;
        break;
      }
    }
  }
  // Check CREDIT ASSOCIATES row
  if (creditIdx !== -1) {
    creditCut = typeof data[creditIdx][0] === 'string' && data[creditIdx][0].trim().toLowerCase() === 'cut';
    for (let col = 1; col < data[creditIdx].length; col++) {
      const cellKey = `${creditIdx}-${col}`;
      const color = (cellColors[cellKey] || '').toLowerCase();
      if (color === '#e53e3e' || color === '#ff0000' || color === 'rgb(229,62,62)' || color === 'rgb(255,0,0)') {
        creditRed = true;
        break;
      }
    }
  }
  if (bosleyCut && bosleyRed && creditCut && creditRed) {
    checkResult1 = '✅ Correct! You CUT and color-filled both 1-minute National DR rows red.';
  } else {
    checkResult1 = '❌ Not quite! Make sure you write CUT in column A and fill at least one cell in both rows red.';
  }
}
let emailText = '';
function checkStep2() {
  checkResult2 = 'show';
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
        const startRow = Math.min(range[0], range[2]);
        const endRow = Math.max(range[0], range[2]);
        const startCol = Math.min(range[1], range[3]);
        const endCol = Math.max(range[1], range[3]);
        for (let row = startRow; row <= endRow; row++) {
          for (let col = startCol; col <= endCol; col++) {
            const cellKey = `${row}-${col}`;
            delete cellColors[cellKey];
            clearedCells.add(cellKey);
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
  showColorPicker = false;
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
    contextMenu: true,
    stretchH: 'none',
    className: '',
    colWidths: [120, 90, 80, 60, 400, 100, 100, 120, 100],
    minSpareRows: 0,
    minSpareCols: 0,
    rowHeights: 25,
    columnSorting: true,
    filters: true,
    dropdownMenu: true,
    selectionMode: 'range',
    outsideClickDeselects: false,
    afterRender: () => {
      // Only apply colors if not already applied to prevent flickering
      if (hot && !hot.isDestroyed) {
        
        // Apply base colors first (event type colors)
        const eventTypeCol = 2;
        for (let row = 1; row < data.length; row++) {
          for (let col = 0; col < data[row].length; col++) {
            const cellKey = `${row}-${col}`;
            const cellElement = hot?.getCell(row, col);
            if (!cellElement) continue;
            
            // Skip if cell is cleared or has persistent color
            if (clearedCells.has(cellKey) || cellColors[cellKey]) continue;
            
            // Check if color is already applied to prevent re-application
            const currentBgColor = cellElement.style.backgroundColor;
            if (currentBgColor && currentBgColor !== 'rgba(0, 0, 0, 0)' && currentBgColor !== 'transparent') continue;
            
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
              } else if (eventType === 'national dr' && col !== 0) {
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
            if (cellValue === 'start time' || cellValue === 'end time' || cellValue === 'end time 10:02:00') {
              cellElement.style.setProperty('background-color', '#d9d9d9', 'important');
              cellElement.style.setProperty('color', '#0000ff', 'important');
              cellElement.style.setProperty('font-weight', 'bold', 'important');
            } else if (!cellColors[`${row}-0`] && !clearedCells.has(`${row}-0`)) {
              cellElement.style.setProperty('background-color', '#fff', 'important');
              cellElement.style.removeProperty('color');
            }
          }
        }
        
        // Style End Time's 10:02:00 cell blue
        const endTimeCell = hot?.getCell(13, 1);
        if (endTimeCell && data[13][0] && data[13][0].toLowerCase().trim() === 'end time') {
          endTimeCell.style.setProperty('color', '#0000ff', 'important');
          endTimeCell.style.setProperty('font-weight', 'bold', 'important');
        }
        
        // Style cell 13-1 with white text
        const endTimeWhiteCell = hot?.getCell(13, 1);
        if (endTimeWhiteCell && data[13][1] === '09:57:50 PM') {
          endTimeWhiteCell.style.setProperty('color', '#fff', 'important');
          endTimeWhiteCell.style.setProperty('font-weight', 'bold', 'important');
        }
      }
    }
  });
  return () => hot?.destroy();
});
</script>

<div class="excel-wrapper">
  <div class="excel-instructions">
    {#if intro}
      <div class="flex justify-between items-center mb-1">
        <div></div>
        <button class="excel-nav-btn excel-nav-btn-next" aria-label="Go to Step 1" on:click={goToStep1}>
          Next →
        </button>
      </div>
      <h1 class="excel-instructions-title">Time Out Practice</h1>
      <p class="excel-subtitle">Practice time out scenarios using the interactive Excel sheet below.</p>
      <h2 class="excel-instructions-subtitle">Instructions</h2>
      <div class="excel-instructions-body">
        The Game went over by 2 minutes! The End Time for the 8:00pm game was 10:02:00
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
        <div class="excel-step-hint">Find 2 minutes to Cut!<br>Look for units from the 10:00:00pm game with the largest length to CUT</div>
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
        <button class="excel-nav-btn excel-nav-btn-prev" aria-label="Back to Step 1" on:click={goToStep1}>
          ← Previous
        </button>
        <div></div>
      </div>
      <h2 class="excel-instructions-title">Step 2</h2>
      <div class="excel-instructions-body">
        <div class="excel-step-hint">Write the email to Master Control explaining what happened!</div>
        <textarea
          bind:value={emailText}
          rows="6"
          style="width:100%;margin-bottom:10px;font-size:1rem;padding:8px;border-radius:4px;border:1px solid #ccc;resize:vertical;"
          placeholder="Type your practice email here..."
        ></textarea>
        <button class="excel-check-btn" on:click={checkStep2}>Check</button>
        {#if checkResult2 === 'show'}
          <div class="excel-email-compare-wrapper">
            <div class="excel-email-compare-col">
              <div class="excel-email-compare-title">Your Email</div>
              <pre class="excel-email-compare-content">{emailText}</pre>
            </div>
            <div class="excel-email-compare-col">
              <div class="excel-email-compare-title">Reference Email</div>
              <pre class="excel-email-compare-content">Here is 2 mins worth of units we can cut in the overnight to get us back on time.

10PM Game
Break 3
CUT: 606670

Break 4
CUT: 601357</pre>
            </div>
          </div>
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
  
  <!-- Navigation Button -->
  <div style="text-align: center; margin-top: 20px; padding: 20px;">
    <button 
      class="excel-step2-next-btn" 
      on:click={handleNext}
      style="background-color: #0074D9; color: white; padding: 12px 24px; border: none; border-radius: 6px; font-size: 1rem; font-weight: bold; cursor: pointer; transition: background-color 0.3s ease;"
    >
      {nextButtonText}
    </button>
  </div>
</div>

<style>
/* Copy all styles from UnitCutPractice.svelte */
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
  /* New styles for step-based instructions */
  .excel-step-hint {
    font-size: 1rem;
    color: #333;
    margin-bottom: 10px;
    font-weight: bold;
  }
  .excel-check-btn {
    background-color: #0074D9;
    color: white;
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: bold;
    transition: background-color 0.3s ease;
  }
  .excel-check-btn:hover {
    background-color: #0056b3;
  }
  .excel-check-result {
    font-size: 0.9rem;
    color: #222;
    margin-top: 10px;
    padding: 8px;
    border-radius: 4px;
    background-color: #e0f7fa;
    border: 1px solid #b2ebf2;
  }
  .excel-step2-next-btn {
    background-color: #4CAF50;
    color: white;
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    font-weight: bold;
    transition: background-color 0.3s ease;
    margin-top: 16px;
  }
  .excel-step2-next-btn:hover {
    background-color: #388e3c;
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