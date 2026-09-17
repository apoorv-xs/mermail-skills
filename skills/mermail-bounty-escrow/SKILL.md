---
name: mermail-bounty-escrow
description: Autonomous bounty settlement, milestone escrow audit, and proof-of-work receipt engine powered by Mermail. Equips AI agents with an email identity (agent@mermail.me) and Agent Wallet (Solana SPL / Base ERC-20) to audit counterparty escrow before compute, compile cryptographic delivery manifests, and dispatch RFC receipts via Mermail MCP.
metadata:
  openclaw:
    requires:
      env:
        - MERMAIL_API_KEY
    primaryEnv: MERMAIL_API_KEY
    homepage: https://docs.mermail.app/ai/skills
    emoji: "🛡️"
author: Apoorv A S (@apoorv_xs / @apoorv-xs)
repository: https://github.com/apoorv-xs
portfolio: https://apoorv.qzz.io
version: 2.0.0
---

# Mermail Bounty Escrow & Settlement Skill (`mermail-bounty-escrow`)

## Overview

Use this skill to protect autonomous agent compute, verify counterparty milestone escrow on-chain before executing heavy workflows (GLSL compilation, 3D WebGPU renders, code generation), compile tamper-evident SHA-256 deliverable manifests, and dispatch cryptographic delivery receipts directly through Mermail's native email gateway and Agent Wallet.

Read [references/tools.md](references/tools.md) for the exact FastMCP tool contract and JSON-RPC payloads. Read [references/workflows.md](references/workflows.md) for the 4-stage autonomous settlement sequence. Read [references/security.md](references/security.md) for Treasury Armor and uncompensated compute defense boundaries.

---

## Preferred Deliverables

- **Live Inbox Discovery:** Unread bounty opportunities and RFPs fetched via Mermail MCP (`list_emails` / `mermail_fetch_inbox`) with parsed dollar amounts and contract addresses.
- **On-Chain Escrow Verification:** Real-time audit of counterparty escrow deposits (Solana SPL USDC / Base ERC-20) before burning compute.
- **Immutable Proof-of-Work Package:** Cryptographically sealed deliverable manifest (`DELIVERY_MANIFEST.json`) with composite root SHA-256.
- **RFC Delivery Receipt:** Outbound email dispatched through Mermail gateway (`mermail_send_email`) with settlement wallet claim.

---

## Workflow

1. **Verify Mailbox & Identity:** Resolve the active Mermail mailbox (`list_mailboxes`). Prefer stable `public_id`. Verify Agent Wallet address via `mermail_get_wallet`.
2. **Scan & Parse Inbound RFPs:** Discover candidate bounty messages with `mermail_fetch_inbox`. Extract prize pool, token, sponsor email, and smart contract.
3. **Audit Counterparty Escrow (Treasury Armor):**
   - Execute `mermail_verify_escrow(deal_id, expected_amount)`.
   - **If Funded:** Grant compute execution approval and proceed to build.
   - **If Unfunded / Pending:** Halt compute immediately. Auto-dispatch standard 50% upfront milestone SOW terms to protect agent resources.
4. **Compile Cryptographic Delivery Proof:**
   - Hash all production build artifacts in the target workspace using SHA-256.
   - Calculate composite root hash and write `DELIVERY_MANIFEST.json`.
5. **Dispatch Milestone Claim & Release Notice:**
   - Construct RFC-compliant delivery receipt referencing the composite root hash and Agent Wallet.
   - Dispatch via `mermail_send_email` through the authenticated Mermail gateway.

---

## Official FastMCP Tool Reference

| Tool | Parameters | Description |
| :--- | :--- | :--- |
| `mermail_get_wallet` | `{}` | Returns the active agent settlement wallet (`2Pjf...MKpac9`) and supported chains |
| `mermail_fetch_inbox` | `{"query": "bounty", "limit": 5, "live": true}` | Queries live Mermail production inbox or simulation fallback |
| `mermail_verify_escrow` | `{"deal_id": "MSG-9042", "expected_amount": 500.0}` | Verifies on-chain counterparty contract locks prior to compute |
| `mermail_send_email` | `{"to": "...", "subject": "...", "body": "..."}` | Dispatches RFC delivery receipt directly via Mermail gateway |

---

## Example Agent Request & Response

### Request:
> "Check my Mermail inbox for active Superteam bounties. If escrow is verified on-chain, seal the build in `./vault/mermail-skill/` and email the delivery proof to bounties@superteam.fun."

### Autonomous Agent Action Sequence:
1. `mermail_fetch_inbox(query='bounty', limit=5)` → Finds `MSG-9042` ($500 USDC, Superteam Earn).
2. `mermail_verify_escrow(deal_id='MSG-9042', expected_amount=500.0)` → Status: `VERIFIED` on-chain (Contract `0x94B0...e81A`).
3. `execute_action(action='deliver', target_dir='.')` → Generates `DELIVERY_MANIFEST.json` (Root SHA-256 signed).
4. `mermail_send_email(to='bounties@superteam.fun', subject='MILESTONE DELIVERED // MSG-9042', ...)` → Dispatched via Mermail gateway (Status: `queued` / delivered).
