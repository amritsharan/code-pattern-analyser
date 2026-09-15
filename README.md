# DSA Pattern Analyser & AI Problem Solver 🚀

An end-to-end intelligent competitive programming companion that predicts optimal Data Structures and Algorithms (DSA) patterns, simulates execution step-by-step, performs AST code complexity inspection, scrapes problem URLs, and analyzes LeetCode user profile mastery.

---

## 🌟 Key Features

### 1. 🧠 Intelligent Multi-Model AI Engine
- **Cloud LLM Support**: Deep algorithmic reasoning powered by **Google Gemini (Gemini 1.5 Flash)** and **OpenAI (GPT-4o-mini)**.
- **Offline Heuristic Fallback**: High-speed, zero-dependency heuristic engine with weighted phrase relevance scoring.
- **Rich Structured Insights**:
  - Primary & secondary algorithmic pattern recognition with confidence rating.
  - Algorithmic justification (*"Why this pattern?"*).
  - Constraint-to-complexity evaluation ($N \le 10^5 \implies O(N \log N)$ or $O(N)$).
  - Multi-language solution boilerplates in **C++, Python, Java, and JavaScript**.
  - Edge cases & common traps checklist.
  - Curated LeetCode practice problems.

### 2. 🔗 One-Click Problem URL Importer
- Paste any URL from **LeetCode**, **Codeforces**, **CodeChef**, **HackerRank**, or **GeeksforGeeks**.
- Automatically extracts problem title, formatted description, input/output constraints, difficulty badge, and topic tags.
- Triggers instant pattern analysis in 1 click.

### 3. 🎬 Interactive Step-by-Step Algorithm Simulator
- Interactive animated visualizers for core patterns:
  - **Two Pointers**: Moving pointers ($L, R$) inward/outward, comparing sum against target, match highlighting.
  - **Sliding Window**: Dynamic window rectangle tracking active elements `[L..R]`, expanding right, shrinking left on boundary violations, tracking max sum.
  - **Binary Search**: Midpoint calculation, dynamic elimination of discarded halves.
  - **Monotonic Stack**: Split view showing array elements, push/pop operations, stack frame state, and resolved Next Greater Elements.
- **Playback Controls**: Step navigation (Prev/Next), Auto-Play/Pause with speed control ($0.75\times, 1.0\times, 2.0\times$), and Custom Input Array/Target modifier.
- **Dual View Mode**: Switch seamlessly between the Interactive Simulator and Mermaid Flowchart.

### 4. 🔬 IDE Code Editor & AST Code Complexity Analyzer
- **Code Editor**: Language selector (`Python 3`, `C++`, `Java`, `JavaScript`), Tab key indentation, and quick sample code loader.
- **Python AST Static Analyzer**:
  - Calculates loop nesting depth to determine Big-O Time Complexity ($O(1), O(N), O(N^2), O(N^3)$).
  - Detects recursive calls, recursion depth, and exponential branching ($O(2^N)$).
  - Analyzes container allocations (lists, dicts, sets, matrices) to estimate Space Complexity ($O(1), O(N), O(N^2)$).
  - Generates actionable optimization insights (e.g. replacing nested loops with Hash Maps / Two Pointers, or adding `@lru_cache` to unmemoized recursion).

### 5. 📊 LeetCode Profile Mastery Radar & Export Tools
- **LeetCode Profile Scanner**: Fetch submission stats and tag distributions for any LeetCode username.
- **DSA Pattern Radar Chart**: Visualize pattern mastery distribution.
- **Skill Gap Detection**: Identify top pattern strengths vs blind spots.
- **Tailored Practice Recommendations**: Curated problems to bridge skill gaps.
- **1-Click Markdown Study Notes Export**: Download structured revision notes for any problem.

---

## 🛠️ Requirements & Setup

### Requirements
- Python 3.8+
- Flask & Flask-CORS

### Installation
1. **Clone the repository**:
   ```sh
   git clone <repo-url>
   cd "code pattern analyser DSA"
   ```

2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```sh
   python app.py
   ```
   Open your browser at `http://127.0.0.1:5000`.

---

## ⚙️ AI Configuration (Optional)
Click the **"⚙️ AI Settings"** button on the top navbar to enter your **Google Gemini API Key** or **OpenAI API Key**. Keys are stored locally in your browser. If no key is provided, the app runs offline using its built-in heuristic engine.

---

## 📄 License
MIT License. Made with Flask, Vanilla JavaScript, and ❤️ for DSA!
