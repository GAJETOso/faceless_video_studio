// State Management
const state = {
    activeTab: 'dashboard',
    activeMode: 'short',
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

        if (tab === 'dashboard') {
            stats.load();
            dashboard.load();
        }
        if (tab === 'library') loadLibrary();
        if (tab === 'settings') settings.load();
        if (tab === 'analytics') analytics.load();
    });
});

// Stats & Analytics
const stats = {
    load: async () => {
        try {
            const response = await fetch('/api/videos');
            const videos = await response.json();

            // Update Stats
            document.getElementById('stat-total').textContent = videos.length;
            document.getElementById('stat-reach').textContent = (videos.length * 2.5).toFixed(1) + 'k';

            // Update Cinema Feed with LATEST video
            if (videos.length > 0) {
                const latest = videos[0]; // Assuming first is latest
                const player = document.getElementById('live-preview');
                player.src = `/exports/${latest.name}`;
                document.getElementById('preview-title').textContent = `Now Playing: ${latest.name}`;

                // Mock Sentiment Update
                const directives = [
                    "Strong demand for High-Stakes Finance hooks in Gen Z demographics.",
                    "Viewers requesting more 'Mystery of the Silk Road' deep dives.",
                    "Viral sentiment spike for 'AI Surveillance' controversy angles.",
                    "Retention high on 4K grain-textured documentary styles."
                ];
                document.getElementById('stat-sentiment').textContent = directives[Math.floor(Math.random() * directives.length)];
            }
        } catch (err) { console.error(err); }
    }
};

const dashboard = {
    load: () => {
        logToTerminal("[SYSTEM] Hub online. Syncing with world pulse...");
        dashboard.fetchNews();
        dashboard.fetchPivot();
        setInterval(dashboard.fetchNews, 60000); // Sync every minute
        setInterval(dashboard.fetchPivot, 300000); // Sync every 5 minutes
    },

    fetchNews: async () => {
        try {
            const res = await fetch('/api/news/trending');
            const news = await res.json();
            dashboard.renderNews(news);
        } catch (err) { console.error("Pulse sync failed", err); }
    },

    fetchPivot: async () => {
        try {
            const res = await fetch('/api/analytics/pivot');
            const data = await res.json();
            const el = document.getElementById('pivot-recommendation');
            if (typeof data === 'string') {
                el.innerHTML = data;
            } else {
                el.innerHTML = `<strong>${data.recommended_pivot}</strong><br>${data.rationale}<br><small>Confidence: ${data.confidence_score || data.confidence}</small>`;
            }
        } catch (err) { console.error("Pivot analysis failed", err); }
    },

    renderNews: (news) => {
        const list = document.getElementById('news-list');
        list.innerHTML = news.map(item => `
            <div class="news-item" onclick="dashboard.useNewsItem('${item.title}')">
                <div>
                    <div class="news-title">${item.title}</div>
                    <div class="news-niche">${item.niche}</div>
                </div>
                <div class="urgency-badge ${item.urgency.toLowerCase()}">${item.urgency}</div>
            </div>
        `).join('');
    },

    useNewsItem: (title) => {
        document.getElementById('custom-title').value = title;
        document.querySelector('[data-tab="production"]').click();
        logToTerminal(`[STRATEGY] Breaking opportunity loaded: "${title}"`);
    }
};

