import sys
from typing import List

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("demo")


@mcp.tool()
async def echo_text(text: str) -> str:
    """Return the same text back."""
    print(f"[demo_server] echo_text called with: {text}", file=sys.stderr)
    return text


@mcp.tool()
async def list_items(category: str = "general") -> List[str]:
    """Return a small demo list of items."""
    print(f"[demo_server] list_items called with: {category}", file=sys.stderr)

    sample_data = {
        "general": ["item-1", "item-2", "item-3"],
        "fruits": ["apple", "banana", "orange"],
        "tickets": ["PAY-101", "PAY-109", "AUTH-210"],
        "prs": ["PR-142", "PR-151", "PR-199"],
    }

    return sample_data.get(
        category.lower(),
        [f"no items found for category '{category}'"]
    )


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()