import re

# 1. Keywords Mapping for Text-Based Classification (Problem Descriptions)
dsa_patterns = {
    "sliding_window": [
        "window", "substring", "subarray", "consecutive", "contiguous", "longest substring", 
        "smallest window", "fixed window", "variable window", "at most k", "maximum sum subarray"
    ],
    "two_pointers": [
        "two pointers", "left and right", "start and end", "move pointers", "increment pointer", 
        "decrement pointer", "opposite ends", "pair sum", "sorted array", "palindrome"
    ],
    "binary_search": [
        "binary search", "sorted", "log n", "find position", "search in rotated", "lower bound", 
        "upper bound", "bisect", "minimize maximum", "maximize minimum", "guess the number"
    ],
    "stack": [
        "stack", "parentheses", "balanced", "reverse string", "push and pop", "undo", "backspace"
    ],
    "monotonic_stack": [
        "monotonic stack", "next greater", "next smaller", "previous greater", "previous smaller", 
        "rectangle in histogram", "daily temperatures", "trap rain water"
    ],
    "queue": [
        "queue", "fifo", "enqueue", "dequeue", "first in first out", "level order", 
        "breadth first search", "bfs", "sliding window maximum"
    ],
    "tree": [
        "tree", "binary tree", "bst", "root", "leaf", "traversal", "inorder", "preorder", 
        "postorder", "subtree", "height of tree", "depth of tree", "lca", "lowest common ancestor"
    ],
    "heap": [
        "heap", "priority queue", "kth largest", "kth smallest", "top k", "merge k sorted", 
        "min heap", "max heap", "median of stream"
    ],
    "dynamic_programming": [
        "dp", "dynamic programming", "subproblems", "overlapping subproblems", "optimal substructure", 
        "memoization", "tabulation", "state", "recurrence", "knapsack", "lcs", "lis", "coin change", 
        "fibonacci", "edit distance"
    ],
    "graph": [
        "graph", "dfs", "bfs", "adjacency list", "edge", "vertex", "shortest path", "dijkstra", 
        "bellman ford", "cycle detection", "topological sort", "mst", "kruskal", "prim", "bipartite"
    ],
    "prefix_sum": [
        "prefix sum", "cumulative sum", "running sum", "range sum", "sum from i to j", "subarray sum equals"
    ],
    "trie": [
        "trie", "prefix tree", "words", "dictionary", "insert word", "search word", "starts with", 
        "autocomplete", "spell checker"
    ],
    "union_find": [
        "union find", "disjoint set", "dsu", "connected components", "find parent", "union set", 
        "path compression", "union by rank", "redundant connection"
    ],
    "segment_tree": [
        "segment tree", "range query", "point update", "range update", "lazy propagation", 
        "fenwick tree", "binary indexed tree", "bit query"
    ],
    "backtracking": [
        "backtrack", "permutations", "combinations", "n-queens", "sudoku", "subsets", "recursion path", 
        "restore state", "visited list", "generate parentheses"
    ],
    "bit_manipulation": [
        "bit manipulation", "bitwise", "xor", "and operator", "or operator", "shift left", 
        "shift right", "binary representation", "power of two", "single number", "hamming weight"
    ],
    "greedy": [
        "greedy", "locally optimal", "global optimum", "choose best", "at each step", "minimize coins", 
        "maximize profit", "fractional knapsack", "interval scheduling", "jump game"
    ]
}

