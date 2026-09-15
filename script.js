const API_BASE = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' 
    ? 'http://127.0.0.1:5000' 
    : window.location.origin;

// Global state variables
window._cppcode = "";
window._patternDetails = {};
window._activePattern = "";
window._activeBoilerplates = {};
window._activeLanguage = "cpp";
window._currentAiAnalysis = null;

// Initialize on DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    checkSession();
    initAiSettings();
    
    // Bind Analyser Form Submit
    const form = document.getElementById('patternForm');
    if (form) {
        form.onsubmit = runPatternAnalysis;
    }
});

// --- AI Configuration Management ---
function getAiConfig() {
    return {
        provider: localStorage.getItem('dsa_ai_provider') || 'gemini',
        apiKey: localStorage.getItem('dsa_ai_key') || ''
    };
}

function initAiSettings() {
    const config = getAiConfig();
    const providerSelect = document.getElementById('ai-provider-select');
    const keyInput = document.getElementById('api-key-input');
    
    if (providerSelect) providerSelect.value = config.provider;
    if (keyInput && config.apiKey) keyInput.value = config.apiKey;
    
    updateAiHeaderStatus();
}

function updateAiHeaderStatus() {
    const config = getAiConfig();
    const indicator = document.getElementById('ai-status-indicator');
    const badge = document.getElementById('active-engine-badge');
    
    if (config.apiKey && config.provider !== 'heuristic') {
        if (indicator) {
            indicator.className = 'ai-indicator';
            indicator.title = `AI Active (${config.provider.toUpperCase()})`;
        }
        if (badge) {
            badge.innerText = config.provider === 'gemini' ? '⚡ Gemini 1.5 Flash' : '🤖 OpenAI GPT-4o';
            badge.style.borderColor = 'rgba(63, 185, 80, 0.4)';
            badge.style.color = '#3fb950';
        }
    } else {
        if (indicator) {
            indicator.className = 'ai-indicator offline';
            indicator.title = 'Offline Heuristic Engine';
        }
        if (badge) {
            badge.innerText = '⚡ Offline Heuristics';
            badge.style.borderColor = 'rgba(188, 140, 255, 0.35)';
            badge.style.color = '#d2a8ff';
        }
    }
}

window.openAiSettingsModal = function() {
    const modal = document.getElementById('ai-settings-modal');
    if (modal) {
        const config = getAiConfig();
        document.getElementById('ai-provider-select').value = config.provider;
        document.getElementById('api-key-input').value = config.apiKey;
        onAiProviderChange();
        document.getElementById('ai-modal-status').innerText = '';
        modal.classList.remove('hidden');
    }
};

window.closeAiSettingsModal = function() {
    const modal = document.getElementById('ai-settings-modal');
    if (modal) modal.classList.add('hidden');
};

window.onAiProviderChange = function() {
    const provider = document.getElementById('ai-provider-select').value;
    const keyGroup = document.getElementById('api-key-group');
    const hint = document.getElementById('api-key-hint');
    
    if (provider === 'heuristic') {
        keyGroup.style.display = 'none';
    } else {
        keyGroup.style.display = 'block';
        hint.innerText = provider === 'gemini' 
            ? 'Get a free Gemini API key from Google AI Studio (aistudio.google.com).'
            : 'Enter your OpenAI API key or compatible proxy key.';
    }
};

window.saveAiSettings = function() {
    const provider = document.getElementById('ai-provider-select').value;
    const apiKey = document.getElementById('api-key-input').value.trim();
    const status = document.getElementById('ai-modal-status');
    
    localStorage.setItem('dsa_ai_provider', provider);
    localStorage.setItem('dsa_ai_key', apiKey);
    
    updateAiHeaderStatus();
    status.className = 'status-msg success-msg';
    status.innerText = 'Settings saved successfully!';
    
    setTimeout(() => {
        closeAiSettingsModal();
    }, 1000);
};

