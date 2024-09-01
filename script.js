var map = L.map('map').setView([28.6139, 77.2090], 12); // Coordinates for Delhi

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
}).addTo(map);

async function fetchHotspots() {
    const response = await fetch('http://127.0.0.1:5000/api/hotspots');
    const data = await response.json();
    return data;
}

async function displayHotspots() {
    const hotspots = await fetchHotspots();
    hotspots.forEach(hotspot => {
        const marker = L.marker([hotspot.latitude, hotspot.longitude])
            .addTo(map)
            .bindPopup(`<b>Pollution Risk:</b> High<br><b>pH:</b> ${hotspot.ph}<br><b>Oxygen:</b> ${hotspot.dissolved_oxygen}`);
    });
}

async function fetchReports() {
    const response = await fetch('http://127.0.0.1:5000/api/reports');
    const data = await response.json();
    return data;
}

async function displayReports() {
    const reports = await fetchReports();
    const reportsList = document.getElementById('reportsList');
    reports.forEach(report => {
        const reportDiv = document.createElement('div');
        reportDiv.className = 'reportItem';
        reportDiv.innerHTML = `<b>Location:</b> ${report.location}<br><b>Description:</b> ${report.description}<br><b>Time:</b> ${report.timestamp}`;
        reportsList.appendChild(reportDiv);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    displayHotspots();
    displayReports();
});
