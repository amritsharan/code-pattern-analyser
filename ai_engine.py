import os
import json
import re
import urllib.request
import urllib.error
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
    detect_greedy
)

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

# Standard template boilerplates for DSA patterns across 4 languages
PATTERN_BOILERPLATES = {
    "two_pointers": {
        "cpp": """// Two Pointers Pattern - C++
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int twoPointersSolve(vector<int>& nums, int target) {
        int left = 0, right = nums.size() - 1;
        while (left < right) {
            int current_sum = nums[left] + nums[right];
            if (current_sum == target) {
                return true; // Match found
            } else if (current_sum < target) {
                left++;  // Need a larger sum
            } else {
                right--; // Need a smaller sum
            }
        }
        return false;
    }
};""",
        "python": """# Two Pointers Pattern - Python
class Solution:
    def two_pointers_solve(self, nums: list[int], target: int) -> bool:
        left, right = 0, len(nums) - 1
        while left < right:
            current_sum = nums[left] + nums[right]
            if current_sum == target:
                return True
            elif current_sum < target:
                left += 1
            else:
                right -= 1
        return False""",
        "java": """// Two Pointers Pattern - Java
public class Solution {
    public boolean twoPointersSolve(int[] nums, int target) {
        int left = 0, right = nums.length - 1;
        while (left < right) {
            int currentSum = nums[left] + nums[right];
            if (currentSum == target) {
                return true;
            } else if (currentSum < target) {
                left++;
            } else {
                right--;
            }
        }
        return false;
    }
}""",
        "javascript": """// Two Pointers Pattern - JavaScript
function twoPointersSolve(nums, target) {
    let left = 0, right = nums.length - 1;
    while (left < right) {
        const sum = nums[left] + nums[right];
        if (sum === target) return true;
        if (sum < target) left++;
        else right--;
    }
    return false;
}"""
    },
    "sliding_window": {
        "cpp": """// Sliding Window Pattern - C++
#include <string>
#include <unordered_map>
using namespace std;

class Solution {
public:
    int slidingWindowSolve(string s, int k) {
        unordered_map<char, int> count;
        int left = 0, max_len = 0;
        for (int right = 0; right < s.length(); right++) {
            count[s[right]]++;
            // Shrink window if constraint is violated
            while (count.size() > k) {
                count[s[left]]--;
                if (count[s[left]] == 0) count.erase(s[left]);
                left++;
            }
            max_len = max(max_len, right - left + 1);
        }
        return max_len;
    }
};""",
        "python": """# Sliding Window Pattern - Python
class Solution:
    def sliding_window_solve(self, s: str, k: int) -> int:
        char_map = {}
        left = 0
        max_len = 0
        for right, ch in enumerate(s):
            char_map[ch] = char_map.get(ch, 0) + 1
            # Shrink window when condition violated
            while len(char_map) > k:
                char_map[s[left]] -= 1
                if char_map[s[left]] == 0:
                    del char_map[s[left]]
                left += 1
            max_len = max(max_len, right - left + 1)
        return max_len""",
        "java": """// Sliding Window Pattern - Java
import java.util.HashMap;
import java.util.Map;

public class Solution {
    public int slidingWindowSolve(String s, int k) {
        Map<Character, Integer> counts = new HashMap<>();
        int left = 0, maxLen = 0;
        for (int right = 0; right < s.length(); right++) {
            char c = s.charAt(right);
            counts.put(c, counts.getOrDefault(c, 0) + 1);
            while (counts.size() > k) {
                char l = s.charAt(left);
                counts.put(l, counts.get(l) - 1);
                if (counts.get(l) == 0) counts.remove(l);
                left++;
            }
            maxLen = Math.max(maxLen, right - left + 1);
        }
        return maxLen;
    }
}""",
        "javascript": """// Sliding Window Pattern - JavaScript
function slidingWindowSolve(s, k) {
    const counts = new Map();
    let left = 0, maxLen = 0;
    for (let right = 0; right < s.length; right++) {
        counts.set(s[right], (counts.get(s[right]) || 0) + 1);
        while (counts.size > k) {
            counts.set(s[left], counts.get(s[left]) - 1);
            if (counts.get(s[left]) === 0) counts.delete(s[left]);
            left++;
        }
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}"""
    },
    "binary_search": {
        "cpp": """// Binary Search Pattern - C++
#include <vector>
using namespace std;

class Solution {
public:
    int binarySearchSolve(vector<int>& nums, int target) {
        int low = 0, high = nums.size() - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] == target) return mid;
            if (nums[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }
};""",
        "python": """# Binary Search Pattern - Python
class Solution:
    def binary_search_solve(self, nums: list[int], target: int) -> int:
        low, high = 0, len(nums) - 1
        while low <= high:
            mid = low + (high - low) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1""",
        "java": """// Binary Search Pattern - Java
public class Solution {
    public int binarySearchSolve(int[] nums, int target) {
        int low = 0, high = nums.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] == target) return mid;
            if (nums[mid] < target) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }
}""",
        "javascript": """// Binary Search Pattern - JavaScript
function binarySearchSolve(nums, target) {
    let low = 0, high = nums.length - 1;
    while (low <= high) {
        const mid = Math.floor(low + (high - low) / 2);
        if (nums[mid] === target) return mid;
        if (nums[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}"""
    },
    "monotonic_stack": {
        "cpp": """// Monotonic Stack Pattern (Next Greater Element) - C++
#include <vector>
#include <stack>
using namespace std;

class Solution {
public:
    vector<int> nextGreaterElements(vector<int>& nums) {
        int n = nums.size();
        vector<int> result(n, -1);
        stack<int> st; // stores indices
        for (int i = 0; i < n; i++) {
            while (!st.empty() && nums[st.top()] < nums[i]) {
                result[st.top()] = nums[i];
                st.pop();
            }
            st.push(i);
        }
        return result;
    }
};""",
        "python": """# Monotonic Stack Pattern - Python
class Solution:
    def next_greater_elements(self, nums: list[int]) -> list[int]:
        n = len(nums)
        result = [-1] * n
        stack = []  # Stores indices
        for i, val in enumerate(nums):
            while stack and nums[stack[-1]] < val:
                idx = stack.pop()
                result[idx] = val
            stack.append(i)
        return result""",
        "java": """// Monotonic Stack Pattern - Java
import java.util.Arrays;
import java.util.Stack;

public class Solution {
    public int[] nextGreaterElements(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        Arrays.fill(result, -1);
        Stack<Integer> stack = new Stack<>();
        for (int i = 0; i < n; i++) {
            while (!stack.isEmpty() && nums[stack.peek()] < nums[i]) {
                result[stack.pop()] = nums[i];
            }
            stack.push(i);
        }
        return result;
    }
}""",
        "javascript": """// Monotonic Stack Pattern - JavaScript
function nextGreaterElements(nums) {
    const result = new Array(nums.length).fill(-1);
    const stack = []; // stores indices
    for (let i = 0; i < nums.length; i++) {
        while (stack.length > 0 && nums[stack[stack.length - 1]] < nums[i]) {
            const idx = stack.pop();
            result[idx] = nums[i];
        }
        stack.push(i);
    }
    return result;
}"""
    },
    "dynamic_programming": {
        "cpp": """// Dynamic Programming Pattern - C++
#include <vector>
#include <algorithm>
using namespace std;

class Solution {
public:
    int dpSolve(vector<int>& nums) {
        int n = nums.size();
        if (n == 0) return 0;
        vector<int> dp(n + 1, 0);
        // Base cases
        dp[0] = 0;
        for (int i = 1; i <= n; i++) {
            // State transition equation
            dp[i] = dp[i - 1] + nums[i - 1]; 
        }
        return dp[n];
    }
};""",
        "python": """# Dynamic Programming Pattern - Python
class Solution:
    def dp_solve(self, nums: list[int]) -> int:
        n = len(nums)
        if not nums:
            return 0
        dp = [0] * (n + 1)
        # Base case
        dp[0] = 0
        for i in range(1, n + 1):
            # Recurrence relation
            dp[i] = max(dp[i - 1], dp[i - 1] + nums[i - 1])
        return dp[n]""",
        "java": """// Dynamic Programming Pattern - Java
public class Solution {
    public int dpSolve(int[] nums) {
        int n = nums.length;
        if (n == 0) return 0;
        int[] dp = new int[n + 1];
        dp[0] = 0;
        for (int i = 1; i <= n; i++) {
            dp[i] = Math.max(dp[i - 1], dp[i - 1] + nums[i - 1]);
        }
        return dp[n];
    }
}""",
        "javascript": """// Dynamic Programming Pattern - JavaScript
function dpSolve(nums) {
    const n = nums.length;
    if (n === 0) return 0;
    const dp = new Array(n + 1).fill(0);
    dp[0] = 0;
    for (let i = 1; i <= n; i++) {
        dp[i] = Math.max(dp[i - 1], dp[i - 1] + nums[i - 1]);
    }
    return dp[n];
}"""
    },
    "tree": {
        "cpp": """// Tree Traversal Pattern - C++
#include <algorithm>
using namespace std;

struct TreeNode {
    int val;
    TreeNode *left;
    TreeNode *right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

class Solution {
public:
    int maxDepth(TreeNode* root) {
        if (!root) return 0;
        int leftDepth = maxDepth(root->left);
        int rightDepth = maxDepth(root->right);
        return 1 + max(leftDepth, rightDepth);
    }
};""",
        "python": """# Tree Traversal Pattern - Python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def max_depth(self, root: TreeNode | None) -> int:
        if not root:
            return 0
        left_depth = self.max_depth(root.left)
        right_depth = self.max_depth(root.right)
        return 1 + max(left_depth, right_depth)""",
        "java": """// Tree Traversal Pattern - Java
class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode(int x) { val = x; }
}

public class Solution {
    public int maxDepth(TreeNode root) {
        if (root == null) return 0;
        int leftDepth = maxDepth(root.left);
        int rightDepth = maxDepth(root.right);
        return 1 + Math.max(leftDepth, rightDepth);
    }
}""",
        "javascript": """// Tree Traversal Pattern - JavaScript
function maxDepth(root) {
    if (!root) return 0;
    const leftDepth = maxDepth(root.left);
    const rightDepth = maxDepth(root.right);
    return 1 + Math.max(leftDepth, rightDepth);
}"""
    },
    "graph": {
        "cpp": """// Graph BFS/DFS Traversal - C++
#include <vector>
#include <queue>
using namespace std;

class Solution {
public:
    void bfs(int start, vector<vector<int>>& adj, vector<bool>& visited) {
        queue<int> q;
        q.push(start);
        visited[start] = true;
        while (!q.empty()) {
            int node = q.front();
            q.pop();
            for (int neighbor : adj[node]) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    q.push(neighbor);
                }
            }
        }
    }
};""",
        "python": """# Graph BFS Traversal - Python
from collections import deque

class Solution:
    def bfs(self, start: int, adj: dict[int, list[int]], n: int):
        visited = [False] * n
        q = deque([start])
        visited[start] = True
        while q:
            node = q.popleft()
            for neighbor in adj.get(node, []):
                if not visited[neighbor]:
                    visited[neighbor] = True
                    q.append(neighbor)""",
        "java": """// Graph BFS Traversal - Java
import java.util.*;

public class Solution {
    public void bfs(int start, List<List<Integer>> adj, int n) {
        boolean[] visited = new boolean[n];
        Queue<Integer> q = new LinkedList<>();
        q.add(start);
        visited[start] = true;
        while (!q.isEmpty()) {
            int node = q.poll();
            for (int neighbor : adj.get(node)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    q.add(neighbor);
                }
            }
        }
    }
}""",
        "javascript": """// Graph BFS Traversal - JavaScript
function bfs(start, adj, n) {
    const visited = new Array(n).fill(false);
    const q = [start];
    visited[start] = true;
    while (q.length > 0) {
        const node = q.shift();
        for (const neighbor of (adj[node] || [])) {
            if (!visited[neighbor]) {
                visited[neighbor] = true;
                q.push(neighbor);
            }
        }
    }
}"""
    }
}