# 2. Comprehensive Details for Each Pattern (Complexity and Practice Problems)
PATTERN_INFO = {
    "two_pointers": {
        "title": "Two Pointers",
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "problems": [
            {"title": "LeetCode 167: Two Sum II - Sorted Input", "url": "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/"},
            {"title": "LeetCode 11: Container With Most Water", "url": "https://leetcode.com/problems/container-with-most-water/"},
            {"title": "LeetCode 15: 3Sum", "url": "https://leetcode.com/problems/3sum/"}
        ]
    },
    "sliding_window": {
        "title": "Sliding Window",
        "time_complexity": "O(N)",
        "space_complexity": "O(1) or O(K)",
        "problems": [
            {"title": "LeetCode 3: Longest Substring Without Repeating Characters", "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"},
            {"title": "LeetCode 209: Minimum Size Subarray Sum", "url": "https://leetcode.com/problems/minimum-size-subarray-sum/"},
            {"title": "LeetCode 76: Minimum Window Substring", "url": "https://leetcode.com/problems/minimum-window-substring/"}
        ]
    },
    "binary_search": {
        "title": "Binary Search",
        "time_complexity": "O(log N)",
        "space_complexity": "O(1)",
        "problems": [
            {"title": "LeetCode 704: Binary Search", "url": "https://leetcode.com/problems/binary-search/"},
            {"title": "LeetCode 33: Search in Rotated Sorted Array", "url": "https://leetcode.com/problems/search-in-rotated-sorted-array/"},
            {"title": "LeetCode 875: Koko Eating Bananas", "url": "https://leetcode.com/problems/koko-eating-bananas/"}
        ]
    },
    "stack": {
        "title": "Stack",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "problems": [
            {"title": "LeetCode 20: Valid Parentheses", "url": "https://leetcode.com/problems/valid-parentheses/"},
            {"title": "LeetCode 155: Min Stack", "url": "https://leetcode.com/problems/min-stack/"},
            {"title": "LeetCode 224: Basic Calculator", "url": "https://leetcode.com/problems/basic-calculator/"}
        ]
    },
    "monotonic_stack": {
        "title": "Monotonic Stack",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "problems": [
            {"title": "LeetCode 739: Daily Temperatures", "url": "https://leetcode.com/problems/daily-temperatures/"},
            {"title": "LeetCode 496: Next Greater Element I", "url": "https://leetcode.com/problems/next-greater-element-i/"},
            {"title": "LeetCode 84: Largest Rectangle in Histogram", "url": "https://leetcode.com/problems/largest-rectangle-in-histogram/"}
        ]
    },
    "queue": {
        "title": "Queue",
        "time_complexity": "O(1) per operation",
        "space_complexity": "O(N)",
        "problems": [
            {"title": "LeetCode 225: Implement Stack using Queues", "url": "https://leetcode.com/problems/implement-stack-using-queues/"},
            {"title": "LeetCode 933: Number of Recent Calls", "url": "https://leetcode.com/problems/number-of-recent-calls/"},
            {"title": "LeetCode 622: Design Circular Queue", "url": "https://leetcode.com/problems/design-circular-queue/"}
        ]
    },
    "tree": {
        "title": "Tree / Graph Traversal (Trees)",
        "time_complexity": "O(N)",
        "space_complexity": "O(H) recursion stack",
        "problems": [
            {"title": "LeetCode 104: Maximum Depth of Binary Tree", "url": "https://leetcode.com/problems/maximum-depth-of-binary-tree/"},
            {"title": "LeetCode 226: Invert Binary Tree", "url": "https://leetcode.com/problems/invert-binary-tree/"},
            {"title": "LeetCode 98: Validate Binary Search Tree", "url": "https://leetcode.com/problems/validate-binary-search-tree/"}
        ]
    },
    "heap": {
        "title": "Heap / Priority Queue",
        "time_complexity": "O(log N) push/pop",
        "space_complexity": "O(N)",
        "problems": [
            {"title": "LeetCode 215: Kth Largest Element in an Array", "url": "https://leetcode.com/problems/kth-largest-element-in-an-array/"},
            {"title": "LeetCode 347: Top K Frequent Elements", "url": "https://leetcode.com/problems/top-k-frequent-elements/"},
            {"title": "LeetCode 23: Merge k Sorted Lists", "url": "https://leetcode.com/problems/merge-k-sorted-lists/"}
        ]
    },
    "dynamic_programming": {
        "title": "Dynamic Programming",
        "time_complexity": "O(N * M) typical",
        "space_complexity": "O(N * M) or O(N)",
        "problems": [
            {"title": "LeetCode 70: Climbing Stairs", "url": "https://leetcode.com/problems/climbing-stairs/"},
            {"title": "LeetCode 322: Coin Change", "url": "https://leetcode.com/problems/coin-change/"},
            {"title": "LeetCode 300: Longest Increasing Subsequence", "url": "https://leetcode.com/problems/longest-increasing-subsequence/"}
        ]
    },
    "graph": {
        "title": "Graph Traversal / Algorithms",
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V + E)",
        "problems": [
            {"title": "LeetCode 200: Number of Islands", "url": "https://leetcode.com/problems/number-of-islands/"},
            {"title": "LeetCode 207: Course Schedule", "url": "https://leetcode.com/problems/course-schedule/"},
            {"title": "LeetCode 743: Network Delay Time", "url": "https://leetcode.com/problems/network-delay-time/"}
        ]
    },
    "prefix_sum": {
        "title": "Prefix Sum",
        "time_complexity": "O(N) setup, O(1) query",
        "space_complexity": "O(N) or O(1)",
        "problems": [
            {"title": "LeetCode 303: Range Sum Query - Immutable", "url": "https://leetcode.com/problems/range-sum-query-immutable/"},
            {"title": "LeetCode 560: Subarray Sum Equals K", "url": "https://leetcode.com/problems/subarray-sum-equals-k/"},
            {"title": "LeetCode 724: Find Pivot Index", "url": "https://leetcode.com/problems/find-pivot-index/"}
        ]
    },
    "trie": {
        "title": "Trie (Prefix Tree)",
        "time_complexity": "O(L) per word",
        "space_complexity": "O(N * C) nodes",
        "problems": [
            {"title": "LeetCode 208: Implement Trie (Prefix Tree)", "url": "https://leetcode.com/problems/implement-trie-prefix-tree/"},
            {"title": "LeetCode 211: Design Add and Search Words", "url": "https://leetcode.com/problems/design-add-and-search-words-data-structure/"},
            {"title": "LeetCode 212: Word Search II", "url": "https://leetcode.com/problems/word-search-ii/"}
        ]
    },
    "union_find": {
        "title": "Union Find / Disjoint Set (DSU)",
        "time_complexity": "O(α(N)) almost O(1)",
        "space_complexity": "O(N)",
        "problems": [
            {"title": "LeetCode 547: Number of Provinces", "url": "https://leetcode.com/problems/number-of-provinces/"},
            {"title": "LeetCode 684: Redundant Connection", "url": "https://leetcode.com/problems/redundant-connection/"},
            {"title": "LeetCode 323: Connected Components", "url": "https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/"}
        ]
    },
    "segment_tree": {
        "title": "Segment Tree / Range Queries",
        "time_complexity": "O(N) build, O(log N) query/update",
        "space_complexity": "O(N)",
        "problems": [
            {"title": "LeetCode 307: Range Sum Query - Mutable", "url": "https://leetcode.com/problems/range-sum-query-mutable/"},
            {"title": "LeetCode 308: Range Sum Query 2D - Mutable", "url": "https://leetcode.com/problems/range-sum-query-2d-mutable/"}
        ]
    },
    "backtracking": {
        "title": "Backtracking",
        "time_complexity": "O(K^N) or O(N!) exponential",
        "space_complexity": "O(N) recursion depth",
        "problems": [
            {"title": "LeetCode 46: Permutations", "url": "https://leetcode.com/problems/permutations/"},
            {"title": "LeetCode 78: Subsets", "url": "https://leetcode.com/problems/subsets/"},
            {"title": "LeetCode 51: N-Queens", "url": "https://leetcode.com/problems/n-queens/"}
        ]
    },
    "bit_manipulation": {
        "title": "Bit Manipulation",
        "time_complexity": "O(1) typical",
        "space_complexity": "O(1)",
        "problems": [
            {"title": "LeetCode 136: Single Number", "url": "https://leetcode.com/problems/single-number/"},
            {"title": "LeetCode 191: Number of 1 Bits", "url": "https://leetcode.com/problems/number-of-1-bits/"},
            {"title": "LeetCode 268: Missing Number", "url": "https://leetcode.com/problems/missing-number/"}
        ]
    },
    "greedy": {
        "title": "Greedy",
        "time_complexity": "O(N log N) sorted, O(N) typical",
        "space_complexity": "O(1) or O(N)",
        "problems": [
            {"title": "LeetCode 455: Assign Cookies", "url": "https://leetcode.com/problems/assign-cookies/"},
            {"title": "LeetCode 55: Jump Game", "url": "https://leetcode.com/problems/jump-game/"},
            {"title": "LeetCode 435: Non-overlapping Intervals", "url": "https://leetcode.com/problems/non-overlapping-intervals/"}
        ]
    }
}

