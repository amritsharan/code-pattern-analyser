const API_BASE = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' 
    ? 'http://127.0.0.1:5000' 
    : window.location.origin;

// Global state variables
window._cppcode = "";
window._patternDetails = {};
window._activePattern = "";

// Check sessions on load
document.addEventListener('DOMContentLoaded', function() {
    checkSession();
    
    // Bind Analyser Form Submit
    const form = document.getElementById('patternForm');
    if (form) {
        form.onsubmit = runPatternAnalysis;
    }
});

// Tab Navigation
window.switchTab = function(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(el => {
        el.classList.add('hidden');
    });
    // Remove active state from buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show active tab
    const activeContent = document.getElementById(`content-${tabName}`);
    if (activeContent) {
        activeContent.classList.remove('hidden');
    }
    // Set button active
    const activeBtn = document.getElementById(`tab-${tabName}`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
    
    // If switching to history, fetch it
    if (tabName === 'history') {
        loadHistory();
    }
};

// Check Authentication Session
async function checkSession() {
    try {
        const res = await fetch(`${API_BASE}/session`, { credentials: 'include' });
        const data = await res.json();
        if (data.logged_in) {
            showDashboard(data.username);
        } else {
            showLogin();
        }
    } catch (e) {
        showLogin();
    }
}

// UI State Toggles
window.showLogin = function() {
    document.getElementById('main-container').classList.add('hidden');
    document.getElementById('register-container').classList.add('hidden');
    document.getElementById('user-profile-header').classList.add('hidden');
    document.getElementById('login-container').classList.remove('hidden');
    document.getElementById('login-error').innerText = '';
};

window.showRegister = function() {
    document.getElementById('main-container').classList.add('hidden');
    document.getElementById('login-container').classList.add('hidden');
    document.getElementById('register-container').classList.remove('hidden');
    document.getElementById('register-error').innerText = '';
    document.getElementById('register-success').innerText = '';
};

function showDashboard(username) {
    document.getElementById('login-container').classList.add('hidden');
    document.getElementById('register-container').classList.add('hidden');
    document.getElementById('main-container').classList.remove('hidden');
    
    const profile = document.getElementById('user-profile-header');
    profile.classList.remove('hidden');
    document.getElementById('username-display').innerText = username;
    
    // Clear forms and reset dashboard state
    document.getElementById('patternForm').reset();
    resetAnalysisOutput();
}

function resetAnalysisOutput() {
    document.getElementById('output').style.display = 'none';
    document.getElementById('pattern-details-card').style.display = 'none';
    document.getElementById('output-placeholder').style.display = 'flex';
    window._cppcode = "";
    window._patternDetails = {};
    window._activePattern = "";
}

// User Actions: Login
window.login = async function() {
    const userField = document.getElementById('username');
    const passField = document.getElementById('password');
    const errField = document.getElementById('login-error');
    
    const username = userField.value.trim();
    const password = passField.value.trim();
    errField.innerText = '';
    
    if (!username || !password) {
        errField.innerText = 'Please enter both username and password.';
        return;
    }
    
    try {
        const res = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (res.ok) {
            showDashboard(username);
            userField.value = '';
            passField.value = '';
        } else {
            errField.innerText = data.error || 'Login failed';
        }
    } catch (e) {
        errField.innerText = 'Unable to connect to the backend server.';
    }
};

// User Actions: Register
window.registerUser = async function() {
    const userField = document.getElementById('reg-username');
    const passField = document.getElementById('reg-password');
    const errField = document.getElementById('register-error');
    const succField = document.getElementById('register-success');
    
    const username = userField.value.trim();
    const password = passField.value.trim();
    errField.innerText = '';
    succField.innerText = '';
    
    if (!username || !password) {
        errField.innerText = 'Username and password are required.';
        return;
    }
    
    try {
        const res = await fetch(`${API_BASE}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        if (res.ok) {
            succField.innerText = 'Account created successfully! Redirecting...';
            userField.value = '';
            passField.value = '';
            setTimeout(showLogin, 1500);
        } else {
            errField.innerText = data.error || 'Registration failed';
        }
    } catch (e) {
        errField.innerText = 'Connection error. Registration failed.';
    }
};

// User Actions: Logout
window.logout = async function() {
    try {
        await fetch(`${API_BASE}/logout`, {
            method: 'POST',
            credentials: 'include'
        });
    } catch (e) {}
    showLogin();
};

// Main DSA Pattern Analysis Submitter
async function runPatternAnalysis(e) {
    if (e) e.preventDefault();
    
    const descVal = document.getElementById('desc').value.trim();
    const codeVal = document.getElementById('cppcode').value.trim();
    const platformVal = document.getElementById('platform').value;
    
    if (!descVal && !codeVal) {
        alert("Please enter either a problem description or a code snippet.");
        return;
    }
    
    // Hide output details, show loading
    document.getElementById('output-placeholder').style.display = 'none';
    const outputDiv = document.getElementById('output');
    outputDiv.style.display = 'block';
    outputDiv.innerHTML = '<div class="loading-spinner">Analysing data inputs, please wait...</div>';
    document.getElementById('pattern-details-card').style.display = 'none';
    
    window._cppcode = codeVal;
    window._patternDetails = {};
    
    let textPatterns = [];
    let codePatterns = [];
    let mergedPatterns = new Set();
    
    try {
        // 1. If description is provided, analyse text
        if (descVal) {
            const url = platformVal ? `${API_BASE}/detect-platform` : `${API_BASE}/detect`;
            const textRes = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ text: descVal, platform: platformVal })
            });
            if (textRes.ok) {
                const data = await textRes.json();
                textPatterns = data.patterns || [];
                // Merge details
                if (data.details) {
                    Object.assign(window._patternDetails, data.details);
                }
            }
        }
        
        // 2. If code snippet is provided, analyse code structures
        if (codeVal) {
            const codeRes = await fetch(`${API_BASE}/detect-code`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ code: codeVal })
            });
            if (codeRes.ok) {
                const data = await codeRes.json();
                codePatterns = data.patterns || [];
                // Merge details and merge explanations
                if (data.details) {
                    for (const [pat, det] of Object.entries(data.details)) {
                        if (window._patternDetails[pat]) {
                            window._patternDetails[pat].explanation = det.explanation;
                        } else {
                            window._patternDetails[pat] = det;
                        }
                    }
                }
            }
        }
        
        // Combine patterns
        textPatterns.forEach(p => mergedPatterns.add(p));
        codePatterns.forEach(p => mergedPatterns.add(p));
        
        const finalPatterns = Array.from(mergedPatterns);
        
        if (finalPatterns.length === 0) {
            outputDiv.innerHTML = '<h3>Analysis Complete</h3><p class="info-msg">No clear algorithmic patterns were matching this query.</p>';
            return;
        }
        
        // Render Chip Controls
        let html = '<h3>Detected Algorithmic Patterns</h3>';
        html += '<p style="margin-bottom:12px; font-size:0.95rem; color:#8B949E;">Click a pattern below to view its complexity, flowchart, and LeetCode problems.</p>';
        html += '<div class="pattern-chips-container" id="pattern-chips"></div>';
        if (platformVal) {
            html += `<div class="platform-badge">Target Platform: <strong>${platformVal.toUpperCase()}</strong></div>`;
        }
        outputDiv.innerHTML = html;
        
        const chipsContainer = document.getElementById('pattern-chips');
        finalPatterns.forEach(p => {
            const isFromText = textPatterns.includes(p);
            const isFromCode = codePatterns.includes(p);
            
            let label = p.replace('_', ' ').toUpperCase();
            let sourceTag = "";
            if (isFromText && isFromCode) sourceTag = " (Desc & Code)";
            else if (isFromText) sourceTag = " (Desc)";
            else if (isFromCode) sourceTag = " (Code)";
            
            const btn = document.createElement('button');
            btn.className = 'pattern-btn';
            btn.innerHTML = `${label}<span class="source-tag">${sourceTag}</span>`;
            btn.onclick = () => selectPattern(p);
            chipsContainer.appendChild(btn);
        });
        
        // Save to Database History in the background
        fetch(`${API_BASE}/history/save`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                desc: descVal,
                code: codeVal,
                patterns: finalPatterns,
                platform: platformVal
            })
        });
        
        // Select the first pattern automatically
        selectPattern(finalPatterns[0]);
        
    } catch (err) {
        outputDiv.innerHTML = `<div class="error-msg">An error occurred during analysis: ${err.message}</div>`;
    }
}

// View Specific Pattern Details
window.selectPattern = async function(patternKey) {
    window._activePattern = patternKey;
    
    // Highlight selected chip
    document.querySelectorAll('.pattern-btn').forEach(btn => {
        if (btn.innerText.toLowerCase().startsWith(patternKey.replace('_', ' '))) {
            btn.classList.add('selected');
        } else {
            btn.classList.remove('selected');
        }
    });
    
    const details = window._patternDetails[patternKey] || {};
    const title = details.title || patternKey.replace('_', ' ').toUpperCase();
    const timeComp = details.time_complexity || 'N/A';
    const spaceComp = details.space_complexity || 'N/A';
    const explanation = details.explanation || `Uses standard ${title} mechanisms.`;
    
    // Update labels
    document.getElementById('details-pattern-title').innerText = title;
    document.getElementById('time-complexity-val').innerText = timeComp;
    document.getElementById('space-complexity-val').innerText = spaceComp;
    document.getElementById('heuristic-explanation-val').innerText = explanation;
    
    // Render Practice Problems
    const probList = document.getElementById('problems-list');
    probList.innerHTML = '';
    const problems = details.problems || [];
    if (problems.length > 0) {
        problems.forEach(p => {
            const li = document.createElement('li');
            li.innerHTML = `<a href="${p.url}" target="_blank" class="problem-link">${p.title} ↗</a>`;
            probList.appendChild(li);
        });
    } else {
        probList.innerHTML = '<li style="color:#8b949e;">No curated problems available for this pattern.</li>';
    }
    
    // Show Details Container
    document.getElementById('pattern-details-card').style.display = 'block';
    
    // Fetch and render flowchart
    const visContainer = document.getElementById('visualization');
    visContainer.innerHTML = '<div style="color:#8b949e; font-size:0.9rem;">Generating flowchart...</div>';
    
    try {
        const res = await fetch(`${API_BASE}/visualize`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ pattern: patternKey })
        });
        const data = await res.json();
        
        if (data.flowchart && data.flowchart.startsWith('flowchart')) {
            visContainer.innerHTML = `<pre class="mermaid" id="mermaid-svg">${data.flowchart}</pre>`;
            if (window.mermaid) {
                try {
                    window.mermaid.init(undefined, visContainer.querySelectorAll('.mermaid'));
                } catch (e) {
                    visContainer.innerHTML = `<pre style="font-family:JetBrains Mono, monospace;font-size:0.8rem;color:#8b949e;">${data.flowchart}</pre>`;
                }
            }
        } else {
            visContainer.innerHTML = `<div style="color:#ff7b72;">${data.flowchart || 'No chart available.'}</div>`;
        }
    } catch (e) {
        visContainer.innerHTML = '<div style="color:#ff7b72;">Failed to render flowchart.</div>';
    }
    
    // Source Code Annotation Highlights
    const codeSec = document.getElementById('annotated-code-section');
    if (window._cppcode && window._cppcode.trim()) {
        codeSec.style.display = 'block';
        let code = escapeHtml(window._cppcode);
        
        // Define language independent matches for highlighting key variables/words
        let highlightKeywords = {
            'two_pointers': ['left', 'right', 'start', 'end', 'low', 'high', 'ptr1', 'ptr2', 'while', 'while\\(', 'for'],
            'sliding_window': ['window', 'start', 'end', 'left', 'right', 'sum', 'max', 'min', 'len', 'while', 'for'],
            'stack': ['stack', 'push', 'pop', 'top', 'append', 'isEmpty'],
            'monotonic_stack': ['stack', 'push', 'pop', 'top', 'append', 'while', '<', '>', '<=', '>='],
            'queue': ['queue', 'push', 'pop', 'front', 'back', 'enqueue', 'dequeue', 'deque', 'popleft'],
            'tree': ['TreeNode', 'Node', 'left', 'right', 'root', 'val', 'dfs', 'traverse'],
            'heap': ['priority_queue', 'PriorityQueue', 'heapq', 'heappush', 'heappop', 'heapify'],
            'dynamic_programming': ['dp', 'memo', 'cache', 'lru_cache', 'vector', 'int\\[\\]\\[\\]'],
            'graph': ['adj', 'graph', 'edges', 'vertices', 'visited', 'bfs', 'dfs', 'dijkstra'],
            'binary_search': ['left', 'right', 'mid', 'middle', 'low', 'high', 'l', 'r', 'while', 'binarySearch', 'bisect'],
            'prefix_sum': ['prefix', 'sum', 'presum', 'cumulative', 'running'],
            'trie': ['trie', 'TrieNode', 'children', 'insert', 'search', 'startsWith', 'isEnd'],
            'union_find': ['union', 'find', 'dsu', 'parent', 'rank', 'DisjointSet'],
            'segment_tree': ['segment', 'tree', 'build', 'query', 'update', 'lazy'],
            'backtracking': ['backtrack', 'dfs', 'solve', 'recursion', 'visited', 'pop_back', 'remove'],
            'bit_manipulation': ['xor', 'and', 'or', 'mask', 'bitmask', '&amp;', '\\|', '\\^', '&lt;&lt;', '&gt;&gt;'],
            'greedy': ['greedy', 'sort', 'sorted', 'min', 'max']
        };
        
        const kws = highlightKeywords[patternKey] || [];
        kws.forEach(kw => {
            // Check if special operators are escaped correctly or match exactly
            let regString = `\\b${kw}\\b`;
            if (kw === '&amp;' || kw === '\\|' || kw === '\\^' || kw === '&lt;&lt;' || kw === '&gt;&gt;' || kw === '<' || kw === '>') {
                regString = kw;
            }
            code = code.replace(new RegExp(regString, 'g'), `<mark>${kw.replace('\\', '')}</mark>`);
        });
        
        document.getElementById('annotated-code').innerHTML = code;
    } else {
        codeSec.style.display = 'none';
    }
};

function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}

// Retrieve Saved Analysis History
async function loadHistory() {
    const listDiv = document.getElementById('history-list');
    listDiv.innerHTML = '<div class="loading-spinner">Fetching query records...</div>';
    
    try {
        const res = await fetch(`${API_BASE}/history`, { credentials: 'include' });
        const data = await res.json();
        
        if (res.ok && data.history && data.history.length > 0) {
            listDiv.innerHTML = '';
            data.history.forEach(item => {
                const row = document.createElement('div');
                row.className = 'history-item glass-card';
                
                // Formulate snippet labels
                let snippet = item.problem_desc ? item.problem_desc.substring(0, 140) + '...' : 'Code analysis snippet';
                let tags = item.detected_patterns.map(p => `<span class="history-tag">${p.replace('_', ' ')}</span>`).join(' ');
                
                row.innerHTML = `
                    <div class="history-item-details">
                        <div class="history-date">${new Date(item.created_at).toLocaleString()}</div>
                        <p class="history-desc">${escapeHtml(snippet)}</p>
                        <div class="history-tags">${tags}</div>
                    </div>
                    <button class="reload-btn" onclick="reloadHistoryItem('${encodeURIComponent(JSON.stringify(item))}')">Load Analysis</button>
                `;
                listDiv.appendChild(row);
            });
        } else {
            listDiv.innerHTML = '<div class="placeholder-msg">No queries recorded yet. Start solving problems!</div>';
        }
    } catch (e) {
        listDiv.innerHTML = '<div class="error-msg">Error loading history records.</div>';
    }
}

// Reload a history item back to main dashboard
window.reloadHistoryItem = function(encodedItem) {
    const item = JSON.parse(decodeURIComponent(encodedItem));
    
    document.getElementById('desc').value = item.problem_desc || "";
    document.getElementById('cppcode').value = item.code_snippet || "";
    document.getElementById('platform').value = item.platform || "";
    
    // Switch tabs to analyser
    switchTab('analyser');
    
    // Run analysis automatically
    runPatternAnalysis();
};

// Repository Analysis Scanner
window.analyzeRepo = async function() {
    const repoUrl = document.getElementById('repo-url').value.trim();
    const statusDiv = document.getElementById('repo-analyze-status');
    const resultDiv = document.getElementById('repo-analyze-result');
    const chartCard = document.getElementById('repo-chart-container');
    
    resultDiv.style.display = 'none';
    chartCard.style.display = 'none';
    statusDiv.className = 'status-message info';
    statusDiv.innerText = 'Cloning and scanning repository. This might take up to a minute...';
    
    if (!repoUrl) {
        statusDiv.className = 'status-message error';
        statusDiv.innerText = 'Please enter a valid public GitHub repo URL.';
        return;
    }
    
    try {
        const res = await fetch(`${API_BASE}/analyze-repo`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ repo_url: repoUrl })
        });
        const data = await res.json();
        
        if (res.ok && data.stats) {
            statusDiv.className = 'status-message success';
            statusDiv.innerText = 'Scan finished successfully!';
            
            // Build stats list
            let html = '<h3>Scan Summary Table</h3>';
            html += '<table class="repo-table"><thead><tr><th>DSA Pattern</th><th>Files Hit</th><th>Sample Code Files</th></tr></thead><tbody>';
            
            let hasHits = false;
            for (const [pattern, count] of Object.entries(data.stats)) {
                if (count > 0) {
                    hasHits = true;
                    const files = (data.file_hits[pattern] || []).slice(0, 4).map(f => `<li><code>${escapeHtml(f)}</code></li>`).join('');
                    html += `<tr>
                        <td><strong>${pattern.replace('_', ' ').toUpperCase()}</strong></td>
                        <td class="count-col">${count}</td>
                        <td><ul class="file-list">${files}</ul></td>
                    </tr>`;
                }
            }
            html += '</tbody></table>';
            
            if (!hasHits) {
                html = '<h3>Scan Summary</h3><p style="color:#8b949e; text-align:center; padding: 20px;">No typical DSA patterns were discovered in the codebase. Supported file extensions: .cpp, .java, .py</p>';
            }
            
            resultDiv.innerHTML = html;
            resultDiv.style.display = 'block';
            
            // Render Chart.js
            const chartCanvas = document.getElementById('repo-analyze-chart');
            chartCard.style.display = 'block';
            
            // Extract hits that are > 0
            const activeStats = {};
            for (const [k, v] of Object.entries(data.stats)) {
                if (v > 0) activeStats[k.replace('_', ' ').toUpperCase()] = v;
            }
            
            const labels = Object.keys(activeStats);
            const values = Object.values(activeStats);
            
            if (window._repoPatternChart) {
                window._repoPatternChart.destroy();
            }
            
            if (labels.length > 0) {
                window._repoPatternChart = new Chart(chartCanvas, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Instances Detected',
                            data: values,
                            backgroundColor: 'rgba(47, 129, 247, 0.65)',
                            borderColor: 'rgba(88, 166, 255, 1)',
                            borderWidth: 1.5,
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false }
                        },
                        scales: {
                            x: {
                                grid: { color: 'rgba(255, 255, 255, 0.05)' },
                                ticks: { color: '#c9d1d9', font: { family: 'Outfit' } }
                            },
                            y: {
                                grid: { color: 'rgba(255, 255, 255, 0.05)' },
                                ticks: { color: '#c9d1d9', precision: 0, font: { family: 'Outfit' } },
                                beginAtZero: true
                            }
                        }
                    }
                });
            } else {
                chartCard.style.display = 'none';
            }
            
        } else {
            statusDiv.className = 'status-message error';
            statusDiv.innerText = data.error || 'Failed to scan repository.';
        }
    } catch (e) {
        statusDiv.className = 'status-message error';
        statusDiv.innerText = 'Unable to connect to the backend server.';
    }
};