PATTERN_EDGE_CASES = {
    "two_pointers": [
        "Array with fewer than 2 elements or empty array.",
        "Array with all identical elements.",
        "Integer overflow during sum operations with large inputs.",
        "Sorted order requirement: confirm if input array is strictly sorted beforehand."
    ],
    "sliding_window": [
        "Empty string or array (size 0).",
        "Window size larger than the input array size (K > N).",
        "All elements are distinct or all elements are duplicate.",
        "Negative numbers when calculating cumulative sum windows."
    ],
    "binary_search": [
        "Single-element array [x] where target matches or is absent.",
        "Mid-point calculation overflow (use low + (high - low) / 2).",
        "Duplicates in array when searching for boundary conditions (lower/upper bound).",
        "Target is smaller than minimum or larger than maximum element."
    ],
    "monotonic_stack": [
        "Strictly increasing vs strictly decreasing input array.",
        "Duplicate adjacent values in input sequence.",
        "No greater/smaller element exists (handle default placeholder like -1 or infinity).",
        "Circular array cases requiring traversing up to 2*N indices."
    ],
    "dynamic_programming": [
        "Base cases: empty inputs (N=0), single element (N=1).",
        "Memory limit exceeded: check if 2D DP can be optimized to 1D rolling array.",
        "Negative weight values or unreachable subproblems initialized to infinity.",
        "Integer overflow when accumulating large state values."
    ],
    "graph": [
        "Disconnected graph with multiple independent components.",
        "Cycles in directed/undirected graphs causing infinite recursion if visited set is omitted.",
        "Self-loops and multi-edges between the same vertex pairs.",
        "Graph with single node and zero edges."
    ],
    "tree": [
        "Empty tree (root == null).",
        "Skewed tree (degenerated linked list) causing recursion stack overflow O(N).",
        "Single root node without left or right children.",
        "Duplicate values in Binary Search Tree."
    ],
    "heap": [
        "K is larger than total number of elements.",
        "Min-heap vs Max-heap inversion required for top-K largest vs smallest.",
        "Handling elements with equal priorities/frequencies."
    ],
    "backtracking": [
        "State not properly restored after recursive calls (failing to undo choice).",
        "Missing base termination condition causing stack overflow.",
        "Duplicate permutations/combinations generated when input has duplicates."
    ],
    "bit_manipulation": [
        "Bit shifting beyond word size (e.g. 1 << 32 in 32-bit signed integers).",
        "Sign bit handling for negative numbers in two's complement.",
        "Precedence of bitwise operators vs arithmetic/comparison operators."
    ],
    "greedy": [
        "Local optimum does not guarantee global optimum (counterexamples exist).",
        "Sorting ties handling (e.g. interval end times vs start times).",
        "Empty inputs or single elements."
    ]
}