const analytics = {
    load: async () => {
        logToTerminal(`[SYSTEM] Calculating studio performance metrics...`);
        analytics.fetchCalendar();
        analytics.fetchHealth();
        try {
            const response = await fetch('/api/videos');
            const videos = await response.json();

            // Simple Bar Chart Logic (Rendering mock bars based on count)
            const chart = document.getElementById('velocity-chart');
            chart.innerHTML = '';
            for (let i = 0; i < 7; i++) {
                const bar = document.createElement('div');
                bar.className = 'bar';
                const h = Math.floor(Math.random() * 80) + 20;
                bar.style.height = `${h}%`;
                chart.appendChild(bar);
            }

            // Production Ledger
            const ledger = document.getElementById('production-ledger');
            ledger.innerHTML = videos.slice(0, 5).map(v => `
                <div style="margin-bottom:5px; border-bottom:1px solid #222; padding-bottom:5px;">
                    <span style="color:var(--accent-gold)">[HD EXPORT]</span> ${v.name} (${(v.size / 1024 / 1024).toFixed(1)}MB)
                </div>
            `).join('');

        } catch (err) { console.error(err); }
    },

    fetchHealth: async () => {
        try {
            const res = await fetch('/api/analytics/health');
            const data = await res.json();
            analytics.renderHealth(data);
        } catch (err) { console.error(err); }
    },

    renderHealth: (data) => {
        document.getElementById('health-total-views').textContent = data.total_views.toLocaleString();
        document.getElementById('health-retention').textContent = data.avg_retention + "%";
        document.getElementById('health-viral').textContent = data.viral_coefficient;

        const platformEl = document.getElementById('platform-health');
        platformEl.innerHTML = Object.entries(data.platforms).map(([name, stats]) => `
            <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; border: 1px solid var(--glass-border);">
                <div style="font-size: 10px; color: var(--accent-gold); text-transform: uppercase;">${name}</div>
                <div style="font-size: 18px; font-weight: 800; color: #fff; margin: 5px 0;">${stats.views.toLocaleString()}</div>
                <div style="font-size: 11px; color: var(--accent-cyan);">${stats.growth} Growth</div>
            </div>
        `).join('');
    },

    fetchCalendar: async () => {
        try {
            const res = await fetch('/api/calendar/current');
            const data = await res.json();
            if (data.days) analytics.renderCalendar(data.days);
            else document.getElementById('calendar-view').innerHTML = '<div class="empty">No active strategy. Click Generate to plan your week.</div>';
        } catch (err) { console.error(err); }
    },

    generateCalendar: async () => {
        logToTerminal(`[STRATEGY] AI is analyzing viral trends and niches...`);
        document.getElementById('calendar-view').innerHTML = '<div class="loading">Orchestrating week...</div>';
        try {
            const res = await fetch('/api/calendar/generate', { method: 'POST' });
            const data = await res.json();
            analytics.renderCalendar(data.plan.days);
            showNotification("Strategy Generated");
            logToTerminal(`[STRATEGY] New 7-day plan successfully calculated.`);
        } catch (err) {
            logToTerminal(`[ERROR] AI strategy session failed.`);
        }
    },

    runBulkProduction: async () => {
        logToTerminal(`[BULK] Initializing background render for the entire week...`);
        try {
            const res = await fetch('/api/produce/bulk', { method: 'POST' });
            const data = await res.json();
            showNotification("Bulk Production Started");
            logToTerminal(`[SYSTEM] Full-week render sequence initiated. Monitor logs for individual progress.`);
        } catch (err) {
            logToTerminal(`[ERROR] Failed to start bulk production.`);
        }
    },

    renderCalendar: (days) => {
        const view = document.getElementById('calendar-view');
        view.innerHTML = days.map(day => `
            <div class="day-card" onclick="analytics.useStrategicTopic('${day.niche}', '${day.topic}')">
                <h4>${day.day}</h4>
                <div class="niche-tag">${day.niche}</div>
                <div class="topic-preview">${day.topic}</div>
            </div>
        `).join('');
    },

    useStrategicTopic: (niche, topic) => {
        document.getElementById('custom-title').value = topic;
        document.querySelector('[data-tab="production"]').click();
        logToTerminal(`[SYSTEM] Loaded strategic topic: "${topic}" into production engine.`);
    }
};

// Production Modes Toggle
const modes = ['short', 'long', 'music'];
modes.forEach(mode => {
    const btn = document.getElementById(`mode-${mode}`);
    if (btn) {
        btn.addEventListener('click', () => {
            state.activeMode = mode;
            document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            logToTerminal(`[SYSTEM] Production mode switched to: ${mode.toUpperCase()}`);
        });
    }
});

document.getElementById('start-production-btn').addEventListener('click', () => production.initialize());