# 3. Text keyword classifier fallback
# 3. Text keyword classifier with weighted scoring
def detect_patterns(text):
    text = text.lower()
    pattern_scores = {}
    
    for pattern, keywords in dsa_patterns.items():
        score = 0
        for kw in keywords:
            # Multi-word exact phrases get highest weight (e.g. "binary search" > "sorted")
            matches = len(re.findall(r'\b' + re.escape(kw) + r'\b', text))
            if matches > 0:
                word_count = len(kw.split())
                char_weight = len(kw)
                score += matches * (word_count * 10 + char_weight)
        
        if score > 0:
            pattern_scores[pattern] = score
            
    # Sort patterns in descending order of match relevance score
    sorted_patterns = sorted(pattern_scores.keys(), key=lambda p: pattern_scores[p], reverse=True)
    return sorted_patterns

# 4. Multi-language Heuristics Code Pattern Analyzers
def detect_two_pointers(code):
    # Matches loops with start/end or left/right pointers moving towards each other
    pointer_keywords = ["left", "right", "start", "end", "low", "high", "ptr1", "ptr2"]
    found_ptrs = [kw for kw in pointer_keywords if kw in code.lower()]
    
    # Heuristic: Find while/for conditions containing <, >, <=, >= with pointer words
    loop_cond = re.search(r'(while|for)\s*\(?.*?(left|start|low|ptr1).*?(<|<=|>|>=).*?(right|end|high|ptr2).*?\)?', code, re.IGNORECASE)
    py_loop_cond = re.search(r'while\s+.*?left|start|low|ptr1.*?<|<=|>|>=.*?right|end|high|ptr2', code, re.IGNORECASE)
    
    detected = bool(loop_cond or py_loop_cond or (len(found_ptrs) >= 2 and ("while" in code or "for" in code)))
    explanation = (
        "Detected Two Pointers pattern: Code uses indices/pointers (like left/right or start/end) initialized at opposite ends or offsets "
        "and advances them towards each other under a loop condition."
        if detected else "No clear Two Pointers pattern detected."
    )
    return {'detected': detected, 'explanation': explanation, 'pointers': found_ptrs}