def generate_rule_based_ai_response(problem_text, code_snippet=None, platform=""):
    """
    Generates a structured, rich AI-like response using heuristic rule matching and curated DSA knowledge.
    Guarantees reliable, instant responses even without an external API key.
    """
    # Detect patterns from description
    desc_patterns = detect_patterns(problem_text) if problem_text else []
    
    # Detect patterns from code snippet
    code_patterns = []
    code_explanations = {}
    if code_snippet:
        for pname, func in pattern_funcs.items():
            res = func(code_snippet)
            if res.get('detected'):
                code_patterns.append(pname)
                code_explanations[pname] = res.get('explanation')

    # Merge and prioritize
    merged_patterns = list(dict.fromkeys(desc_patterns + code_patterns))
    if not merged_patterns:
        merged_patterns = ["two_pointers"] # Sensible fallback
        primary_pattern = "two_pointers"
        confidence = 0.50
    else:
        primary_pattern = merged_patterns[0]
        confidence = 0.92 if len(desc_patterns) > 0 and len(code_patterns) > 0 else 0.85

    secondary_patterns = [p for p in merged_patterns if p != primary_pattern]
    
    # Pattern info
    info = PATTERN_INFO.get(primary_pattern, {
        "title": primary_pattern.replace('_', ' ').title(),
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "problems": []
    })

    title = info.get('title', primary_pattern.replace('_', ' ').title())
    time_comp = info.get('time_complexity', 'O(N)')
    space_comp = info.get('space_complexity', 'O(1)')
    
    # Justification
    if code_snippet and primary_pattern in code_explanations:
        justification = code_explanations[primary_pattern]
    else:
        justification = f"The problem characteristics match the {title} pattern. This approach enables optimal processing of constraints in {time_comp} time and {space_comp} auxiliary space without redundant brute-force evaluations."

    # Constraint Analysis
    constraint_analysis = (
        f"For typical competitive programming constraints (N ≤ 10⁵ to 10⁶), the {title} pattern provides "
        f"an optimal {time_comp} runtime, avoiding Time Limit Exceeded (TLE) errors associated with naive brute-force O(N²) or exponential approaches."
    )

    # Boilerplates
    boilerplates = PATTERN_BOILERPLATES.get(primary_pattern, PATTERN_BOILERPLATES.get("two_pointers"))
    
    # Edge Cases
    edge_cases = PATTERN_EDGE_CASES.get(primary_pattern, [
        "Empty or single element input.",
        "Duplicate input values.",
        "Integer overflow during accumulation."
    ])

    # Practice Problems
    practice_problems = info.get('problems', [])

    return {
        "primary_pattern": primary_pattern,
        "primary_pattern_title": title,
        "secondary_patterns": secondary_patterns,
        "confidence_score": confidence,
        "justification": justification,
        "constraint_analysis": constraint_analysis,
        "time_complexity": time_comp,
        "space_complexity": space_comp,
        "boilerplates": boilerplates,
        "edge_cases": edge_cases,
        "practice_problems": practice_problems,
        "mode": "heuristic"
    }


