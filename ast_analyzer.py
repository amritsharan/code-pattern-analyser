import ast
import re

class CodeComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.max_loop_depth = 0
        self.current_loop_depth = 0
        self.loop_locations = []
        
        self.has_recursion = False
        self.recursion_functions = set()
        self.current_function = None
        self.function_calls = {}
        
        self.data_structures = set()
        self.nested_search_detected = False
        self.uses_sorting = False

    def visit_FunctionDef(self, node):
        prev_function = self.current_function
        self.current_function = node.name
        self.function_calls[node.name] = []
        
        self.generic_visit(node)
        
        # Check if the function calls itself (recursion)
        if self.current_function and self.current_function in self.function_calls.get(self.current_function, []):
            self.has_recursion = True
            self.recursion_functions.add(self.current_function)
            
        self.current_function = prev_function

    def visit_For(self, node):
        self.current_loop_depth += 1
        if self.current_loop_depth > self.max_loop_depth:
            self.max_loop_depth = self.current_loop_depth
            self.loop_locations.append(node.lineno)
            
        if self.current_loop_depth >= 2:
            self.nested_search_detected = True
            
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_While(self, node):
        self.current_loop_depth += 1
        if self.current_loop_depth > self.max_loop_depth:
            self.max_loop_depth = self.current_loop_depth
            self.loop_locations.append(node.lineno)
            
        if self.current_loop_depth >= 2:
            self.nested_search_detected = True
            
        self.generic_visit(node)
        self.current_loop_depth -= 1

    def visit_Call(self, node):
        call_name = ""
        if isinstance(node.func, ast.Name):
            call_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            call_name = node.func.attr
            
        if self.current_function and call_name:
            self.function_calls.setdefault(self.current_function, []).append(call_name)
            
        if call_name in ["sort", "sorted"]:
            self.uses_sorting = True
        elif call_name in ["list", "dict", "set", "deque", "defaultdict", "Counter"]:
            self.data_structures.add(call_name)
            
        self.generic_visit(node)

    def visit_List(self, node):
        self.data_structures.add("list")
        self.generic_visit(node)

    def visit_Dict(self, node):
        self.data_structures.add("dict")
        self.generic_visit(node)

    def visit_Set(self, node):
        self.data_structures.add("set")
        self.generic_visit(node)