def detect_sliding_window(code):
    # Look for window dimensions and bounds resizing
    keywords = ["window", "start", "end", "len", "left", "right"]
    found_kw = [kw for kw in keywords if kw in code.lower()]
    
    # Sliding window typical logic: while/for loop expanding right, nested while contracting left
    loop_nesting = re.search(r'(for|while).*?((while).*?(\+\+|--|\+=|-=))', code, re.DOTALL | re.IGNORECASE)
    has_window_var = "window" in code.lower()
    
    detected = has_window_var or (len(found_kw) >= 3 and loop_nesting)
    explanation = (
        "Detected Sliding Window pattern: Code maintains a range (window) that expands and contracts dynamically "
        "to search for an optimal subarray/substring."
        if detected else "No clear Sliding Window pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_stack(code):
    # Detect language specific stack templates
    cpp_stack = "stack<" in code or "std::stack<" in code
    java_stack = "Stack<" in code or "Deque<" in code or "ArrayDeque<" in code
    py_stack = re.search(r'\w+\s*=\s*\[\s*\]', code) and (".append(" in code and ".pop(" in code)
    
    detected = bool(cpp_stack or java_stack or py_stack or ("stack" in code.lower() and "pop" in code.lower()))
    explanation = (
        "Detected Stack pattern: Code uses a Last-In-First-Out (LIFO) stack collection or list "
        "supporting push and pop operations."
        if detected else "No clear Stack pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_monotonic_stack(code):
    # Needs a stack structure combined with a loop comparing array values
    has_stack = detect_stack(code)['detected']
    nested_loop = "while" in code and ("pop" in code or "pop_back" in code)
    comparisons = any(op in code for op in ["<", ">", "<=", ">="])
    
    detected = has_stack and nested_loop and comparisons
    explanation = (
        "Detected Monotonic Stack pattern: Code pops elements from a stack in a loop based on inequality comparisons "
        "to maintain elements in sorted order (increasing or decreasing)."
        if detected else "No clear Monotonic Stack pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_queue(code):
    cpp_q = "queue<" in code or "std::queue<" in code or "deque<" in code
    java_q = "Queue<" in code or "ArrayDeque<" in code or "LinkedList<" in code
    py_q = "deque" in code or "Queue" in code or "popleft" in code or "put(" in code
    
    detected = bool(cpp_q or java_q or py_q)
    explanation = (
        "Detected Queue pattern: Code uses a First-In-First-Out (FIFO) queue collection (like std::queue, deque, or ArrayDeque)."
        if detected else "No clear Queue pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_tree(code):
    keywords = ["TreeNode", "Node*", "BinaryTree", "left", "right", "root", "val"]
    found = [kw for kw in keywords if kw in code]
    
    # Left and right child pointers/fields are highly indicative of tree node structs
    has_ptrs = ("left" in code and "right" in code) or ("->left" in code or ".left" in code)
    
    detected = "TreeNode" in code or (len(found) >= 3 and has_ptrs)
    explanation = (
        "Detected Tree pattern: Structure or class resembles a TreeNode with left and right children, "
        "often traversed recursively."
        if detected else "No clear Tree pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_heap(code):
    cpp_heap = "priority_queue<" in code or "make_heap" in code
    java_heap = "PriorityQueue<" in code or "PriorityQueue" in code
    py_heap = "heapq" in code or "heappush" in code or "heappop" in code or "heapify" in code
    
    detected = bool(cpp_heap or java_heap or py_heap)
    explanation = (
        "Detected Heap/Priority Queue pattern: Code relies on priority queues or min/max heaps to "
        "retrieve elements dynamically by order/priority."
        if detected else "No clear Heap pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_dp(code):
    # DP matches memoization tables, lru_cache, 2D arrays, or iterative vectors named dp
    keywords = ["dp", "memo", "cache", "lru_cache", "memoize", "tabulation"]
    found_kw = [kw for kw in keywords if kw in code.lower()]
    
    array_inits = (
        "vector<vector<" in code or 
        "vector<int>" in code or 
        "new int[" in code or 
        re.search(r'\[\s*0\s*\]\s*\*\s*\w+', code) or
        re.search(r'\[\s*\[\s*0\s*\].*?\*.*?\]', code)
    )
    
    detected = len(found_kw) >= 1 or (array_inits and ("memo" in code.lower() or "dp" in code.lower()))
    explanation = (
        "Detected Dynamic Programming pattern: Code uses an array, vector, hash map, or caching decorators "
        "to store results of overlapping subproblems (memoization/tabulation)."
        if detected else "No DP pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_graph(code):
    keywords = ["adj", "graph", "edge", "edges", "vertex", "vertices", "visited", "dijkstra", "bfs", "dfs"]
    found = [kw for kw in keywords if kw in code.lower()]
    
    adjacency = "vector<vector<" in code or "List<List<" in code or "defaultdict(list)" in code or "adj.push_back" in code or "adj.add" in code
    
    detected = len(found) >= 2 or adjacency
    explanation = (
        "Detected Graph pattern: Code implements adjacency representations (list/matrix), tracks visited states, "
        "or performs traversals like Breadth-First Search (BFS) / Depth-First Search (DFS)."
        if detected else "No clear Graph pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_binary_search(code):
    # Binary search uses left/right boundaries, a midpoint division, and halving the search space
    has_ptrs = ("left" in code and "right" in code) or ("low" in code and "high" in code) or ("l" in code and "r" in code)
    has_mid = "mid" in code or "middle" in code
    has_div = "/ 2" in code or "// 2" in code or ">> 1" in code
    
    detected = (has_ptrs and has_mid and has_div) or "binary_search" in code.lower() or "bisect" in code.lower()
    explanation = (
        "Detected Binary Search pattern: Code calculates a mid-point index/value and splits the search range "
        "in half (left/right or low/high boundaries updated dynamically)."
        if detected else "No clear Binary Search pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_prefix_sum(code):
    keywords = ["prefix", "sum", "presum", "cumulative", "running"]
    found = [kw for kw in keywords if kw in code.lower()]
    
    prefix_calc = "prefix[i]" in code or "pref[i]" in code or "sum += arr[i]" in code or "running_sum" in code
    
    detected = ("prefix" in code.lower() and "sum" in code.lower()) or (len(found) >= 2 and prefix_calc)
    explanation = (
        "Detected Prefix Sum pattern: Code constructs an array or sequence of cumulative sums "
        "to achieve O(1) range sum queries."
        if detected else "No clear Prefix Sum pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_trie(code):
    detected = "trie" in code.lower() or "TrieNode" in code or "children" in code and ("insert" in code or "search" in code)
    explanation = (
        "Detected Trie pattern: Code defines hierarchical tree nodes containing dictionaries or character arrays (children) "
        "specifically optimized for prefix word matches."
        if detected else "No clear Trie pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_union_find(code):
    detected = "union" in code.lower() and "find" in code.lower() or "dsu" in code.lower() or "UnionFind" in code
    explanation = (
        "Detected Union-Find / Disjoint Set Union (DSU) pattern: Code keeps track of connected components "
        "via a parent array, find parent checks, and union merges."
        if detected else "No clear Union-Find pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_segment_tree(code):
    detected = "segmenttree" in code.lower() or "segment_tree" in code.lower() or ("build" in code.lower() and "query" in code.lower() and "update" in code.lower() and "tree" in code.lower())
    explanation = (
        "Detected Segment Tree pattern: Code maintains a range query tree with build, query, or update functions."
        if detected else "No Segment Tree pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_backtracking(code):
    # Matches recursive state restoration
    backtrack_action = "pop_back" in code or "remove(" in code or "visited[i] = false" in code or "visited.remove" in code or "visited[i] = 0" in code
    has_recursion = "dfs(" in code.lower() or "backtrack(" in code.lower() or "solve(" in code.lower()
    
    detected = "backtrack" in code.lower() or (has_recursion and backtrack_action)
    explanation = (
        "Detected Backtracking pattern: Code explores choices recursively, saving states, and restoring/cleaning them "
        "after return calls (e.g. pop_back or unmarking visited arrays)."
        if detected else "No backtracking pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_bit_manipulation(code):
    bitwise = any(op in code for op in ["&", "|", "^", "<<", ">>", "~"])
    binary_literals = "0b" in code or "0x" in code or "bit" in code.lower()
    
    detected = bitwise and ("bit" in code.lower() or "mask" in code.lower() or "1 << " in code)
    explanation = (
        "Detected Bit Manipulation pattern: Code uses bitwise operators (&, |, ^, shifts) "
        "to represent subsets, optimize space, or perform fast mathematical operations."
        if detected else "No clear Bit Manipulation pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}

def detect_greedy(code):
    sorting = "sort(" in code or "sorted(" in code or "Arrays.sort" in code or "Collections.sort" in code
    greedy_selection = "min(" in code or "max(" in code or "greedy" in code.lower()
    
    detected = "greedy" in code.lower() or (sorting and greedy_selection)
    explanation = (
        "Detected Greedy pattern: Code makes locally optimal choices at each step (e.g., sorting events and choosing the earliest finishing ones) "
        "to reach a global optimum."
        if detected else "No clear Greedy pattern detected."
    )
    return {'detected': detected, 'explanation': explanation}


# 5. Visualization flowcharts for Mermaid.js
def visualize_two_pointer_flowchart():
    return "flowchart TD\n    A[Initialize left and right pointers] --> B{left < right?}\n    B -- Yes --> C[Process elements at left and right]\n    C --> D[Move left or right pointer]\n    D --> B\n    B -- No --> E[End]"

def visualize_sliding_window_flowchart():
    return "flowchart TD\n    A[Initialize window pointers] --> B{End of array?}\n    B -- No --> C[Expand/contract window]\n    C --> D[Update result if needed]\n    D --> B\n    B -- Yes --> E[End]"

def visualize_stack_flowchart():
    return "flowchart TD\n    A[Initialize stack] --> B{Elements left?}\n    B -- Yes --> C[Process top of stack]\n    C --> D[Push/pop as needed]\n    D --> B\n    B -- No --> E[End]"

def visualize_monotonic_stack_flowchart():
    return "flowchart TD\n    A[Initialize stack] --> B{Stack not empty and condition?}\n    B -- Yes --> C[Pop from stack]\n    C --> B\n    B -- No --> D[Push to stack]\n    D --> E[Continue/End]"

def visualize_queue_flowchart():
    return "flowchart TD\n    A[Initialize queue] --> B{Elements left?}\n    B -- Yes --> C[Process front of queue]\n    C --> D[Enqueue/dequeue as needed]\n    D --> B\n    B -- No --> E[End]"

def visualize_tree_flowchart():
    return "flowchart TD\n    A[Start at root] --> B{Node exists?}\n    B -- Yes --> C[Process node]\n    C --> D[Recurse left/right]\n    D --> B\n    B -- No --> E[End]"

def visualize_heap_flowchart():
    return "flowchart TD\n    A[Build heap] --> B{Heap not empty?}\n    B -- Yes --> C[Extract min/max]\n    C --> D[Heapify]\n    D --> B\n    B -- No --> E[End]"

def visualize_dp_flowchart():
    return "flowchart TD\n    A[Initialize DP table/memo] --> B[Iterate or recurse subproblems]\n    B --> C[Fill DP table/memo]\n    C --> D[Return results]"

def visualize_graph_flowchart():
    return "flowchart TD\n    A[Start at source node] --> B{Nodes left?}\n    B -- Yes --> C[Visit neighbors]\n    C --> D[Mark visited]\n    D --> B\n    B -- No --> E[End]"

def visualize_binary_search_flowchart():
    return "flowchart TD\n    A[Initialize left/right pointers] --> B{left <= right?}\n    B -- Yes --> C[Calculate mid]\n    C --> D[Check mid value]\n    D --> E[Move left/right bounds]\n    E --> B\n    B -- No --> F[End]"

def visualize_prefix_sum_flowchart():
    return "flowchart TD\n    A[Compute prefix sums array] --> B[Answer range queries using sums] --> C[End]"

def visualize_trie_flowchart():
    return "flowchart TD\n    A[Start at root] --> B{Char exists in children?}\n    B -- Yes --> C[Move to child]\n    C --> B\n    B -- No --> D[Create new node]\n    D --> E[Continue/End]"

def visualize_union_find_flowchart():
    return "flowchart TD\n    A[Find root of node] --> B{Roots equal?}\n    B -- No --> C[Union roots]\n    B -- Yes --> D[Already connected]\n    C --> E[Continue]\n    D --> E"

def visualize_segment_tree_flowchart():
    return "flowchart TD\n    A[Build segment tree] --> B[Query/Update]\n    B --> C{Leaf node?}\n    C -- No --> D[Recurse left/right]\n    C -- Yes --> E[Return/Update value]\n    D --> B"

def visualize_backtracking_flowchart():
    return "flowchart TD\n    A[Choose option] --> B[Recurse]\n    B --> C{Valid solution?}\n    C -- Yes --> D[Record/Return]\n    C -- No --> E[Backtrack]\n    E --> A"

def visualize_bit_manipulation_flowchart():
    return "flowchart TD\n    A[Initialize mask/bit] --> B[Apply bitwise operation]\n    B --> C[Check/Update result]\n    C --> D[Continue/End]"

def visualize_greedy_flowchart():
    return "flowchart TD\n    A[Sort/Choose best option] --> B[Make greedy choice]\n    B --> C{Done?}\n    C -- No --> A\n    C -- Yes --> D[End]"