def call_gemini_api(api_key, problem_text, code_snippet=None, platform=""):
    """
    Calls Google Gemini API to get deep AI pattern analysis and structured JSON output.
    """
    prompt = f"""You are an elite Competitive Programming & Data Structures / Algorithms coach.
Analyze the following competitive programming problem or code snippet and return a strictly formatted JSON object.

Problem Description:
\"\"\"{problem_text or "No problem description provided"}\"\"\"

Code Snippet:
\"\"\"{code_snippet or "No code snippet provided"}\"\"\"

Target Platform: {platform or "General / LeetCode"}

Respond with ONLY a valid, parseable JSON object matching this exact schema:
{{
  "primary_pattern": "<one of: two_pointers, sliding_window, binary_search, stack, monotonic_stack, queue, tree, heap, dynamic_programming, graph, prefix_sum, trie, union_find, segment_tree, backtracking, bit_manipulation, greedy>",
  "primary_pattern_title": "<Human Readable Pattern Name>",
  "secondary_patterns": ["<other applicable pattern keys>"],
  "confidence_score": <float between 0.0 and 1.0>,
  "justification": "<Concise, clear explanation of why this pattern is optimal for this problem>",
  "constraint_analysis": "<Analysis of time/space complexity based on problem input constraints (e.g. N <= 10^5)>",
  "time_complexity": "<Big-O Time Complexity, e.g. O(N log N)>",
  "space_complexity": "<Big-O Space Complexity, e.g. O(1)>",
  "boilerplates": {{
    "cpp": "<Complete, clean C++ solution starter code>",
    "python": "<Complete, clean Python 3 solution starter code>",
    "java": "<Complete, clean Java solution starter code>",
    "javascript": "<Complete, clean JavaScript solution starter code>"
  }},
  "edge_cases": [
    "<Edge case 1>",
    "<Edge case 2>",
    "<Edge case 3>"
  ],
  "practice_problems": [
    {{"title": "<LeetCode Problem Name 1>", "url": "<LeetCode URL or search link>"}},
    {{"title": "<LeetCode Problem Name 2>", "url": "<LeetCode URL or search link>"}}
  ]
}}
Do NOT wrap the response in markdown code fences. Output valid JSON only."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=15) as resp:
        res_data = json.loads(resp.read().decode('utf-8'))
        
    candidate_text = res_data['candidates'][0]['content']['parts'][0]['text']
    # Clean potential markdown fences
    candidate_text = re.sub(r'^```(json)?\s*', '', candidate_text.strip(), flags=re.IGNORECASE)
    candidate_text = re.sub(r'\s*```$', '', candidate_text.strip())
    
    parsed = json.loads(candidate_text)
    parsed["mode"] = "gemini_ai"
    return parsed


def call_openai_api(api_key, problem_text, code_snippet=None, platform=""):
    """
    Calls OpenAI / OpenAI-compatible API for structured JSON pattern analysis.
    """
    prompt = f"""You are an elite Competitive Programming & Data Structures / Algorithms coach.