// Production API
const production = {
    initialize: () => {
        logToTerminal("[SYSTEM] Analyzing production parameters...");
        if (state.activeMode === 'long') production.long();
        else if (state.activeMode === 'music') production.music();
        else production.custom();
    },

    music: async () => {
        const title = document.getElementById('custom-title').value;
        const genre = prompt("Enter music genre (e.g. hip-hop, cinematic, cyberpunk):", "hip-hop");

        if (!title) return alert("Please enter a title/topic for the song.");

        logToTerminal(`[MUSIC] Initiating Music Video production for: "${title}" (${genre})...`);
        try {
            const res = await fetch('/api/produce/music', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic: title, genre: genre })
            });
            showNotification("Music Video Production Started");
        } catch (err) { logToTerminal(`[ERROR] Music studio failed.`); }
    },

    intl: async () => {
        const title = document.getElementById('custom-title').value;
        const script = document.getElementById('custom-script').value;
        const style = document.getElementById('custom-style').value;
        const voice = document.getElementById('custom-voice').value;
        const structure = document.getElementById('custom-structure').value;

        if (!title || !script) return showNotification("Title & Script required");

        logToTerminal(`[GLOBAL] Initializing 5-language dubbing sequence for: "${title}"`);
        try {
            const res = await fetch('/api/produce/intl', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, script, style, voice, structure })
            });
            showNotification("Global Broadcast Sequence Started");
        } catch (err) { logToTerminal(`[ERROR] Global broadcast failed.`); }
    },

    test: async () => {
        const title = document.getElementById('custom-title').value;
        const script = document.getElementById('custom-script').value;

        if (!title) return alert("Please enter a title for the angle test.");

        logToTerminal(`[OPTIMIZATION] running demographic angle test for: "${title}"...`);
        try {
            const response = await fetch('/api/produce/test', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ title, script, style: 'cinematic_documentary', voice: 'onyx' })
            });
            const data = await response.json();
            logToTerminal(`[SUCCESS] ${data.status}`);
            showNotification("Angle Test Running in Background");
        } catch (err) { logToTerminal(`[ERROR] Angle test failed.`); }
    },

    designHook: async () => {
        const title = document.getElementById('custom-title').value;
        if (!title) return alert("Enter a title to design a hook for.");

        logToTerminal(`[DESIGN] Generating 5s CGI Super Hook blueprint...`);
        try {
            const res = await fetch('/api/produce/intro-hook', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic: title })
            });
            const data = await res.json();
            document.getElementById('hook-design-output').style.display = 'block';
            document.getElementById('hook-design-text').textContent = data.design;
            showNotification("CGI Hook Designed");
        } catch (err) { logToTerminal(`[ERROR] Design engine failed.`); }
    },

    planSeries: async () => {
        const title = document.getElementById('custom-title').value;
        if (!title) return alert("Enter a topic/title to plan a trilogy for.");

        logToTerminal(`[SERIES] Architecting 3-Part Documentary Arc...`);
        try {
            const res = await fetch('/api/produce/series-plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic: title })
            });
            const data = await res.json();
            const plan = data.plan;

            let html = "";
            if (plan.part_1) {
                html += `PART 1: ${plan.part_1.title}\nSynopsis: ${plan.part_1.synopsis}\n\n`;
                html += `PART 2: ${plan.part_2.title}\nSynopsis: ${plan.part_2.synopsis}\n\n`;
                html += `PART 3: ${plan.part_3.title}\nSynopsis: ${plan.part_3.synopsis}`;
            } else {
                html = JSON.stringify(plan, null, 2);
            }

            document.getElementById('series-plan-output').style.display = 'block';
            document.getElementById('series-plan-text').textContent = html;
            showNotification("Trilogy Arc Planned");
        } catch (err) { logToTerminal(`[ERROR] Series planner failed.`); }
    },

    testThumbnails: async () => {
        const title = document.getElementById('custom-title').value;
        if (!title) return alert("Enter a topic to test thumbnails for.");

        logToTerminal(`[A/B TEST] Generating Dual Thumbnail Concepts...`);
        try {
            const res = await fetch('/api/produce/thumbnail-ab', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic: title })
            });
            const data = await res.json();
            const concepts = data.concepts;

            const grid = document.getElementById('thumb-ab-grid');
            grid.innerHTML = `
                <div style="background: #111; padding: 10px; border: 1px solid #333;">
                    <strong style="color: var(--accent-cyan);">CONCEPT A: ${concepts.concept_a.type}</strong>
                    <div style="margin-top:5px; font-size:11px; color:#ccc;">${concepts.concept_a.visual}</div>
                    <div style="margin-top:5px; font-weight:bold; color:#fff;">TEXT: "${concepts.concept_a.text}"</div>
                </div>
                <div style="background: #111; padding: 10px; border: 1px solid #333;">
                    <strong style="color: #ff0055;">CONCEPT B: ${concepts.concept_b.type}</strong>
                    <div style="margin-top:5px; font-size:11px; color:#ccc;">${concepts.concept_b.visual}</div>
                    <div style="margin-top:5px; font-weight:bold; color:#fff;">TEXT: "${concepts.concept_b.text}"</div>
                </div>
            `;
            document.getElementById('thumb-ab-output').style.display = 'block';
            showNotification("A/B Concepts Generated");
        } catch (err) { logToTerminal(`[ERROR] Thumbnail A/B test failed.`); }
    },

    findSponsors: async () => {
        const script = document.getElementById('custom-script').value;
        if (!script) return alert("Please generate or enter a script first.");

        logToTerminal(`[MONETIZATION] Scanning script for brand-safe ad slots...`);
        try {
            const res = await fetch('/api/monetization/sponsors', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ script })
            });
            const data = await res.json();

            const list = document.getElementById('sponsor-list');
            list.innerHTML = data.spots.map(s => `
                <div style="margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #333;">
                    <strong style="color: #00ff88;">${s.position}</strong>
                    <div style="opacity: 0.7;">CONTEXT: ${s.context}</div>
                    <div style="font-style: italic; color: #aaa;">CUE: "...${s.cue}..."</div>
                </div>
            `).join('');

            document.getElementById('sponsor-output').style.display = 'block';
            showNotification("Ad Spots Identified");
        } catch (err) { logToTerminal(`[ERROR] Sponsor analysis failed.`); }
    },

    repurposeShorts: async () => {
        const script = document.getElementById('custom-script').value;
        if (!script) return alert("Please generate or enter a script first.");

        logToTerminal(`[DISTRIBUTION] Identifying viral micro-moments...`);
        try {
            const res = await fetch('/api/distribution/repurpose', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ script })
            });
            const data = await res.json();

            const list = document.getElementById('shorts-list');
            list.innerHTML = data.shorts.map(s => `
                <div style="margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #333;">
                    <strong style="color: #aa00ff;">${s.title}</strong> <span style="font-size:10px; opacity:0.5;">(${s.segment})</span>
                    <div style="opacity: 0.7;">${s.reason}</div>
                </div>
            `).join('');

            document.getElementById('shorts-output').style.display = 'block';
            showNotification("Viral Clips Identified");
        } catch (err) { logToTerminal(`[ERROR] Repurposing analysis failed.`); }
    },

    openVoiceCloning: () => {
        const modal = document.getElementById('voice-clone-modal');
        modal.style.display = modal.style.display === 'none' ? 'block' : 'none';
    },

    cloneVoice: async () => {
        const name = document.getElementById('clone-name').value;
        const sample = document.getElementById('clone-sample').value;
        if (!name || !sample) return alert("Please enter both a voice name and a sample file path.");

        document.getElementById('clone-status').textContent = "Processing audio sample...";
        logToTerminal(`[VOICE] Cloning voice model: "${name}"...`);

        try {
            const res = await fetch('/api/personalization/clone-voice', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: "clone", name, sample_path: sample })
            });
            const data = await res.json();

            document.getElementById('clone-status').textContent = `Success! Voice ID: ${data.voice_id}`;
            document.getElementById('clone-status').style.color = "#00ff88";
            logToTerminal(`[SUCCESS] Voice cloned. ID: ${data.voice_id}`);
            showNotification("Voice Model Created");
        } catch (err) {
            logToTerminal(`[ERROR] Voice cloning failed.`);
            document.getElementById('clone-status').textContent = "Error: Cloning process failed.";
            document.getElementById('clone-status').style.color = "#ff0055";
        }
    },

    triggerPublishing: async () => {
        logToTerminal(`[PUBLISH] Initiating automated distribution pipeline...`);
        const title = document.getElementById('custom-title').value || "Untitled Project";

        // Mock video path for now, in reality this would be the last rendered video
        const videoPath = "outputs/latest_render.mp4";

        try {
            const res = await fetch('/api/distribution/publish', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    video_path: videoPath,
                    platforms: ["youtube", "tiktok"],
                    metadata: { title }
                })
            });
            const data = await res.json();

            const log = document.getElementById('publish-log');
            let html = "";
            for (const [platform, result] of Object.entries(data)) {
                html += `<div style="margin-bottom:5px;"><strong style="color:#00ccff;">${platform.toUpperCase()}</strong>: ${result.status} <a href="${result.url}" target="_blank" style="color:#fff;">[View Link]</a></div>`;
            }
            log.innerHTML = html;
            document.getElementById('publish-output').style.display = 'block';
            showNotification("Content Published Successfully");
        } catch (err) { logToTerminal(`[ERROR] Publishing pipeline failed.`); }
    },

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
        const structure = document.getElementById('custom-structure').value;

        const gThumb = document.getElementById('toggle-thumb').checked;
        const gEnhance = document.getElementById('toggle-enhance').checked;
        const gPublish = document.getElementById('toggle-publish').checked;
        const gLipsync = document.getElementById('toggle-lipsync').checked;
        const gVertical = document.getElementById('toggle-vertical').checked;

        if (!title) {
            alert("Please provide at least a title.");
            return;
        }

        logToTerminal(`[SYSTEM] Packaging custom script: "${title}"...`);
        try {
            const response = await fetch('/api/produce/custom', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title, script, style, voice, structure,
                    generate_thumb: gThumb,
                    enhance_script: gEnhance,
                    publish: gPublish,
                    lipsync: gLipsync,
                    vertical: gVertical
                })
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
    },

    long: async () => {
        const title = document.getElementById('custom-title').value;
        const script = document.getElementById('custom-script').value;
        const style = document.getElementById('custom-style').value;
        const voice = document.getElementById('custom-voice').value;
        const structure = document.getElementById('custom-structure').value;

        const gThumb = document.getElementById('toggle-thumb').checked;
        const gEnhance = document.getElementById('toggle-enhance').checked;
        const gPublish = document.getElementById('toggle-publish').checked;

        logToTerminal(`[FEATURE] INITIALIZING CHAPTER-BASED RENDER for: "${title}"...`);
        logToTerminal(`[SYSTEM] Analyzing script for chapter breaks...`);

        try {
            const response = await fetch('/api/produce/long', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title, script, style, voice, structure,
                    generate_thumb: gThumb,
                    enhance_script: gEnhance,
                    publish: gPublish
                })
            });
            const data = await response.json();
            showNotification("Feature Documentary Initiated");
            logToTerminal(`[DOC-ENGINE] ${data.status}`);
        } catch (err) {
            logToTerminal(`[ERROR] Long-form engine failed: ${err.message}`);
        }
    }
};