def analyze_python_ast(code):
    """Parses Python code into an Abstract Syntax Tree (AST) to compute static complexity metrics."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return analyze_non_python_or_invalid_code(code, error=f"Python syntax error at line {e.lineno}")

    visitor = CodeComplexityVisitor()
    visitor.visit(tree)

    # 1. Estimate Time Complexity
    time_comp = "O(1)"
    if visitor.has_recursion:
        # Check branching factor in recursive calls
        rec_func = list(visitor.recursion_functions)[0] if visitor.recursion_functions else ""
        calls_count = visitor.function_calls.get(rec_func, []).count(rec_func)
        if calls_count >= 2:
            time_comp = "O(2^N) [Exponential]"
        else:
            time_comp = "O(N) [Linear Recursive]"
    elif visitor.max_loop_depth == 1:
        time_comp = "O(N log N)" if visitor.uses_sorting else "O(N)"
    elif visitor.max_loop_depth == 2:
        time_comp = "O(N^2)"
    elif visitor.max_loop_depth >= 3:
        time_comp = f"O(N^{visitor.max_loop_depth})"
    elif visitor.uses_sorting:
        time_comp = "O(N log N)"

    # 2. Estimate Space Complexity
    space_comp = "O(1)"
    if visitor.has_recursion:
        space_comp = "O(N) [Call Stack Depth]"
    elif any(ds in visitor.data_structures for ds in ["dict", "set", "list", "deque", "defaultdict", "Counter"]):
        space_comp = "O(N)"
    if visitor.max_loop_depth >= 2 and ("matrix" in code.lower() or "grid" in code.lower() or "dp" in code.lower()):
        space_comp = "O(N^2) or O(N*M)"

    # 3. Actionable Optimization Suggestions
    optimizations = []
    if visitor.nested_search_detected:
        optimizations.append("Nested loop structure detected. If performing element lookups or pair matching, consider replacing inner search with a Hash Map (O(1) lookup) or Two Pointers (on sorted array) to reduce complexity to O(N).")
    if visitor.uses_sorting and visitor.max_loop_depth >= 1:
        optimizations.append("Array sorting (O(N log N)) combined with traversal. Verify if a single-pass Hash Map or Heap can achieve linear O(N) performance.")
    if visitor.has_recursion and "memo" not in code.lower() and "cache" not in code.lower() and "@lru_cache" not in code:
        optimizations.append("Recursive function detected without visible memoization. If overlapping subproblems exist, adding @lru_cache or a memoization dictionary will prevent exponential O(2^N) time complexity.")

    if not optimizations:
        optimizations.append("Code structure is clean with linear or logarithmic complexity characteristics.")

    return {
        "status": "success",
        "language": "python",
        "estimated_time_complexity": time_comp,
        "estimated_space_complexity": space_comp,
        "loop_depth": visitor.max_loop_depth,
        "has_recursion": visitor.has_recursion,
        "recursion_functions": list(visitor.recursion_functions),
        "data_structures": list(visitor.data_structures),
        "optimizations": optimizations,
        "summary": f"AST Analysis: Max loop nesting depth is {visitor.max_loop_depth}, recursion: {'Yes' if visitor.has_recursion else 'No'}, data structures allocated: {', '.join(visitor.data_structures) if visitor.data_structures else 'None'}."
    }


def analyze_non_python_or_invalid_code(code, error=None):
    """Heuristic bracket and syntax analyzer for C++, Java, or JavaScript snippets."""
    # Count nested braces/loops
    for_count = len(re.findall(r'\bfor\s*\(', code))
    while_count = len(re.findall(r'\bwhile\s*\(', code))
    has_recursion = bool(re.search(r'\b(\w+)\s*\([^)]*\)\s*\{[^}]*\b\1\s*\(', code, re.DOTALL))
    
    # Estimate max loop depth using indentation or nested keywords
    max_depth = 1 if (for_count > 0 or while_count > 0) else 0
    if for_count >= 2 or while_count >= 2 or (for_count >= 1 and while_count >= 1):
        if re.search(r'for[^{]*\{[^}]*for', code, re.DOTALL) or re.search(r'for[^{]*\{[^}]*while', code, re.DOTALL) or re.search(r'while[^{]*\{[^}]*while', code, re.DOTALL):
            max_depth = 2
            
    time_comp = "O(1)"
    if has_recursion:
        time_comp = "O(N) to O(2^N)"
    elif max_depth == 1:
        time_comp = "O(N)"
    elif max_depth >= 2:
        time_comp = "O(N^2)"
        
    space_comp = "O(1)"
    if "vector" in code or "unordered_map" in code or "HashMap" in code or "ArrayList" in code or "Array" in code:
        space_comp = "O(N)"
    if has_recursion:
        space_comp = "O(N) [Call Stack]"

    optimizations = []
    if max_depth >= 2:
        optimizations.append("Nested loop detected (O(N^2)). If searching for pairs or subsegments, consider Two Pointers or a Hash Map to achieve O(N) runtime.")
    else:
        optimizations.append("Code maintains acceptable single-pass or logarithmic complexity.")

    return {
        "status": "success",
        "language": "cpp/java/generic",
        "estimated_time_complexity": time_comp,
        "estimated_space_complexity": space_comp,
        "loop_depth": max_depth,
        "has_recursion": has_recursion,
        "data_structures": ["collections/containers"] if space_comp == "O(N)" else [],
        "optimizations": optimizations,
        "summary": f"Structural Analysis: Estimated loop depth is {max_depth}, recursion: {'Yes' if has_recursion else 'No'}.",
        "note": error
    }


def analyze_code_ast(code, language="python"):
    """Main router for AST / Static Code Analysis."""
    if not code or not code.strip():
        return {
            "status": "empty",
            "estimated_time_complexity": "N/A",
            "estimated_space_complexity": "N/A",
            "loop_depth": 0,
            "has_recursion": False,
            "optimizations": ["No code provided for static AST analysis."]
        }
        
    lang = language.lower() if language else "python"
    if lang == "python" or "def " in code or "import " in code:
        return analyze_python_ast(code)
    else:
        return analyze_non_python_or_invalid_code(code)
