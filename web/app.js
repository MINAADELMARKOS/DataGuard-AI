const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });

async function loadDashboard() {
  const response = await fetch('/api/dashboard');
  const data = await response.json();
  document.querySelector('#kpis').innerHTML = [
    ['Revenue at risk', money.format(data.estimated_revenue_at_risk_usd)],
    ['Open alerts', data.open_alerts],
    ['Critical alerts', data.critical_alerts],
    ['Feeds monitored', data.total_feeds],
  ].map(([label, value]) => `<div class="card"><small>${label}</small><strong>${value}</strong></div>`).join('');

  document.querySelector('#alerts').innerHTML = data.alerts.map(alert => `
    <div class="item">
      <div class="row"><strong>${alert.title}</strong><span class="badge ${alert.severity}">${alert.severity}</span></div>
      <p class="muted">${alert.description}</p>
      <p><strong>Estimated impact:</strong> ${money.format(alert.estimated_revenue_at_risk_usd)}</p>
      <p class="muted">Owner: ${alert.owner} · Confidence: ${alert.confidence}</p>
    </div>
  `).join('');

  document.querySelector('#feeds').innerHTML = data.feeds.map(feed => `
    <div class="item row">
      <div><strong>${feed.name}</strong><div class="muted">${feed.owner}</div></div>
      <strong class="${feed.status}">${feed.status}</strong>
    </div>
  `).join('');
}

loadDashboard();
