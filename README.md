# DSA Pattern Analyser

A web application to detect the most likely Data Structures and Algorithms (DSA) patterns required to solve a given competitive programming problem. Supports both rule-based and AI-based (HuggingFace zero-shot) detection.

## Features
- User registration, login, logout with session persistence
- Modern dark-themed UI
- Paste any problem description and get DSA pattern suggestions
- Rule-based keyword matching (always available)
- AI-based detection using HuggingFace zero-shot classification (if supported)

## Requirements
- Python 3.8+
- Flask
- flask_cors
- transformers (for AI mode)
- torch >= 2.4 (for AI mode)

## Setup

1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd code pattern analyser DSA
   ```

2. **Install dependencies**
   ```sh
   pip install flask flask_cors
   pip install transformers torch  # For AI-based detection
   ```
   - For CPU only: `pip install torch --index-url https://download.pytorch.org/whl/cpu`
   - For CUDA (GPU): `pip install torch --index-url https://download.pytorch.org/whl/cu121`

3. **Run the backend**
   ```sh
   python app.py
   ```
   The app will be available at http://127.0.0.1:5000

4. **Access the frontend**
   - Open your browser and go to http://127.0.0.1:8000 if using a static server, or
   - Serve static files from Flask and access http://127.0.0.1:5000

## Usage
- Register a new user or log in with existing credentials.
- Paste a competitive programming problem description.
- Select a platform (optional) and click "Detect Patterns".
- The detected DSA patterns will be shown below.

## AI-based Detection
- If `transformers` and `torch >= 2.4` are installed, the app will use HuggingFace's zero-shot classification for smarter pattern detection.
- If not, it will fall back to rule-based keyword matching.

## Customization
- To improve rule-based detection, edit `pattern_detector.py` and expand the `dsa_patterns` dictionary with more keywords.
- To add more DSA patterns, add new keys and keywords to `dsa_patterns`.

## Troubleshooting
- If you see errors about PyTorch version, upgrade torch as shown above.
- If AI-based detection is not available, the app will still work with rule-based detection.
- For Windows symlink warnings, see [HuggingFace cache docs](https://huggingface.co/docs/huggingface_hub/how-to-cache#limitations).

## License
MIT

---

**Made with Flask, JavaScript, and ❤️ for DSA!**
