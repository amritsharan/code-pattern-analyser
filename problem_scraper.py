import re
import json
import html
import urllib.request
import urllib.parse
import urllib.error

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def clean_html_to_text(html_content):
    """Converts HTML content to clean, readable plaintext with proper spacing and symbols."""
    if not html_content:
        return ""
    
    # Replace paragraph and break tags with newlines
    text = re.sub(r'<\s*br\s*/?>', '\n', html_content, flags=re.IGNORECASE)
    text = re.sub(r'<\s*/\s*p\s*>', '\n\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<\s*/\s*li\s*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<\s*li\s*>', '• ', text, flags=re.IGNORECASE)
    text = re.sub(r'<\s*/\s*div\s*>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<\s*/\s*h[1-6]\s*>', '\n\n', text, flags=re.IGNORECASE)
    
    # Remove all remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Unescape HTML entities (e.g. &lt; to <, &quot; to ", &nbsp; to space)
    text = html.unescape(text)
    
    # Normalize non-breaking spaces and irregular whitespace
    text = text.replace('\xa0', ' ').replace('\u200b', '').replace('\ufeff', '')
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Clean up redundant empty lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def scrape_leetcode(url):
    """Scrapes problem title, content, difficulty, and tags from LeetCode using its public GraphQL API."""
    match = re.search(r'leetcode\.com/problems/([^/?#]+)', url)
    if not match:
        raise ValueError("Invalid LeetCode problem URL format. Expected: https://leetcode.com/problems/<problem-slug>/")
    
    title_slug = match.group(1).rstrip('/')
    graphql_url = "https://leetcode.com/graphql"
    
    query = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        questionFrontendId
        title
        titleSlug
        difficulty
        content
        topicTags {
          name
          slug
        }
        hints
      }
    }
    """
    
    payload = {
        "operationName": "getQuestionDetail",
        "query": query,
        "variables": {"titleSlug": title_slug}
    }
    
    req = urllib.request.Request(
        graphql_url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
            "Referer": f"https://leetcode.com/problems/{title_slug}/"
        },
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=12) as response:
        data = json.loads(response.read().decode('utf-8'))
        
    question = data.get("data", {}).get("question")
    if not question:
        raise ValueError("LeetCode problem not found or problem slug is invalid.")
        
    raw_html = question.get("content") or ""
    clean_desc = clean_html_to_text(raw_html)
    
    tags = [t.get("name") for t in question.get("topicTags", []) if t.get("name")]
    
    return {
        "platform": "leetcode",
        "title": f"LeetCode {question.get('questionFrontendId')}: {question.get('title')}",
        "difficulty": question.get("difficulty", "Medium"),
        "description": clean_desc,
        "tags": tags,
        "url": f"https://leetcode.com/problems/{title_slug}/"
    }


def scrape_codeforces(url):
    """Scrapes problem title and description from Codeforces."""
    match = re.search(r'codeforces\.com/(?:contest|problemset/problem)/(\d+)/([A-Za-z0-9]+)', url)
    if not match:
        raise ValueError("Invalid Codeforces problem URL format. Expected: https://codeforces.com/problemset/problem/<contestId>/<index>")
        
    contest_id, index = match.group(1), match.group(2)
    fetch_url = f"https://codeforces.com/contest/{contest_id}/problem/{index}"
    
    req = urllib.request.Request(
        fetch_url,
        headers={"User-Agent": USER_AGENT}
    )
    
    with urllib.request.urlopen(req, timeout=12) as response:
        page_html = response.read().decode('utf-8', errors='ignore')
        
    # Extract title
    title_match = re.search(r'<div class="title">\s*([^<]+)\s*</div>', page_html)
    title = title_match.group(1).strip() if title_match else f"Codeforces {contest_id}{index}"
    
    # Extract statement body
    statement_match = re.search(r'<div class="problem-statement">(.*?)<div class="sample-tests">', page_html, re.DOTALL)
    if statement_match:
        statement_html = statement_match.group(1)
        # Remove header section containing time limit etc from description body
        statement_html = re.sub(r'<div class="header">.*?</div>', '', statement_html, flags=re.DOTALL)
        clean_desc = clean_html_to_text(statement_html)
    else:
        clean_desc = clean_html_to_text(page_html[:4000])
        
    return {
        "platform": "codeforces",
        "title": f"Codeforces {contest_id}{index}: {title}",
        "difficulty": "Competitive",
        "description": clean_desc,
        "tags": ["Codeforces"],
        "url": fetch_url
    }


def scrape_generic_url(url):
    """Generic fallback scraper for other problem platforms (GeeksforGeeks, HackerRank, etc.)"""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT}
    )
    
    with urllib.request.urlopen(req, timeout=12) as response:
        page_html = response.read().decode('utf-8', errors='ignore')
        
    # Extract page title
    title_match = re.search(r'<title>(.*?)</title>', page_html, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Problem Statement"
    title = html.unescape(title)
    
    # Try to find main content or article
    main_match = re.search(r'<(?:article|main)[^>]*>(.*?)</(?:article|main)>', page_html, re.IGNORECASE | re.DOTALL)
    if main_match:
        clean_desc = clean_html_to_text(main_match.group(1))
    else:
        clean_desc = clean_html_to_text(page_html[:5000])
        
    platform = "general"
    if "geeksforgeeks.org" in url:
        platform = "geeksforgeeks"
    elif "hackerrank.com" in url:
        platform = "hackerrank"
    elif "codechef.com" in url:
        platform = "codechef"
        
    return {
        "platform": platform,
        "title": title,
        "difficulty": "Unknown",
        "description": clean_desc,
        "tags": [],
        "url": url
    }


def scrape_problem(url):
    """Main routing dispatcher to scrape competitive programming problem URLs."""
    if not url or not isinstance(url, str):
        raise ValueError("Problem URL is required.")
        
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
        
    if "leetcode.com" in url:
        return scrape_leetcode(url)
    elif "codeforces.com" in url:
        return scrape_codeforces(url)
    else:
        return scrape_generic_url(url)