window.clearAiKey = function() {
    localStorage.removeItem('dsa_ai_key');
    document.getElementById('api-key-input').value = '';
    const status = document.getElementById('ai-modal-status');
    status.className = 'status-msg';
    status.innerText = 'API Key reset to default.';
    updateAiHeaderStatus();
};

// --- Tab Navigation ---
window.switchTab = function(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => {
        el.classList.add('hidden');
    });
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const activeContent = document.getElementById(`content-${tabName}`);
    if (activeContent) activeContent.classList.remove('hidden');
    
    const activeBtn = document.getElementById(`tab-${tabName}`);
    if (activeBtn) activeBtn.classList.add('active');
    
    if (tabName === 'history') {
        loadHistory();
    }
};

// --- Authentication Session ---
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
    
    document.getElementById('patternForm').reset();
    resetAnalysisOutput();
    updateAiHeaderStatus();
}

function resetAnalysisOutput() {
    document.getElementById('output').style.display = 'none';
    document.getElementById('pattern-details-card').style.display = 'none';
    document.getElementById('output-placeholder').style.display = 'flex';
    window._cppcode = "";
    window._patternDetails = {};
    window._activePattern = "";
    window._activeBoilerplates = {};
    window._currentAiAnalysis = null;
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
        errField.innerText = 'Unable to connect to backend server.';
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

// --- Phase 4: Code Editor Helper Functions ---
window.handleCodeEditorKeydown = function(e) {
    if (e.key === 'Tab') {
        e.preventDefault();
        const textarea = e.target;
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        textarea.value = textarea.value.substring(0, start) + '    ' + textarea.value.substring(end);
        textarea.selectionStart = textarea.selectionEnd = start + 4;
    }
};

window.onCodeLanguageChange = function() {
    const langSelect = document.getElementById('code-lang-select');
    const lang = langSelect ? langSelect.value : 'python';
    const editor = document.getElementById('cppcode');
    if (editor && !editor.value.trim()) {
        editor.placeholder = `Paste your ${lang.toUpperCase()} solution or partial code snippet here... (Tab key supported)`;
    }
};

window.loadSampleCode = function() {
    const langSelect = document.getElementById('code-lang-select');
    const lang = langSelect ? langSelect.value : 'python';
    const editor = document.getElementById('cppcode');
    if (!editor) return;

    const samples = {
        python: `def two_sum_quadratic(nums, target):
    # O(N^2) brute force search
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []`,
        cpp: `class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        for (int i = 0; i < nums.size(); i++) {
            for (int j = i + 1; j < nums.size(); j++) {
                if (nums[i] + nums[j] == target) return {i, j};
            }
        }
        return {};
    }
};`,
        java: `public class Solution {
    public int[] twoSum(int[] nums, int target) {
        for (int i = 0; i < nums.length; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] + nums[j] == target) return new int[]{i, j};
            }
        }
        return new int[]{};
    }
}`,
        javascript: `function twoSum(nums, target) {
    for (let i = 0; i < nums.length; i++) {
        for (let j = i + 1; j < nums.length; j++) {
            if (nums[i] + nums[j] === target) return [i, j];
        }
    }
    return [];
}`
    };

    editor.value = samples[lang] || samples.python;
};

window.clearCodeEditor = function() {
    const editor = document.getElementById('cppcode');
    if (editor) editor.value = '';
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

// --- Phase 2: One-Click Problem URL Importer ---
window.fetchProblemByUrl = async function() {
    const urlInput = document.getElementById('import-url-input');
    const statusDiv = document.getElementById('import-url-status');
    const pillsDiv = document.getElementById('imported-meta-pills');
    const fetchBtn = document.getElementById('import-fetch-btn');
    
    const url = urlInput ? urlInput.value.trim() : "";
    if (!url) {
        statusDiv.className = 'import-status-text error';
        statusDiv.innerText = 'Please enter a problem URL (e.g., https://leetcode.com/problems/two-sum/)';
        return;
    }
    
    // Set UI loading state
    statusDiv.className = 'import-status-text loading';
    statusDiv.innerText = '⚡ Scraping problem details & constraints...';
    pillsDiv.style.display = 'none';
    pillsDiv.innerHTML = '';
    fetchBtn.disabled = true;
    fetchBtn.innerText = 'Scraping...';
    
    try {
        const res = await fetch(`${API_BASE}/api/scrape-problem`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ url })
        });
        
        const data = await res.json();
        
        if (res.ok && data.description) {
            // Auto-populate description textarea
            document.getElementById('desc').value = data.description;
            
            // Auto-select platform dropdown if matched
            const platformSelect = document.getElementById('platform');
            if (platformSelect && data.platform) {
                const options = Array.from(platformSelect.options).map(o => o.value);
                if (options.includes(data.platform)) {
                    platformSelect.value = data.platform;
                }
            }
            
            // Render Metadata Pills
            let pillsHtml = '';
            if (data.difficulty && data.difficulty !== 'Unknown') {
                const diffClass = data.difficulty.toLowerCase().includes('easy') 
                    ? 'difficulty-easy' 
                    : (data.difficulty.toLowerCase().includes('hard') ? 'difficulty-hard' : 'difficulty-medium');
                pillsHtml += `<span class="meta-pill ${diffClass}">${data.difficulty}</span>`;
            }
            
            if (data.tags && data.tags.length > 0) {
                data.tags.slice(0, 4).forEach(t => {
                    pillsHtml += `<span class="meta-pill tag-pill">${t}</span>`;
                });
            }
            
            if (pillsHtml) {
                pillsDiv.innerHTML = pillsHtml;
                pillsDiv.style.display = 'flex';
            }
            
            statusDiv.className = 'import-status-text success';
            statusDiv.innerText = `✅ Loaded: ${data.title}`;
            
            // Automatically run AI pattern analysis on imported problem!
            runPatternAnalysis();
            
        } else {
            statusDiv.className = 'import-status-text error';
            statusDiv.innerText = data.error || 'Failed to fetch problem from the given URL.';
        }
    } catch (err) {
        statusDiv.className = 'import-status-text error';
        statusDiv.innerText = `Error connecting to scraper: ${err.message}`;
    } finally {
        fetchBtn.disabled = false;
        fetchBtn.innerText = '⚡ Fetch & Analyze';
    }
};

