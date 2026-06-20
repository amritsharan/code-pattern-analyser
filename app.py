import os
import tempfile
import shutil
import subprocess
import sqlite3
from functools import wraps
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

# Import functions and constants from pattern_detector.py
from pattern_detector import (
    dsa_patterns,
    PATTERN_INFO,
    detect_patterns,
    detect_two_pointers,
    detect_sliding_window,
    detect_stack,
    detect_monotonic_stack,
    detect_queue,
    detect_tree,
    detect_heap,
    detect_dp,
    detect_graph,
    detect_binary_search,
    detect_prefix_sum,
    detect_trie,
    detect_union_find,
    detect_segment_tree,
    detect_backtracking,
    detect_bit_manipulation,
    detect_greedy,
    visualize_two_pointer_flowchart,
    visualize_sliding_window_flowchart,
    visualize_stack_flowchart,
    visualize_monotonic_stack_flowchart,
    visualize_queue_flowchart,
    visualize_tree_flowchart,
    visualize_heap_flowchart,
    visualize_dp_flowchart,
    visualize_graph_flowchart,
    visualize_binary_search_flowchart,
    visualize_prefix_sum_flowchart,
    visualize_trie_flowchart,
    visualize_union_find_flowchart,
    visualize_segment_tree_flowchart,
    visualize_backtracking_flowchart,
    visualize_bit_manipulation_flowchart,
    visualize_greedy_flowchart
)

# Try to load HuggingFace zero-shot pipeline for AI-based detection
try:
    from transformers import pipeline
    # Load model (fallbacks to rule-based if transformers/torch is missing or errors out)
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    HF_AVAILABLE = True
except Exception as e:
    print("[INFO] HuggingFace pipeline not available (falling back to rule-based):", e)
    classifier = None
    HF_AVAILABLE = False

# Helper for AI-based detection
def ai_detect_patterns(text, candidate_labels=None, threshold=0.3):
    if not HF_AVAILABLE or classifier is None:
        return []
    if candidate_labels is None:
        candidate_labels = list(dsa_patterns.keys())
    result = classifier(text, candidate_labels)
    return [label for label, score in zip(result['labels'], result['scores']) if score > threshold]

# --- Database Integration ---
DATABASE = 'dsa_analyser.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                problem_desc TEXT,
                code_snippet TEXT,
                detected_patterns TEXT,
                platform TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    print("[INFO] SQLite database initialized.")

# Initialize DB
init_db()

# --- Flask Configuration ---
app = Flask(__name__)
# Enable CORS for frontend cookies (session persistence)
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8000", "http://localhost:8000", "http://127.0.0.1:5000"])
app.secret_key = 'supersecretkey_dsa_pattern_analyser_key_2026'

# Map pattern names to detection functions
pattern_funcs = {
    'two_pointers': detect_two_pointers,
    'sliding_window': detect_sliding_window,
    'stack': detect_stack,
    'queue': detect_queue,
    'tree': detect_tree,
    'heap': detect_heap,
    'dynamic_programming': detect_dp,
    'graph': detect_graph,
    'binary_search': detect_binary_search,
    'prefix_sum': detect_prefix_sum,
    'trie': detect_trie,
    'union_find': detect_union_find,
    'segment_tree': detect_segment_tree,
    'monotonic_stack': detect_monotonic_stack,
    'backtracking': detect_backtracking,
    'bit_manipulation': detect_bit_manipulation,
    'greedy': detect_greedy
}

# --- Multi-lingual File Scanning for Repositories ---
def scan_files_for_patterns(folder):
    """Recursively scan C++, Python, and Java files for DSA patterns and aggregate stats."""
    stats = {k: 0 for k in pattern_funcs}
    file_hits = {k: [] for k in pattern_funcs}
    
    code_extensions = ('.cpp', '.h', '.hpp', '.cc', '.cxx', '.py', '.java')
    
    for root, _, files in os.walk(folder):
        for fname in files:
            if fname.lower().endswith(code_extensions):
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, encoding='utf-8', errors='ignore') as f:
                        code = f.read()
                    for pname, func in pattern_funcs.items():
                        result = func(code)
                        if result.get('detected'):
                            stats[pname] += 1
                            file_hits[pname].append(fpath)
                except Exception:
                    continue
    return stats, file_hits

# --- Authentication Decorator ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route('/session', methods=['GET'])
def check_session():
    if 'username' in session:
        return jsonify({'logged_in': True, 'username': session['username']})
    return jsonify({'logged_in': False}), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    password_hash = generate_password_hash(password)
    
    conn = get_db()
    try:
        conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()
        return jsonify({'message': 'Registration successful'})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 409
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        session['username'] = username
        return jsonify({'message': 'Login successful'})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out'})

@app.route('/detect', methods=['POST'])
@login_required
def detect():
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'No description text provided'}), 400
        
    patterns = []
    if HF_AVAILABLE:
        patterns = ai_detect_patterns(text, list(dsa_patterns.keys()))
    if not patterns:
        patterns = detect_patterns(text)
        
    # Get information details (complexity + LeetCode links) for each pattern
    pattern_details = {}
    for p in patterns:
        if p in PATTERN_INFO:
            pattern_details[p] = PATTERN_INFO[p]
            
    return jsonify({
        'patterns': patterns,
        'details': pattern_details
    })

