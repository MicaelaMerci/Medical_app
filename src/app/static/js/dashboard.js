// Dashboard: fetches /api/history and renders heart rate and SpO2 charts
let hrChart = null;
let spo2Chart = null;

// Limit devicePixelRatio to avoid oversized internal canvas scaling on some devices
if (window.Chart) {
  window.Chart.defaults.devicePixelRatio = Math.min(window.devicePixelRatio || 1, 2);
}

function createChart(ctx, label, color) {
  return new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: '',
        data: [],
        borderColor: color,
        backgroundColor: color + '33',
        fill: true,
        tension: 0.2,
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: label,
          color: '#222',
          align: 'center',
          padding: {
            top: 6,
            bottom: 6
          },
          font: {
            size: 18,
            weight: '600'
          }
        },
        legend: { display: false }
      },
      scales: {
        x: { display: true, ticks: { color: '#333', font: { size: 12 } } },
        y: { display: true, ticks: { color: '#333', font: { size: 12 } } }
      }
    }
  });
}

async function fetchHistoryAndUpdate() {
  try {
    const res = await fetch('/api/history');
    if (!res.ok) {
      console.warn('/api/history returned', res.status);
      return;
    }
    const data = await res.json();
    const labels = data.map(d => new Date(d.timestamp).toLocaleTimeString());
    const hrData = data.map(d => d.heart_rate);
    const spo2Data = data.map(d => d.blood_oxygen);

    if (!hrChart) {
      const hrCtx = document.getElementById('hrChart').getContext('2d');
      hrChart = createChart(hrCtx, 'Heart Rate (bpm)', 'rgb(220,20,60)');
      const spo2Ctx = document.getElementById('spo2Chart').getContext('2d');
      spo2Chart = createChart(spo2Ctx, 'Blood Oxygen (%)', 'rgb(30,144,255)');
    }

    hrChart.data.labels = labels;
    hrChart.data.datasets[0].data = hrData;
    hrChart.update();

    spo2Chart.data.labels = labels;
    spo2Chart.data.datasets[0].data = spo2Data;
    spo2Chart.update();
  } catch (err) {
    console.error('Error fetching history', err);
  }
}

// initial load and periodic refresh
fetchHistoryAndUpdate();
setInterval(fetchHistoryAndUpdate, 2000);
