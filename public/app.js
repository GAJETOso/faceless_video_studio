
// State Management
const state = {
    activeTab: 'dashboard',
    terminalLines: []
};

// Navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
        const tab = item.getAttribute('data-tab');

        // Update UI
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');

        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        document.getElementById(`tab-${tab}`).classList.add('active');

        state.activeTab = tab;

        if (tab === 'library') {
            loadLibrary();
        }
    });
});

// Production API
const production = {
    niche: async (nicheName) => {
        logToTerminal(`[AUTOPILOT] Initializing discovery for niche: ${nicheName}...`);
        try {
            const response = await fetch('/api/produce/niche', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ niche: nicheName, count: 1 })
            });
            const data = await response.json();
            showNotification(`Autopilot engaged: ${nicheName}`);
            logToTerminal(`[ENGINE] ${data.status}`);
        } catch (err) {
            logToTerminal(`[ERROR] Failed to contact engine: ${err.message}`);
        }
    },

    custom: async () => {
        const title = document.getElementById('custom-title').value;
        const script = document.getElementById('custom-script').value;
        const style = document.getElementById('custom-style').value;
        const voice = document.getElementById('custom-voice').value;

        if (!title || !script) {
            alert("Please provide both a title and a script for production.");
            return;
        }

        logToTerminal(`[SYSTEM] Packaging custom script: "${title}"...`);
        try {
            const response = await fetch('/api/produce/custom', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, script, style, voice })
            });
            const data = await response.json();
            showNotification("Render Pipeline Initialized");
            logToTerminal(`[RENDERER] ${data.status}`);

            // Clear inputs
            document.getElementById('custom-title').value = '';
            document.getElementById('custom-script').value = '';
        } catch (err) {
            logToTerminal(`[ERROR] Render engine error: ${err.message}`);
        }
    }
};

// Library Logic
async function loadLibrary() {
    const listEl = document.getElementById('video-list');
    listEl.innerHTML = '<div class="loading">Sourcing branded content...</div>';

    try {
        const response = await fetch('/api/videos');
        const videos = await response.json();

        listEl.innerHTML = '';
        if (videos.length === 0) {
            listEl.innerHTML = '<div class="empty">No videos in production yet.</div>';
            return;
        }

        videos.forEach(v => {
            const sizeMB = (v.size / (1024 * 1024)).toFixed(2);
            const card = document.createElement('div');
            card.className = 'video-card';
            card.innerHTML = `
                <div class="v-icon">🎬</div>
                <div class="v-name">${v.name}</div>
                <div class="v-size">${sizeMB} MB | HD Render</div>
                <a href="${v.path}" download class="btn-niche" style="display:block; font-size: 12px; margin-top:10px;">Download Branded File</a>
            `;
            listEl.appendChild(card);
        });
    } catch (err) {
        listEl.innerHTML = `<div class="error">Failed to load library: ${err.message}</div>`;
    }
}

// Helpers
function logToTerminal(msg) {
    const terminal = document.getElementById('terminal-feed');
    const timestamp = new Date().toLocaleTimeString();
    const line = document.createElement('div');
    line.textContent = `[${timestamp}] ${msg}`;
    terminal.appendChild(line);
    terminal.scrollTop = terminal.scrollHeight;
}

function showNotification(msg) {
    const notif = document.getElementById('notification');
    notif.textContent = msg;
    notif.classList.add('show');
    setTimeout(() => notif.classList.remove('show'), 3000);
}
