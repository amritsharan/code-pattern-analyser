import json
import urllib.request
import urllib.error

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

PATTERN_TAG_MAPPINGS = {
    "two_pointers": ["Two Pointers"],
    "sliding_window": ["Sliding Window"],
    "binary_search": ["Binary Search"],
    "dynamic_programming": ["Dynamic Programming", "Memoization"],
    "stack": ["Stack"],
    "monotonic_stack": ["Monotonic Stack"],
    "tree": ["Tree", "Binary Tree", "Binary Search Tree"],
    "graph": ["Graph", "Breadth-First Search", "Depth-First Search", "Shortest Path", "Topological Sort"],
    "heap": ["Heap (Priority Queue)"],
    "trie": ["Trie"],
    "union_find": ["Union Find"],
    "segment_tree": ["Segment Tree", "Binary Indexed Tree"],
    "backtracking": ["Backtracking"],
    "bit_manipulation": ["Bit Manipulation"],
    "greedy": ["Greedy"],
    "prefix_sum": ["Prefix Sum"]
}

CURATED_TARGET_PROBLEMS = {
    "dynamic_programming": [
        {"title": "LeetCode 70: Climbing Stairs", "difficulty": "Easy", "url": "https://leetcode.com/problems/climbing-stairs/"},
        {"title": "LeetCode 322: Coin Change", "difficulty": "Medium", "url": "https://leetcode.com/problems/coin-change/"},
        {"title": "LeetCode 300: Longest Increasing Subsequence", "difficulty": "Medium", "url": "https://leetcode.com/problems/longest-increasing-subsequence/"}
    ],
    "monotonic_stack": [
        {"title": "LeetCode 739: Daily Temperatures", "difficulty": "Medium", "url": "https://leetcode.com/problems/daily-temperatures/"},
        {"title": "LeetCode 496: Next Greater Element I", "difficulty": "Easy", "url": "https://leetcode.com/problems/next-greater-element-i/"},
        {"title": "LeetCode 84: Largest Rectangle in Histogram", "difficulty": "Hard", "url": "https://leetcode.com/problems/largest-rectangle-in-histogram/"}
    ],
    "sliding_window": [
        {"title": "LeetCode 3: Longest Substring Without Repeating Characters", "difficulty": "Medium", "url": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"},
        {"title": "LeetCode 209: Minimum Size Subarray Sum", "difficulty": "Medium", "url": "https://leetcode.com/problems/minimum-size-subarray-sum/"},
        {"title": "LeetCode 76: Minimum Window Substring", "difficulty": "Hard", "url": "https://leetcode.com/problems/minimum-window-substring/"}
    ],
    "graph": [
        {"title": "LeetCode 200: Number of Islands", "difficulty": "Medium", "url": "https://leetcode.com/problems/number-of-islands/"},
        {"title": "LeetCode 207: Course Schedule", "difficulty": "Medium", "url": "https://leetcode.com/problems/course-schedule/"},
        {"title": "LeetCode 743: Network Delay Time", "difficulty": "Medium", "url": "https://leetcode.com/problems/network-delay-time/"}
    ],
    "tree": [
        {"title": "LeetCode 104: Maximum Depth of Binary Tree", "difficulty": "Easy", "url": "https://leetcode.com/problems/maximum-depth-of-binary-tree/"},
        {"title": "LeetCode 226: Invert Binary Tree", "difficulty": "Easy", "url": "https://leetcode.com/problems/invert-binary-tree/"},
        {"title": "LeetCode 236: Lowest Common Ancestor", "difficulty": "Medium", "url": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/"}
    ],
    "two_pointers": [
        {"title": "LeetCode 167: Two Sum II - Sorted Array", "difficulty": "Medium", "url": "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/"},
        {"title": "LeetCode 11: Container With Most Water", "difficulty": "Medium", "url": "https://leetcode.com/problems/container-with-most-water/"},
        {"title": "LeetCode 15: 3Sum", "difficulty": "Medium", "url": "https://leetcode.com/problems/3sum/"}
    ],
    "binary_search": [
        {"title": "LeetCode 704: Binary Search", "difficulty": "Easy", "url": "https://leetcode.com/problems/binary-search/"},
        {"title": "LeetCode 33: Search in Rotated Sorted Array", "difficulty": "Medium", "url": "https://leetcode.com/problems/search-in-rotated-sorted-array/"},
        {"title": "LeetCode 875: Koko Eating Bananas", "difficulty": "Medium", "url": "https://leetcode.com/problems/koko-eating-bananas/"}
    ],
    "trie": [
        {"title": "LeetCode 208: Implement Trie (Prefix Tree)", "difficulty": "Medium", "url": "https://leetcode.com/problems/implement-trie-prefix-tree/"},
        {"title": "LeetCode 211: Design Add and Search Words", "difficulty": "Medium", "url": "https://leetcode.com/problems/design-add-and-search-words-data-structure/"}
    ],
    "union_find": [
        {"title": "LeetCode 547: Number of Provinces", "difficulty": "Medium", "url": "https://leetcode.com/problems/number-of-provinces/"},
        {"title": "LeetCode 684: Redundant Connection", "difficulty": "Medium", "url": "https://leetcode.com/problems/redundant-connection/"}
    ],
    "segment_tree": [
        {"title": "LeetCode 307: Range Sum Query - Mutable", "difficulty": "Medium", "url": "https://leetcode.com/problems/range-sum-query-mutable/"}
    ]
}


def fetch_leetcode_profile(username):
    """Fetches user problem solving statistics and tag breakdown from LeetCode public GraphQL."""
    query = """
    query userProfileStats($username: String!) {
      matchedUser(username: $username) {
        username
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
        tagProblemCounts {
          advanced {
            tagName
            tagSlug
            problemsSolved
          }
          intermediate {
            tagName
            tagSlug
            problemsSolved
          }
          fundamental {
            tagName
            tagSlug
            problemsSolved
          }
        }
      }
    }
    """

    payload = {
        "operationName": "userProfileStats",
        "query": query,
        "variables": {"username": username}
    }

    req = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
            "Referer": f"https://leetcode.com/{username}/"
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=12) as resp:
        data = json.loads(resp.read().decode('utf-8'))

    matched = data.get("data", {}).get("matchedUser")
    if not matched:
        raise ValueError(f"LeetCode user '{username}' was not found. Please check spelling.")

    # 1. Total Problems Solved
    submissions = matched.get("submitStatsGlobal", {}).get("acSubmissionNum", [])
    total_solved = 0
    easy_count = 0
    med_count = 0
    hard_count = 0
    for s in submissions:
        diff = s.get("difficulty", "")
        cnt = s.get("count", 0)
        if diff == "All":
            total_solved = cnt
        elif diff == "Easy":
            easy_count = cnt
        elif diff == "Medium":
            med_count = cnt
        elif diff == "Hard":
            hard_count = cnt

    # 2. Tag Breakdown Mapping
    tag_counts = {}
    tags_obj = matched.get("tagProblemCounts") or {}
    for group in ["fundamental", "intermediate", "advanced"]:
        for item in tags_obj.get(group, []):
            name = item.get("tagName")
            solved = item.get("problemsSolved", 0)
            if name:
                tag_counts[name] = solved

    # 3. Aggregate into DSA Pattern Scores
    pattern_scores = {}
    for pat_key, tag_names in PATTERN_TAG_MAPPINGS.items():
        total_for_pat = sum(tag_counts.get(tn, 0) for tn in tag_names)
        pattern_scores[pat_key] = total_for_pat

    # Find strengths and blind spots
    sorted_patterns = sorted(pattern_scores.items(), key=lambda x: x[1], reverse=True)
    strengths = [p[0] for p in sorted_patterns[:3] if p[1] > 0]
    
    # Blind spots: patterns with lowest solved count
    blind_spots = [p[0] for p in sorted_patterns if p[1] <= 5][:3]
    if not blind_spots:
        blind_spots = [p[0] for p in sorted_patterns[-3:]]

    # Curated recommendations based on blind spots
    recommendations = []
    for spot in blind_spots:
        probs = CURATED_TARGET_PROBLEMS.get(spot, [])
        for pr in probs[:2]:
            recommendations.append({
                "pattern": spot.replace('_', ' ').title(),
                "title": pr["title"],
                "difficulty": pr.get("difficulty", "Medium"),
                "url": pr["url"]
            })

    # Prepare radar chart labels and values (top 8 key patterns)
    radar_keys = ["two_pointers", "sliding_window", "binary_search", "tree", "graph", "dynamic_programming", "monotonic_stack", "heap"]
    radar_labels = [k.replace('_', ' ').title() for k in radar_keys]
    radar_values = [pattern_scores.get(k, 0) for k in radar_keys]

    return {
        "status": "success",
        "username": username,
        "total_solved": total_solved,
        "difficulty_breakdown": {
            "easy": easy_count,
            "medium": med_count,
            "hard": hard_count
        },
        "pattern_scores": pattern_scores,
        "radar": {
            "labels": radar_labels,
            "values": radar_values
        },
        "strengths": [s.replace('_', ' ').title() for s in strengths] if strengths else ["Starting Out"],
        "blind_spots": [b.replace('_', ' ').title() for b in blind_spots],
        "recommendations": recommendations,
        "summary": f"{username} has solved {total_solved} problems ({easy_count} Easy, {med_count} Med, {hard_count} Hard). Strongest areas: {', '.join(strengths) if strengths else 'N/A'}."
    }