Analyze the following problem and return a strictly formatted JSON object with DSA patterns, complexity, boilerplates in C++, Python, Java, JavaScript, edge cases, and practice problems.

Problem: {problem_text}
Code: {code_snippet}
Platform: {platform}"""

    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a DSA pattern recognition engine. Respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=15) as resp:
        res_data = json.loads(resp.read().decode('utf-8'))

    candidate_text = res_data['choices'][0]['message']['content']
    parsed = json.loads(candidate_text)
    parsed["mode"] = "openai_ai"
    return parsed


def analyze_dsa_problem(problem_text, code_snippet=None, platform="", api_key=None, api_provider="gemini"):
    """
    Primary interface for analyzing DSA problems.
    Uses AI API if key provided; otherwise seamlessly uses rule-based heuristic AI fallback.
    """
    # Priority: explicitly passed key from user modal > environment key
    key = ""
    if api_key and isinstance(api_key, str) and api_key.strip():
        key = api_key.strip()
    elif api_provider == "openai":
        env_key = os.environ.get("OPENAI_API_KEY", "").strip()
        if env_key and "your_api_key" not in env_key.lower():
            key = env_key
    else:
        env_key = os.environ.get("GEMINI_API_KEY", "").strip()
        if env_key and "your_api_key" not in env_key.lower():
            key = env_key
    
    # Only make network request if a non-placeholder key is supplied
    if key and len(key) >= 15 and key != "undefined" and key != "null" and "your_api_key" not in key.lower():
        try:
            if api_provider == "openai" or key.startswith("sk-"):
                return call_openai_api(key, problem_text, code_snippet, platform)
            else:
                return call_gemini_api(key, problem_text, code_snippet, platform)
        except Exception as e:
            print(f"[WARN] AI API call failed ({e}). Falling back to heuristic engine.")
            res = generate_rule_based_ai_response(problem_text, code_snippet, platform)
            res["api_warning"] = f"AI API call returned: {str(e)}. Displaying heuristic analysis."
            return res
            
    # Default rule-based structured analysis
    return generate_rule_based_ai_response(problem_text, code_snippet, platform)
