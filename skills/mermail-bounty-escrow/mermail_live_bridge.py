import sys
import os
import json
import urllib.request

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mermail-live")

ENDPOINT = "https://console.mermail.app/mcp"
API_KEY = os.environ.get("MERMAIL_API_KEY", "")

def _forward_mcp(tool_name: str, args: dict):
    req_body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": args
        }
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(req_body).encode("utf-8"),
        headers={
            "accept": "application/json, text/event-stream",
            "content-type": "application/json",
            "x-api-key": API_KEY
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return json.dumps(data.get("result", {}), indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

@mcp.tool()
def list_mailboxes() -> str:
    """List all available Mermail mailboxes in the active workspace."""
    return _forward_mcp("list_mailboxes", {})

@mcp.tool()
def list_workspaces() -> str:
    """List all Mermail workspaces and quota details."""
    return _forward_mcp("list_workspaces", {})

@mcp.tool()
def list_emails(mailboxId: str = "ricksanchez@mermail.app") -> str:
    """List emails from the specified Mermail mailbox."""
    return _forward_mcp("list_emails", {"mailboxId": mailboxId})

@mcp.tool()
def send_email(mailboxId: str, to: str, subject: str, body: str) -> str:
    """Send an email via the authenticated Mermail agent mailbox."""
    return _forward_mcp("send_email", {
        "mailboxId": mailboxId,
        "to": [to] if isinstance(to, str) else to,
        "subject": subject,
        "body": body
    })

if __name__ == "__main__":
    mcp.run()
