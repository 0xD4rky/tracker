document.addEventListener('DOMContentLoaded', function() {
    const videoFeed = document.getElementById('video-feed');
    const startBtn = document.getElementById('start-btn');
    const stopBtn = document.getElementById('stop-btn');
    const trackingStatus = document.getElementById('tracking-status');
    const coordX = document.getElementById('coord-x');
    const coordY = document.getElementById('coord-y');
    const normX = document.getElementById('norm-x');
    const normY = document.getElementById('norm-y');

    let isTracking = true;

    function updateTrackingStatus(status) {
        trackingStatus.textContent = status;
        trackingStatus.style.color = status === 'Tracking' ? '#27ae60' : '#c0392b';
    }

    function startTracking() {
        if (!isTracking) {
            videoFeed.src = "{{ url_for('video_feed') }}";
            isTracking = true;
            updateTrackingStatus('Tracking');
        }
    }

    function stopTracking() {
        if (isTracking) {
            videoFeed.src = "";
            isTracking = false;
            updateTrackingStatus('Stopped');
            resetCoordinates();
        }
    }

    function resetCoordinates() {
        coordX.textContent = '0';
        coordY.textContent = '0';
        normX.textContent = '0.00';
        normY.textContent = '0.00';
    }

    startBtn.addEventListener('click', startTracking);
    stopBtn.addEventListener('click', stopTracking);

    // This function would be called by your backend to update coordinates
    // You'll need to implement a way to send this data from your Python backend
    // One way could be using Server-Sent Events or WebSockets
    function updateCoordinates(x, y, nx, ny) {
        coordX.textContent = x;
        coordY.textContent = y;
        normX.textContent = nx.toFixed(2);
        normY.textContent = ny.toFixed(2);
    }

    // Example of how you might use Server-Sent Events to receive updates
    // You'll need to implement the corresponding endpoint in your Flask app
    const evtSource = new EventSource("{{ url_for('coordinate_stream') }}");
    evtSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        updateCoordinates(data.x, data.y, data.nx, data.ny);
    };
});