const settings = {
    load: async () => {
        document.getElementById('settings-infra').innerHTML = '<div class="loading">Booting systems...</div>';
        try {
            const response = await fetch('/api/settings');
            const data = await response.json();

            // 1. Load Infrastructure (Flat Keys)
            const infraEl = document.getElementById('settings-infra');
            infraEl.innerHTML = '';
            const flatKeys = ["OPENAI_API_KEY", "PEXELS_API_KEY", "CHAPTER_LENGTH_MINUTES", "OUTPUT_DIR"];
            flatKeys.forEach(k => {
                infraEl.appendChild(settings.createInputBox(k, data[k]));
            });

            // 2. Load Styles (Nested Objects)
            const stylesEl = document.getElementById('settings-styles');
            stylesEl.innerHTML = '';
            Object.keys(data.STYLES).forEach(sName => {
                const s = data.STYLES[sName];
                const box = document.createElement('div');
                box.className = 'monobox';
                box.innerHTML = `
                    <label>STYLE: ${sName.toUpperCase()}</label>
                    <textarea class="style-json" data-name="${sName}" style="height:100px; background:transparent; border:none; color:inherit; width:100%; font-family:inherit; font-size:inherit;">${JSON.stringify(s, null, 2)}</textarea>
                `;
                stylesEl.appendChild(box);
            });

            // 3. Load Voices
            const voicesEl = document.getElementById('settings-voices');
            voicesEl.innerHTML = '';
            Object.keys(data.VOICES).forEach(vName => {
                const v = data.VOICES[vName];
                const box = document.createElement('div');
                box.className = 'monobox';
                box.innerHTML = `
                    <label>VOICE: ${vName.toUpperCase()}</label>
                    <input type="text" class="voice-engine" data-name="${vName}" value="${v.engine}">
                `;
                voicesEl.appendChild(box);
            });

        } catch (err) {
            console.error(err);
        }
    },

    createInputBox: (label, value) => {
        const box = document.createElement('div');
        box.className = 'monobox';
        box.innerHTML = `
            <label>${label.replace(/_/g, ' ')}</label>
            <input type="text" id="setting-${label}" value="${value}">
        `;
        return box;
    },

    save: async () => {
        logToTerminal(`[SYSTEM] Initiating Global Sync...`);

        const newSettings = { STYLES: {}, VOICES: {} };

        // Collect Infra
        ["OPENAI_API_KEY", "PEXELS_API_KEY", "CHAPTER_LENGTH_MINUTES", "OUTPUT_DIR"].forEach(k => {
            newSettings[k] = document.getElementById(`setting-${k}`).value;
        });

        // Collect Styles
        document.querySelectorAll('.style-json').forEach(ta => {
            newSettings.STYLES[ta.getAttribute('data-name')] = JSON.parse(ta.value);
        });

        // Collect Voices
        document.querySelectorAll('.voice-engine').forEach(inp => {
            newSettings.VOICES[inp.getAttribute('data-name')] = { engine: inp.value };
        });

        try {
            const response = await fetch('/api/settings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newSettings)
            });
            const data = await response.json();
            showNotification("Studio Synchronized");
            logToTerminal(`[ENGINE] ${data.status}`);
        } catch (err) {
            logToTerminal(`[ERROR] Sync failed: ${err.message}`);
        }
    }
};

