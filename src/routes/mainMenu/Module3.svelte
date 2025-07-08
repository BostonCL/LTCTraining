<script lang="ts">
  import { onMount } from 'svelte';
  import Handsontable from 'handsontable';
  import 'handsontable/dist/handsontable.full.min.css';

  let container: HTMLDivElement;
  let hot: Handsontable | null = null;

  // Sample data for demonstration
  let data = [
    ['Unit', 'Advertiser', 'Start Time', 'End Time', 'Length (sec)', 'Notes'],
    ['A1', 'Geico', '12:00:00', '12:00:30', 30, ''],
    ['A2', 'Coke', '12:00:30', '12:01:00', 30, ''],
    ['A3', 'Pepsi', '12:01:00', '12:01:30', 30, ''],
    ['A4', 'Toyota', '12:01:30', '12:02:00', 30, ''],
  ];

  onMount(() => {
    hot = new Handsontable(container, {
      data,
      rowHeaders: true,
      colHeaders: true,
      width: '100%',
      height: 450,
      licenseKey: 'non-commercial-and-evaluation',
      manualRowMove: true,
      manualColumnMove: true,
      manualColumnResize: true,
      contextMenu: true,
      stretchH: 'none',
      className: 'htCenter',
      colWidths: [60, 120, 100, 100, 100, 200],
      minSpareRows: 10,
      minSpareCols: 0,
      rowHeights: 25,
      columnSorting: true,
      filters: true,
      dropdownMenu: true,
      afterChange: (changes, source) => {
        // Optionally handle changes here
      }
    });
    return () => hot?.destroy();
  });
</script>

<div class="excel-wrapper">
  <div class="excel-header">
    <h1 class="excel-title">Module 3: Marking down commercial times and Moving Units</h1>
    <p class="excel-subtitle">Below is an interactive Excel-like sheet. You can edit cells, drag rows, and use right-click for more options.</p>
  </div>
  
  <div class="excel-workspace">
    <div bind:this={container} class="excel-sheet"></div>
  </div>
</div>

<style>
  .excel-wrapper {
    background: #f0f0f0;
    min-height: 100vh;
    padding: 20px;
    font-family: 'Calibri', 'Segoe UI', sans-serif;
  }

  .excel-header {
    margin-bottom: 20px;
  }

  .excel-title {
    font-size: 20px;
    font-weight: 600;
    color: #1f1f1f;
    margin: 0 0 8px 0;
  }

  .excel-subtitle {
    font-size: 14px;
    color: #666;
    margin: 0;
  }

  .excel-workspace {
    background: #f0f0f0;
    border: 1px solid #c3c3c3;
  }

  .excel-sheet {
    background: white;
    border: 1px solid #c3c3c3;
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
</style> 