@app.route('/detect-platform', methods=['POST'])
@login_required
def detect_platform():
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    platform = data.get('platform', '').strip().lower()
    
    if not text:
        return jsonify({'error': 'No description text provided'}), 400
        
    patterns = []
    if HF_AVAILABLE:
        patterns = ai_detect_patterns(text, list(dsa_patterns.keys()))
    if not patterns:
        patterns = detect_patterns(text)
        
    pattern_details = {}
    for p in patterns:
        if p in PATTERN_INFO:
            pattern_details[p] = PATTERN_INFO[p]
            
    return jsonify({
        'patterns': patterns,
        'platform': platform,
        'details': pattern_details
    })

# Unified Pasted Code Heuristic Analyzer
@app.route('/detect-code', methods=['POST'])
@login_required
def detect_code():
    data = request.get_json() or {}
    code = data.get('code', '').strip()
    if not code:
        return jsonify({'error': 'No code provided'}), 400
        
    detected = []
    explanations = {}
    
    for pname, func in pattern_funcs.items():
        res = func(code)
        if res.get('detected'):
            detected.append(pname)
            explanations[pname] = res.get('explanation')
            
    pattern_details = {}
    for p in detected:
        if p in PATTERN_INFO:
            details = PATTERN_INFO[p].copy()
            details['explanation'] = explanations[p]
            pattern_details[p] = details
            
    return jsonify({
        'patterns': detected,
        'details': pattern_details
    })

# Save query to history
@app.route('/history/save', methods=['POST'])
@login_required
def save_history():
    data = request.get_json() or {}
    desc = data.get('desc', '').strip()
    code = data.get('code', '').strip()
    patterns_list = data.get('patterns', [])
    platform = data.get('platform', '').strip()
    
    patterns_str = ",".join(patterns_list)
    username = session['username']
    
    conn = get_db()
    conn.execute(
        'INSERT INTO history (username, problem_desc, code_snippet, detected_patterns, platform) VALUES (?, ?, ?, ?, ?)',
        (username, desc, code, patterns_str, platform)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'History saved successfully'})

# Retrieve history
@app.route('/history', methods=['GET'])
@login_required
def get_history():
    username = session['username']
    conn = get_db()
    rows = conn.execute('SELECT * FROM history WHERE username = ? ORDER BY created_at DESC LIMIT 20', (username,)).fetchall()
    conn.close()
    
    history_list = []
    for r in rows:
        history_list.append({
            'id': r['id'],
            'problem_desc': r['problem_desc'],
            'code_snippet': r['code_snippet'],
            'detected_patterns': r['detected_patterns'].split(',') if r['detected_patterns'] else [],
            'platform': r['platform'],
            'created_at': r['created_at']
        })
    return jsonify({'history': history_list})

# Analyze whole GitHub Repository
@app.route('/analyze-repo', methods=['POST'])
@login_required
def analyze_repo():
    data = request.get_json() or {}
    repo_url = data.get('repo_url', '').strip()
    if not repo_url or not repo_url.startswith('https://github.com/'):
        return jsonify({'error': 'Invalid or missing GitHub repo URL.'}), 400
        
    temp_dir = tempfile.mkdtemp()
    try:
        # Clone repo
        subprocess.run(['git', 'clone', '--depth', '1', repo_url, temp_dir], check=True)
        stats, file_hits = scan_files_for_patterns(temp_dir)
        
        # Clean paths relative to temp_dir
        cleaned_file_hits = {}
        for k in file_hits:
            cleaned_file_hits[k] = [os.path.relpath(f, temp_dir) for f in file_hits[k]]
            
        return jsonify({'stats': stats, 'file_hits': cleaned_file_hits})
    except Exception as e:
        return jsonify({'error': f'Failed to analyze repo: {str(e)}'}), 500
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

# Visualization Flowchart Router
@app.route('/visualize', methods=['POST'])
@login_required
def visualize():
    data = request.get_json() or {}
    pattern = data.get('pattern', '').strip()
    
    flowcharts = {
        'two_pointers': visualize_two_pointer_flowchart,
        'sliding_window': visualize_sliding_window_flowchart,
        'stack': visualize_stack_flowchart,
        'monotonic_stack': visualize_monotonic_stack_flowchart,
        'queue': visualize_queue_flowchart,
        'tree': visualize_tree_flowchart,
        'heap': visualize_heap_flowchart,
        'dynamic_programming': visualize_dp_flowchart,
        'dp': visualize_dp_flowchart,
        'graph': visualize_graph_flowchart,
        'binary_search': visualize_binary_search_flowchart,
        'prefix_sum': visualize_prefix_sum_flowchart,
        'trie': visualize_trie_flowchart,
        'union_find': visualize_union_find_flowchart,
        'segment_tree': visualize_segment_tree_flowchart,
        'backtracking': visualize_backtracking_flowchart,
        'bit_manipulation': visualize_bit_manipulation_flowchart,
        'greedy': visualize_greedy_flowchart
    }
    
    if pattern in flowcharts:
        flowchart = flowcharts[pattern]()
    else:
        flowchart = 'No visualization available for this pattern.'
        
    return jsonify({'pattern': pattern, 'flowchart': flowchart})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
