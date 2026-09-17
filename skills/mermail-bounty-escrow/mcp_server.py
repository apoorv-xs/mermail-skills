import sys
import os
import json
import urllib.request
from datetime import datetime, timezone
from mcp.server.fastmcp import FastMCP

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Initialize Mermail Bounty Escrow MCP Server (v3.0 - Verified Standard)
mcp = FastMCP("Mermail-Bounty-Escrow-MCP")

ENDPOINT = "https://console.mermail.app/mcp"
DEFAULT_MAILBOX = os.environ.get("MERMAIL_MAILBOX_ID", "")
SOLANA_RPC_URL = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
BASE_RPC_URL = os.environ.get("BASE_RPC_URL", "https://mainnet.base.org")

def _get_api_key():
    return os.environ.get("MERMAIL_API_KEY", "")

def _resolve_wallet(override_wallet: str = None) -> str:
    if override_wallet and override_wallet.strip():
        return override_wallet.strip()
    env_w = os.environ.get("AGENT_WALLET_ADDRESS", "").strip() or os.environ.get("SOLANA_WALLET_ADDRESS", "").strip()
    if env_w:
        return env_w
    return "WALLET_NOT_CONFIGURED"

def _resolve_mailbox(override_mailbox: str = None) -> str:
    if override_mailbox and override_mailbox.strip():
        return override_mailbox.strip()
    env_mb = os.environ.get("MERMAIL_MAILBOX_ID", "").strip()
    if env_mb:
        return env_mb
    api_key = _get_api_key()
    if api_key:
        try:
            res = _query_mermail_gateway("list_mailboxes", {})
            items = res.get("structuredContent", {}).get("items", [])
            if items:
                primary = items[0]
                return primary.get("public_id") or primary.get("email") or ""
        except Exception:
            pass
    return "agent@mermail.me"