// --- Main DSA AI Pattern Analysis Submitter ---
async function runPatternAnalysis(e) {
    if (e) e.preventDefault();
    
    const descVal = document.getElementById('desc').value.trim();
    const codeVal = document.getElementById('cppcode').value.trim();
    const platformVal = document.getElementById('platform').value;
    
    if (!descVal && !codeVal) {
        alert("Please enter either a problem description or a code snippet.");
        return;
    }
    
    // Hide placeholder, show loading
    document.getElementById('output-placeholder').style.display = 'none';
    const outputDiv = document.getElementById('output');
    outputDiv.style.display = 'block';
    outputDiv.innerHTML = '<div class="loading-spinner">⚡ Extracting algorithmic structures & synthesizing AI patterns...</div>';
    document.getElementById('pattern-details-card').style.display = 'none';
    
    window._cppcode = codeVal;
    window._patternDetails = {};
    
    const aiConfig = getAiConfig();
    
    try {
        // Call Unified AI Analysis Endpoint
        const aiRes = await fetch(`${API_BASE}/api/ai-analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Gemini-Key': aiConfig.apiKey,
                'X-AI-Provider': aiConfig.provider
            },
            credentials: 'include',
            body: JSON.stringify({
                text: descVal,
                code: codeVal,
                platform: platformVal,
                apiKey: aiConfig.apiKey,
                apiProvider: aiConfig.provider
            })
        });
        
        if (!aiRes.ok) {
            throw new Error(`Server returned status ${aiRes.status}`);
        }
        
        const aiData = await aiRes.json();
        window._currentAiAnalysis = aiData;
        
        const primary = aiData.primary_pattern || "two_pointers";
        const secondary = aiData.secondary_patterns || [];
        const allPatterns = [primary, ...secondary];
        
        // Populate global details
        window._patternDetails[primary] = {
            title: aiData.primary_pattern_title || primary.replace('_', ' ').toUpperCase(),
            time_complexity: aiData.time_complexity || 'O(N)',
            space_complexity: aiData.space_complexity || 'O(1)',
            explanation: aiData.justification,
            constraint_analysis: aiData.constraint_analysis,
            boilerplates: aiData.boilerplates,
            edge_cases: aiData.edge_cases,
            problems: aiData.practice_problems,
            mode: aiData.mode
        };
        
        // Render Output Top Card
        let html = `
            <div class="output-header-flex">
                <h3>Detected Algorithmic Patterns</h3>
                <span id="confidence-pill" class="confidence-pill">${Math.round((aiData.confidence_score || 0.88) * 100)}% Confidence Match</span>
            </div>
            <p style="margin-bottom:12px; font-size:0.95rem; color:#8B949E;">Click any detected pattern to view its complexity, boilerplate code, edge cases, and flowchart.</p>
            <div class="pattern-chips-container" id="pattern-chips"></div>
        `;
        if (platformVal) {
            html += `<div class="platform-badge">Target Platform: <strong>${platformVal.toUpperCase()}</strong></div>`;
        }
        outputDiv.innerHTML = html;
        
        const chipsContainer = document.getElementById('pattern-chips');
        allPatterns.forEach((p, idx) => {
            const btn = document.createElement('button');
            btn.className = idx === 0 ? 'pattern-btn selected' : 'pattern-btn';
            btn.innerHTML = `${p.replace('_', ' ').toUpperCase()}${idx === 0 ? ' <span class="source-tag">(Primary)</span>' : ''}`;
            btn.onclick = () => selectPattern(p);
            chipsContainer.appendChild(btn);
        });
        
        // Save to Database History
        fetch(`${API_BASE}/history/save`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                desc: descVal,
                code: codeVal,
                patterns: allPatterns,
                platform: platformVal
            })
        });

        // If code is provided, run AST static analysis
        const astSection = document.getElementById('ast-inspection-section');
        if (codeVal && codeVal.trim()) {
            const codeLang = document.getElementById('code-lang-select') ? document.getElementById('code-lang-select').value : 'python';
            try {
                const astRes = await fetch(`${API_BASE}/api/analyze-code-ast`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ code: codeVal, language: codeLang })
                });
                if (astRes.ok) {
                    const astData = await astRes.json();
                    document.getElementById('ast-lang-badge').innerText = `${codeLang.toUpperCase()} AST`;
                    document.getElementById('ast-time-val').innerText = astData.estimated_time_complexity || 'O(1)';
                    document.getElementById('ast-space-val').innerText = astData.estimated_space_complexity || 'O(1)';
                    document.getElementById('ast-loop-depth-val').innerText = astData.loop_depth !== undefined ? astData.loop_depth : 0;
                    document.getElementById('ast-recursion-val').innerText = astData.has_recursion ? 'Yes (Recursive)' : 'No';
                    
                    const optList = document.getElementById('ast-optimizations-list');
                    if (optList) {
                        optList.innerHTML = '';
                        (astData.optimizations || ['Code complexity structure looks optimal.']).forEach(opt => {
                            const li = document.createElement('li');
                            li.innerHTML = `• ${escapeHtml(opt)}`;
                            optList.appendChild(li);
                        });
                    }
                    if (astSection) astSection.style.display = 'block';
                }
            } catch (e) {
                if (astSection) astSection.style.display = 'none';
            }
        } else {
            if (astSection) astSection.style.display = 'none';
        }
        
        // Select Primary Pattern
        selectPattern(primary);
        
    } catch (err) {
        outputDiv.innerHTML = `<div class="error-msg">An error occurred during pattern analysis: ${err.message}</div>`;
    }
}

// --- View Specific Pattern Details ---
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
    const timeComp = details.time_complexity || 'O(N)';
    const spaceComp = details.space_complexity || 'O(1)';
    const explanation = details.explanation || `Uses standard ${title} algorithmic mechanisms.`;
    const constraintAnalysis = details.constraint_analysis || `Optimal runtime complexity of ${timeComp} avoids TLE under standard input bounds.`;
    const mode = details.mode === 'gemini_ai' ? '⚡ Gemini Flash AI' : (details.mode === 'openai_ai' ? '🤖 OpenAI GPT-4o' : '💡 Heuristic Engine');
    
    // Update labels & headers
    document.getElementById('details-pattern-title').innerText = title;
    document.getElementById('analysis-mode-tag').innerText = mode;
    document.getElementById('time-complexity-val').innerText = timeComp;
    document.getElementById('space-complexity-val').innerText = spaceComp;
    document.getElementById('heuristic-explanation-val').innerText = explanation;
    document.getElementById('constraint-analysis-val').innerText = constraintAnalysis;
    
    // Update Boilerplates
    window._activeBoilerplates = details.boilerplates || {};
    renderBoilerplateCode();
    
    // Render Edge Cases & Common Traps
    const edgeList = document.getElementById('edge-cases-list');
    edgeList.innerHTML = '';
    const edgeCases = details.edge_cases || [
        "Empty or single element input boundary.",
        "Duplicate elements handling in test sets.",
        "Integer overflow with large values."
    ];
    edgeCases.forEach(ec => {
        const li = document.createElement('li');
        li.innerText = ec;
        edgeList.appendChild(li);
    });
    
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
    
    // Initialize interactive algorithm simulator for this pattern
    if (window.initVisualizerForPattern) {
        window.initVisualizerForPattern(patternKey);
    }
    
    // Show Details Card
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
            visContainer.innerHTML = `<div style="color:#ff7b72;">${data.flowchart || 'No flowchart available.'}</div>`;
        }
    } catch (e) {
        visContainer.innerHTML = '<div style="color:#ff7b72;">Failed to render flowchart.</div>';
    }
    
    // Source Code Annotation Highlights
    const codeSec = document.getElementById('annotated-code-section');
    if (window._cppcode && window._cppcode.trim()) {
        codeSec.style.display = 'block';
        let code = escapeHtml(window._cppcode);
        
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

// --- Visualization View Mode Tab Switcher (Simulator vs Flowchart) ---
window.switchVisView = function(view) {
    const simWrapper = document.getElementById('vis-view-simulator');
    const flowWrapper = document.getElementById('vis-view-flowchart');
    const simBtn = document.getElementById('vis-tab-sim');
    const flowBtn = document.getElementById('vis-tab-flow');
    
    if (view === 'sim') {
        if (simWrapper) simWrapper.style.display = 'block';
        if (flowWrapper) flowWrapper.style.display = 'none';
        if (simBtn) simBtn.classList.add('active');
        if (flowBtn) flowBtn.classList.remove('active');
    } else {
        if (simWrapper) simWrapper.style.display = 'none';
        if (flowWrapper) flowWrapper.style.display = 'block';
        if (simBtn) simBtn.classList.remove('active');
        if (flowBtn) flowBtn.classList.add('active');
    }
};

// --- Boilerplate Language Tab Switching ---
window.switchLanguageTab = function(lang) {
    window._activeLanguage = lang;
    document.querySelectorAll('.lang-tab-btn').forEach(btn => {
        if (btn.innerText.toLowerCase().includes(lang === 'cpp' ? 'c++' : (lang === 'javascript' ? 'js' : lang))) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    renderBoilerplateCode();
};

function renderBoilerplateCode() {
    const codeView = document.getElementById('boilerplate-code-view');
    const lang = window._activeLanguage || 'cpp';
    const code = (window._activeBoilerplates && window._activeBoilerplates[lang]) 
        ? window._activeBoilerplates[lang] 
        : `// No boilerplate template available for ${lang.toUpperCase()}`;
    codeView.innerText = code;
}

window.copyBoilerplateCode = function() {
    const codeView = document.getElementById('boilerplate-code-view');
    const copyBtn = document.getElementById('copy-boilerplate-btn');
    if (!codeView) return;
    
    navigator.clipboard.writeText(codeView.innerText).then(() => {
        const originalText = copyBtn.innerText;
        copyBtn.innerText = '✅ Copied!';
        setTimeout(() => {
            copyBtn.innerText = originalText;
        }, 1800);
    }).catch(() => {
        alert("Failed to copy code to clipboard.");
    });
};

function escapeHtml(unsafe) {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}

// --- Retrieve Saved Analysis History ---
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

// Reload history item back to main dashboard
window.reloadHistoryItem = function(encodedItem) {
    const item = JSON.parse(decodeURIComponent(encodedItem));
    
    document.getElementById('desc').value = item.problem_desc || "";
    document.getElementById('cppcode').value = item.code_snippet || "";
    document.getElementById('platform').value = item.platform || "";
    
    switchTab('analyser');
    runPatternAnalysis();
};

// --- Repository Analysis Scanner ---
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
                        plugins: { legend: { display: false } },
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

// --- Phase 5: Export Study Notes (Markdown) ---
window.exportStudyNotes = function() {
    const patternKey = window._activePattern || "dsa_pattern";
    const details = window._patternDetails[patternKey] || {};
    const title = details.title || patternKey.replace('_', ' ').toUpperCase();
    const timeComp = details.time_complexity || 'O(N)';
    const spaceComp = details.space_complexity || 'O(1)';
    const explanation = details.explanation || '';
    const constraintAnalysis = details.constraint_analysis || '';
    const edgeCases = details.edge_cases || [];
    const boilerplates = details.boilerplates || {};
    const problems = details.problems || [];

    let md = `# DSA Study Notes: ${title}\n\n`;
    md += `> **Time Complexity**: \`${timeComp}\` | **Space Complexity**: \`${spaceComp}\`\n\n`;
    md += `## 💡 Algorithmic Rationale\n${explanation}\n\n`;
    md += `## 📊 Constraint & Complexity Deduction\n${constraintAnalysis}\n\n`;
    
    if (edgeCases.length > 0) {
        md += `## ⚠️ Edge Cases & Common Traps\n`;
        edgeCases.forEach(ec => {
            md += `- [ ] ${ec}\n`;
        });
        md += `\n`;
    }

    if (boilerplates) {
        md += `## 💻 Multi-Language Boilerplates\n\n`;
        if (boilerplates.cpp) md += `### C++\n\`\`\`cpp\n${boilerplates.cpp}\n\`\`\`\n\n`;
        if (boilerplates.python) md += `### Python\n\`\`\`python\n${boilerplates.python}\n\`\`\`\n\n`;
        if (boilerplates.java) md += `### Java\n\`\`\`java\n${boilerplates.java}\n\`\`\`\n\n`;
        if (boilerplates.javascript) md += `### JavaScript\n\`\`\`javascript\n${boilerplates.javascript}\n\`\`\`\n\n`;
    }

    if (problems.length > 0) {
        md += `## 🎯 Curated Practice Problems\n`;
        problems.forEach(p => {
            md += `- [${p.title}](${p.url})\n`;
        });
        md += `\n`;
    }

    md += `---\n*Generated by DSA Pattern Analyser & AI Problem Solver*\n`;

    // Trigger client-side file download
    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${patternKey}_study_notes.md`;
    link.click();
};

// --- Phase 5: LeetCode Profile Mastery Analyzer ---
window.analyzeLeetCodeProfile = async function() {
    const userInput = document.getElementById('profile-username-input');
    const statusDiv = document.getElementById('profile-analyze-status');
    const summaryBox = document.getElementById('profile-summary-box');
    const chartCard = document.getElementById('profile-chart-container');
    const insightsCard = document.getElementById('profile-insights-container');
    const btn = document.getElementById('analyze-profile-btn');

    const username = userInput ? userInput.value.trim() : "";
    if (!username) {
        statusDiv.className = 'status-message error';
        statusDiv.innerText = 'Please enter a LeetCode username.';
        return;
    }

    statusDiv.className = 'status-message info';
    statusDiv.innerText = `Fetching ${username}'s submissions & tag distribution from LeetCode...`;
    summaryBox.style.display = 'none';
    chartCard.style.display = 'none';
    insightsCard.style.display = 'none';
    btn.disabled = true;
    btn.innerText = 'Analyzing...';

    try {
        const res = await fetch(`${API_BASE}/api/analyze-profile`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ username })
        });

        const data = await res.json();

        if (res.ok && data.status === 'success') {
            statusDiv.className = 'status-message success';
            statusDiv.innerText = `✅ Profile analysis for @${data.username} complete!`;

            // 1. Render Summary Pills
            document.getElementById('prof-total-solved').innerText = data.total_solved;
            document.getElementById('prof-easy-solved').innerText = data.difficulty_breakdown.easy;
            document.getElementById('prof-med-solved').innerText = data.difficulty_breakdown.medium;
            document.getElementById('prof-hard-solved').innerText = data.difficulty_breakdown.hard;
            summaryBox.style.display = 'block';

            // 2. Render Radar Chart
            chartCard.style.display = 'block';
            const canvas = document.getElementById('profile-radar-chart');
            if (window._profileRadarChart) {
                window._profileRadarChart.destroy();
            }

            window._profileRadarChart = new Chart(canvas, {
                type: 'radar',
                data: {
                    labels: data.radar.labels,
                    datasets: [{
                        label: 'Problems Solved',
                        data: data.radar.values,
                        backgroundColor: 'rgba(88, 166, 255, 0.25)',
                        borderColor: '#58a6ff',
                        pointBackgroundColor: '#bc8cff',
                        pointBorderColor: '#ffffff',
                        pointHoverBackgroundColor: '#ffffff',
                        pointHoverBorderColor: '#58a6ff',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            angleLines: { color: 'rgba(255, 255, 255, 0.08)' },
                            grid: { color: 'rgba(255, 255, 255, 0.08)' },
                            pointLabels: {
                                color: '#c9d1d9',
                                font: { family: 'Outfit', size: 11, weight: '600' }
                            },
                            ticks: {
                                backdropColor: 'transparent',
                                color: '#8b949e',
                                precision: 0
                            }
                        }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });

            // 3. Render Strengths & Blind Spots
            const strengthsList = document.getElementById('profile-strengths-list');
            strengthsList.innerHTML = '';
            data.strengths.forEach(s => {
                const li = document.createElement('li');
                li.innerText = s;
                strengthsList.appendChild(li);
            });

            const blindspotsList = document.getElementById('profile-blindspots-list');
            blindspotsList.innerHTML = '';
            data.blind_spots.forEach(b => {
                const li = document.createElement('li');
                li.innerText = b;
                blindspotsList.appendChild(li);
            });

            // 4. Render Recommended Bridge Problems
            const recList = document.getElementById('profile-recommendations-list');
            recList.innerHTML = '';
            data.recommendations.forEach(r => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span class="history-tag" style="margin-right:8px;">${r.pattern}</span>
                    <a href="${r.url}" target="_blank" class="problem-link">${r.title} (${r.difficulty}) ↗</a>
                `;
                recList.appendChild(li);
            });

            insightsCard.style.display = 'block';

        } else {
            statusDiv.className = 'status-message error';
            statusDiv.innerText = data.error || 'Failed to fetch LeetCode profile.';
        }
    } catch (err) {
        statusDiv.className = 'status-message error';
        statusDiv.innerText = `Error connecting to profile analyzer: ${err.message}`;
    } finally {
        btn.disabled = false;
        btn.innerText = 'Analyze Profile';
    }
};
