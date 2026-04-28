import os
import sys
from typing import List, Dict, Any, Optional

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("github")

GITHUB_API_BASE = "https://api.github.com"


def _get_headers() -> Dict[str, str]:
    token = os.getenv("GITHUB_TOKEN", "")
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


async def _get(url: str, params: Optional[Dict[str, Any]] = None) -> Any:
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.get(
            url,
            headers=_get_headers(),
            params=params or {},
        )
        response.raise_for_status()
        return response.json()


@mcp.tool()
async def list_pull_requests(
    owner: str,
    repo: str,
    state: str = "open",
    per_page: int = 5,
) -> List[Dict[str, Any]]:
    """List pull requests for a repository."""
    print(
        f"[github_server] list_pull_requests called with owner={owner}, repo={repo}, state={state}",
        file=sys.stderr,
    )

    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls"
    data = await _get(
        url,
        params={
            "state": state,
            "per_page": per_page,
        },
    )

    results: List[Dict[str, Any]] = []
    for pr in data:
        results.append(
            {
                "number": pr["number"],
                "title": pr["title"],
                "state": pr["state"],
                "html_url": pr["html_url"],
                "created_at": pr["created_at"],
                "user": pr["user"]["login"],
            }
        )
    return results


@mcp.tool()
async def search_issues(
    owner: str,
    repo: str,
    query: str,
    state: str = "open",
    per_page: int = 5,
) -> List[Dict[str, Any]]:
    """Search issues in a repository."""
    print(
        f"[github_server] search_issues called with owner={owner}, repo={repo}, query={query}",
        file=sys.stderr,
    )

    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues"
    data = await _get(
        url,
        params={
            "state": state,
            "per_page": per_page,
        },
    )

    query_lower = query.lower()
    results: List[Dict[str, Any]] = []

    for issue in data:
        # Skip PRs because GitHub issues endpoint can include PRs
        if "pull_request" in issue:
            continue

        title = issue.get("title", "")
        body = issue.get("body") or ""

        if query_lower in title.lower() or query_lower in body.lower():
            results.append(
                {
                    "number": issue["number"],
                    "title": title,
                    "state": issue["state"],
                    "html_url": issue["html_url"],
                    "created_at": issue["created_at"],
                    "user": issue["user"]["login"],
                }
            )

    return results[:per_page]


@mcp.tool()
async def list_commits(
    owner: str,
    repo: str,
    per_page: int = 5,
    sha: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """List recent commits for a repository or branch."""
    print(
        f"[github_server] list_commits called with owner={owner}, repo={repo}, sha={sha}",
        file=sys.stderr,
    )

    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/commits"
    params: Dict[str, Any] = {"per_page": per_page}
    if sha:
        params["sha"] = sha

    data = await _get(url, params=params)

    results: List[Dict[str, Any]] = []
    for commit in data:
        commit_data = commit.get("commit", {})
        author_data = commit_data.get("author", {}) or {}

        results.append(
            {
                "sha": commit["sha"],
                "message": commit_data.get("message", ""),
                "author": author_data.get("name", ""),
                "date": author_data.get("date", ""),
                "html_url": commit["html_url"],
            }
        )

    return results


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()