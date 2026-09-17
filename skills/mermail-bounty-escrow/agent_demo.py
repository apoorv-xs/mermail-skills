import sys
import time
import os

# UTF-8 Console for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def stream_type(text, delay=0.015):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 80)
    print("  AUTONOMOUS AGENT RUNTIME: CLAUDE 3.7 SONNET // MERMAIL MCP BRIDGE")
    print("  Active Skill: mermail-bounty-escrow (v1.0.0)")
    print("  Principal:    Apoorv A S (@apoorv_xs) | https://apoorv.qzz.io")
    print("=" * 80)
    print()

    time.sleep(1.0)
    stream_type("USER PROMPT:")
    print('  "Agent, check my Mermail inbox for active Superteam bounties. If escrow is locked,')
    print('   seal the build deliverables in ./vault/mermail-skill and dispatch the delivery receipt."')
    print("-" * 80)
    time.sleep(1.5)

    stream_type("\n[AGENT REASONING]")
    print("  > Querying Mermail MCP server for unread bounty proposals...")
    time.sleep(1.0)

    stream_type("\n[TOOL CALL] mermail_fetch_inbox(query='bounty OR milestone', limit=5)")
    time.sleep(1.2)
    print("  └─ Response: Found MSG-9042 from bounties@superteam.fun | Reward: $500.00 USDC")
    time.sleep(1.0)

    stream_type("\n[AGENT REASONING]")
    print("  > Counterparty deal identified. Initiating Agent Wallet on-chain escrow audit...")
    time.sleep(1.2)

    stream_type("\n[TOOL CALL] mermail_verify_escrow(deal_id='MSG-9042', expected_usdc=500.0)")
    time.sleep(1.5)
    print("  └─ Status: VERIFIED (Contract: 0x94B0...e81A on Solana SPL)")
    print("  └─ Escrow balance of 500.00 USDC is locked. Execution approved.")
    time.sleep(1.2)

    stream_type("\n[AGENT REASONING]")
    print("  > Escrow verified. Computing cryptographic SHA-256 deliverable manifest...")
    time.sleep(1.2)

    stream_type("\n[TOOL CALL] execute_skill_action(action='deliver', dir='B:\\vault\\mermail-skill')")
    time.sleep(1.8)
    print("  └─ Hashed 4 production files.")
    print("  └─ Composite Root SHA-256: bdec2861ffdc3812fb568be18db1bfe68f70c94fc1cbd281c278c75e70cc3b6c")
    print("  └─ Output: B:\\vault\\mermail-skill\\DELIVERY_MANIFEST.json created.")
    time.sleep(1.2)

    stream_type("\n[AGENT REASONING]")
    print("  > Proof-of-work generated. Dispatching RFC delivery receipt and escrow release claim...")
    time.sleep(1.2)

    stream_type("\n[TOOL CALL] mermail_send_email(to='bounties@superteam.fun', subject='MILESTONE DELIVERED // MSG-9042')")
    time.sleep(1.8)
    print("  └─ Sender:  apoorv@mermail.me")
    print("  └─ Recipient: bounties@superteam.fun")
    print("  └─ Settlement Wallet: 2PjfGyk1PcnXPj26BpaE4BicdbR5uGce9ULV7NMKpac9")
    print("  └─ Status: DISPATCHED VIA MERMAIL GATEWAY (SMTP 250 OK)")
    time.sleep(1.0)

    print("\n" + "=" * 80)
    stream_type("AGENT EXECUTION COMPLETE: Autonomous settlement cycle finalized in 8.4s.")
    print("=" * 80)

if __name__ == "__main__":
    main()
