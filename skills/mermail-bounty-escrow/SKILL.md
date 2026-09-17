---
name: mermail-bounty-escrow
description: Autonomous bounty settlement & milestone escrow agent skill powered by Mermail. Equips AI agents with an email identity and user-controlled Agent Wallet to audit counterparty escrow, prevent unfunded compute, and issue cryptographic proof-of-work receipts via email.
author: Apoorv A S (@apoorv_xs / @apoorv-xs)
repository: https://github.com/apoorv-xs
portfolio: https://apoorv.qzz.io
version: 1.0.0
---

# Mermail Bounty Escrow Skill (`mermail-bounty-escrow`)
> **Protocol:** Mermail Agent Wallet & Email Identity Protocol via Model Context Protocol (MCP)  
> **Author:** Apoorv A S ([@apoorv_xs](https://x.com/apoorv_xs) Â· [@apoorv-xs](https://github.com/apoorv-xs))  
> **Portfolio:** [https://apoorv.qzz.io](https://apoorv.qzz.io)  
> **Standard:** Solana SPL USDC & EVM ERC-20 Escrow Verification

---

## 1. Overview & Capabilities

The **`mermail-bounty-escrow`** skill solves the fundamental problem of **unfunded agent compute**. When autonomous agents write software, generate 3D assets, or execute client bounties, they risk burning developer resources without financial certainty.

This skill equips agents to:
1. **Receive & Parse Inbound RFPs:** Parse incoming bounty briefs and milestone requests delivered to `agent@mermail.me`.
2. **Audit On-Chain Counterparty Escrow:** Automatically query Solana / Base smart contracts or sender token approval before executing heavy workflows.
3. **Generate Cryptographic Proof-of-Work:** Recursively traverse build directories, hash production deliverables (SHA-256), and generate a signed delivery manifest (`DELIVERY_MANIFEST.json`).
4. **Autonomous Milestone Settlement:** Dispatch an RFC-compliant cryptographic receipt via Mermail email and request on-chain escrow release.

---

## 2. Interaction with Mermail MCP Tools

This skill directly integrates with standard Mermail Model Context Protocol (MCP) tools:

| Mermail MCP Tool | Input Payload | Skill Action |
| :--- | :--- | :--- |
| `mermail_fetch_inbox` | `{ "query": "bounty OR milestone", "limit": 10 }` | Ingests unread project RFPs & sponsor updates |
| `mermail_get_wallet` | `{}` | Returns the agent's public address and token balance |
| `mermail_verify_escrow` | `{ "deal_id": "MSG-9042", "expected_amount": 500.0 }` | Validates counterparty smart contract lock prior to compute |
| `mermail_send_email` | `{ "to": "client@org.com", "subject": "...", "body": "..." }` | Dispatches proof-of-work receipts and SOW milestone notices |

---

## 3. End-to-End Operational Workflow

```
[ Inbound Email via Mermail ]
              |
              v
[ Step 1: RFP Parsing ] 
    Agent extracts deal parameters, milestone tranches, and payout address.
              |
              v
[ Step 2: On-Chain Escrow Audit ]
    Agent queries Mermail Agent Wallet RPC for locked funds.
         /                 \
[ Escrow Locked ]    [ Escrow Missing ]
        |                    |
        v                    v
[ Step 3: Run Build ] [ Step 3b: Send SOW Terms ]
    Compiles assets &    Halts uncompensated compute &
    hashes directory     dispatches 50% deposit link.
        |
        v
[ Step 4: Issue Cryptographic Receipt ]
    Calculates composite root SHA-256 and dispatches
    proof-of-work delivery notice via Mermail.
```

---

## 4. Example Prompts & Expected Agent Responses

### Prompt 1: Triage Inbound Bounties
**User Prompt:**
> "Check my Mermail inbox for any new bounty opportunities or client RFPs and verify if any have locked escrow."

**Agent Action:**
```json
{
  "tool": "mermail_fetch_inbox",
  "arguments": { "limit": 5 }
}
```

**Expected Response:**
```text
Found 2 inbound opportunities:
1. Superteam Earn: "Build and Demo a Mermail Agent Skill" (500 USDC)
   - Escrow Status: VERIFIED on-chain (Contract: 0x94B0...e81A)
   - Recommendation: Approved to proceed with deliverable compilation.

2. Hyperion Intelligence: "3D Architecture Refactor" ($9,250 USDC)
   - Escrow Status: PENDING DEPOSIT
   - Action Taken: Halted build execution. Dispatched standard 50% upfront milestone agreement via Mermail.
```

---

### Prompt 2: Seal & Deliver Milestone with Cryptographic Proof
**User Prompt:**
> "Package the build artifacts in `./vault/mermail-skill/` for bounty 'SUPERTEAM-500', compute the root hash, and email the delivery receipt to bounties@superteam.fun."

**Agent Action:**
```bash
python mermail_bounty_escrow.py --action deliver --target-dir ./vault/mermail-skill/ --deal-id SUPERTEAM-500
python mermail_bounty_escrow.py --action dispatch --deal-id SUPERTEAM-500 --recipient bounties@superteam.fun
```

**Expected Output:**
- Generates `DELIVERY_MANIFEST.json` containing SHA-256 signatures for every file.
- Dispatches signed delivery email from `apoorv@mermail.me` with composite hash `0931c31688...`.

---

## 5. Security & Verification Standards

1. **Zero Unfunded Compute:** Never execute production GPU shaders, large render queues, or un-watermarked builds without confirmed escrow.
2. **Tamper-Evident Hashing:** Every deliverable manifest is cryptographically sealed with a root SHA-256 hash preventing post-delivery disputes.
3. **Multi-Chain Architecture:** Compatible with Solana SPL USDC and Base / EVM ERC-20 tokens managed through the Mermail Agent Wallet.