const library = {
    load: async () => {
        loadLibrary();
    },

    draftResponse: async () => {
        const comment = document.getElementById('viewer-comment').value;
        if (!comment) return showNotification("Paste a comment first");

        logToTerminal(`[STRATEGY] Drafting perspective defense for viewer comment...`);
        try {
            const res = await fetch('/api/engage/comment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    topic: "Current Context", // In real use, we'd pick the active video
                    script: "Latest Script",
                    comment: comment
                })
            });
            const data = await res.json();
            document.getElementById('draft-output').style.display = 'block';
            document.getElementById('reply-text').textContent = data.reply;
            showNotification("Engagement Strategy Generated");
        } catch (err) { logToTerminal(`[ERROR] Engagement bot failed.`); }
    },

    draftCommunity: async () => {
        logToTerminal(`[STRATEGY] Drafting Viral Community Kit (Polls & Teasers)...`);
        try {
            const res = await fetch('/api/community/draft', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    topic: "Current Context",
                    script: "Latest Script"
                })
            });
            const data = await res.json();
            document.getElementById('community-output').style.display = 'block';
            document.getElementById('community-text').textContent = typeof data.kit === 'string' ? data.kit : JSON.stringify(data.kit, null, 2);
            showNotification("Community Kit Ready");
        } catch (err) { logToTerminal(`[ERROR] Community manager failed.`); }
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