def _query_mermail_gateway(tool_name: str, args: dict):
    req_body = {
        "jsonrpc": "2.0",
        "id": int(datetime.now().timestamp() * 1000) % 100000,
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
            "x-api-key": _get_api_key()
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("result", {})
    except Exception as e:
        return {"error": str(e), "isError": True}

def _query_solana_rpc(method: str, params: list) -> dict:
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    req = urllib.request.Request(
        SOLANA_RPC_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"content-type": "application/json", "User-Agent": "mermail-bounty-mcp/3.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

def _query_evm_rpc(to_address: str, data: str, rpc_url: str = BASE_RPC_URL) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_call",
        "params": [{"to": to_address, "data": data}, "latest"]
    }
    req = urllib.request.Request(
        rpc_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"content-type": "application/json", "User-Agent": "mermail-bounty-mcp/3.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def mermail_get_wallet(explicit_wallet: str = None) -> str:
    """Return the active agent settlement wallet and supported settlement networks."""
    wallet = _resolve_wallet(explicit_wallet)
    return json.dumps({
        "status": "connected",
        "chain": "Solana SPL / Base ERC-20",
        "wallet_address": wallet,
        "token_supported": ["USDC", "SOL"]
    }, indent=2)

@mcp.tool()
def mermail_fetch_inbox(query: str = "bounty", limit: int = 5, mailboxId: str = None) -> str:
    """Scan Mermail agent inbox for incoming RFPs and bounty milestone awards."""
    active_mailbox = _resolve_mailbox(mailboxId)
    res = _query_mermail_gateway("list_emails", {"mailboxId": active_mailbox})
    if "error" in res or res.get("isError"):
        return json.dumps({
            "source": "LIVE_MERMAIL_GATEWAY",
            "status": "error",
            "message": res.get("error", "Failed to query Mermail gateway"),
            "mailbox": active_mailbox,
            "inbox": []
        }, indent=2)

    raw_items = res.get("structuredContent", {}).get("items", [])
    parsed = []
    for item in raw_items[:limit]:
        parsed.append({
            "id": item.get("id"),
            "from": item.get("sender"),
            "subject": item.get("subject"),
            "date": item.get("date"),
            "snippet": (item.get("snippet") or "")[:120]
        })
    return json.dumps({
        "source": "LIVE_MERMAIL_GATEWAY",
        "mailbox": active_mailbox,
        "count": len(parsed),
        "inbox": parsed
    }, indent=2)

@mcp.tool()
def mermail_verify_escrow(escrow_address: str, expected_amount: float, chain: str = "solana") -> str:
    """Audit on-chain counterparty escrow locks via public RPC nodes prior to burning compute."""
    if not escrow_address or "..." in escrow_address or len(escrow_address) < 32:
        return json.dumps({
            "escrow_address": escrow_address,
            "chain": chain,
            "verified": False,
            "action": "HALT_UNFUNDED_COMPUTE",
            "reason": "Invalid or incomplete escrow address provided"
        }, indent=2)

    if chain.lower() == "solana":
        # Check SPL Token Account balance
        token_res = _query_solana_rpc("getTokenAccountBalance", [escrow_address])
        if "result" in token_res and "value" in token_res["result"]:
            val = token_res["result"]["value"]
            ui_amount = val.get("uiAmount", 0.0)
            if ui_amount >= expected_amount:
                return json.dumps({
                    "escrow_address": escrow_address,
                    "chain": "solana",
                    "verified": True,
                    "locked_usdc_balance": ui_amount,
                    "action": "PROCEED_WITH_EXECUTION"
                }, indent=2)

        # Check native SOL balance
        bal_res = _query_solana_rpc("getBalance", [escrow_address])
        if "result" in bal_res and "value" in bal_res["result"]:
            sol_bal = bal_res["result"]["value"] / 1e9
            if sol_bal > 0:
                return json.dumps({
                    "escrow_address": escrow_address,
                    "chain": "solana",
                    "verified": True,
                    "native_sol_balance": sol_bal,
                    "action": "PROCEED_WITH_EXECUTION"
                }, indent=2)

    elif chain.lower() in ("base", "evm", "ethereum"):
        clean_addr = escrow_address.lower().replace("0x", "").zfill(64)
        data = "0x70a08231" + clean_addr
        USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
        rpc_res = _query_evm_rpc(USDC_BASE, data)
        if "result" in rpc_res and rpc_res["result"] != "0x":
            try:
                raw_bal = int(rpc_res["result"], 16)
                bal = raw_bal / 1e6
                if bal >= expected_amount:
                    return json.dumps({
                        "escrow_address": escrow_address,
                        "chain": "base",
                        "verified": True,
                        "locked_usdc_balance": bal,
                        "action": "PROCEED_WITH_EXECUTION"
                    }, indent=2)
            except Exception:
                pass

    return json.dumps({
        "escrow_address": escrow_address,
        "chain": chain,
        "verified": False,
        "action": "HALT_UNFUNDED_COMPUTE",
        "reason": "On-chain escrow deposit unconfirmed on RPC"
    }, indent=2)

@mcp.tool()
def mermail_send_email(to: str, subject: str, body: str, mailboxId: str = None) -> str:
    """Dispatch RFC-compliant email and escrow claim via Mermail gateway."""
    active_mailbox = _resolve_mailbox(mailboxId)
    res = _query_mermail_gateway("send_email", {
        "mailboxId": active_mailbox,
        "body": {
            "from": active_mailbox,
            "to": to,
            "subject": subject,
            "text": body
        }
    })
    if "error" not in res and not res.get("isError"):
        structured = res.get("structuredContent", {})
        return json.dumps({
            "status": structured.get("status", "queued"),
            "id": structured.get("id"),
            "undo_until": structured.get("undo_until"),
            "sender": active_mailbox,
            "recipient": to,
            "subject": subject
        }, indent=2)

    return json.dumps({
        "status": "error",
        "details": res.get("error", "Unknown gateway dispatch error"),
        "sender": active_mailbox,
        "recipient": to
    }, indent=2)

if __name__ == "__main__":
    mcp.run()
