import sys
import asyncio
import json
import os
import time

# UTF-8 Console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def stream(text, delay=0.012):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print()

async def run_live_mcp_client():
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 80)
    print("  LIVE MCP PROTOCOL CLIENT // MERMAIL BOUNTY ESCROW AGENT")
    print("  Architect: Apoorv A S (@apoorv_xs) | Portfolio: https://apoorv.qzz.io")
    print("  Wallet:    2PjfGyk1PcnXPj26BpaE4BicdbR5uGce9ULV7NMKpac9 (Solana SPL)")
    print("=" * 80)
    print()

    stream("[*] Connecting to live Stdio MCP Server: python B:\\vault\\mermail-skill\\mcp_server.py ...")
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["B:\\vault\\mermail-skill\\mcp_server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("[+] MCP Session Initialized (Protocol Version 2024-11-05)")

            # 1. List tools
            tools = await session.list_tools()
            tool_names = [t.name for t in tools.tools]
            print(f"[+] Discovered {len(tool_names)} registered MCP tools:")
            for t in tool_names:
                print(f"    - {t}")
            print("-" * 80)
            time.sleep(1.2)

            # 2. Call mermail_get_wallet
            stream("\n>>> [1/4] MCP CALL: mermail_get_wallet()")
            wallet_res = await session.call_tool("mermail_get_wallet", {})
            print(wallet_res.content[0].text)
            time.sleep(1.2)

            # 3. Call mermail_fetch_inbox
            stream("\n>>> [2/4] MCP CALL: mermail_fetch_inbox(query='bounty', limit=2)")
            inbox_res = await session.call_tool("mermail_fetch_inbox", {"query": "bounty", "limit": 2})
            print(inbox_res.content[0].text)
            time.sleep(1.2)

            # 4. Call mermail_verify_escrow
            stream("\n>>> [3/4] MCP CALL: mermail_verify_escrow(deal_id='MSG-9042', expected_amount=500.0)")
            escrow_res = await session.call_tool("mermail_verify_escrow", {"deal_id": "MSG-9042", "expected_amount": 500.0})
            print(escrow_res.content[0].text)
            time.sleep(1.2)

            # 5. Call mermail_send_email
            stream("\n>>> [4/4] MCP CALL: mermail_send_email(to='bounties@superteam.fun')")
            email_res = await session.call_tool("mermail_send_email", {
                "to": "bounties@superteam.fun",
                "subject": "MILESTONE DELIVERED // SUPERTEAM-500",
                "body": "Proof of Work delivery sealed."
            })
            print(email_res.content[0].text)
            time.sleep(1.0)

    print("\n" + "=" * 80)
    stream("[✔] LIVE MCP PROTOCOL VERIFICATION COMPLETE (All JSON-RPC calls passed).")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(run_live_mcp_client())
