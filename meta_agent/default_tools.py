import requests
import subprocess
import requests

from bs4 import BeautifulSoup


def web_search_tool(query: str) -> str:
    """
    Search the web for information. It is useful for finding information about current events, stocks, and other real-time information.
    """
    url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for result in soup.find_all("a", class_="result__a"):
        title = result.get_text()
        link = result["href"]
        results.append((title, link))

    return results


def python_repl_tool(code: str) -> str:
    """|
    Execute Python code and return the output.
    """
    try:
        result = subprocess.run(
            ["python", "-c", code], capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
