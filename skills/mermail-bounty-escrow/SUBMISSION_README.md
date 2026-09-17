# Superteam Earn Submission: Mermail Agent Skill
## Project: Autonomous Bounty Escrow & Milestone Delivery Skill (`mermail-bounty-escrow`)

> **Bounty Track:** Build and Demo a Mermail Agent Skill  
> **Prize Pool:** 500 USDC  
> **Architect & Submitter:** Apoorv A S ([@apoorv_xs](https://x.com/apoorv_xs) · [@apoorv-xs](https://github.com/apoorv-xs))  
> **Role:** Creative Technologist & 3D WebUI Architect | Creator, ERAVEX (Spatial Computing & WebGPU Engine)  
> **Portfolio:** [https://apoorv.qzz.io](https://apoorv.qzz.io)  
> **Repository Core:** `B:\vault\mermail-skill\` (ERAVEX Vault)

---

## 1. Project Overview & Motivation

AI agents today can write code, generate 3D assets, and solve engineering challenges. However, when interfacing with clients or bounty programs, they face two critical bottlenecks:

1. **No Institutional Email Presence:** Clients and sponsors communicate via RFC-compliant email, not ephemeral terminal outputs or Discord DMs.
2. **The "Unfunded Compute" Vulnerability:** Agents risk burning GPU compute, API calls, and developer time on unvetted requests that lack locked escrow.

**`mermail-bounty-escrow`** bridges Mermail's native email identity (`agent@mermail.me`) and Agent Wallet (Solana / Base) to create an end-to-end autonomous bounty settlement loop.

The agent monitors its Mermail inbox for inbound RFPs, verifies on-chain counterparty escrow or token approval before initiating heavy compute, signs an immutable SHA-256 deliverable manifest, and dispatches a cryptographic milestone release receipt directly back to the sponsor.

---

## 2. Architecture & Transaction Flow

```
   [ Sponsor / Client ]
            |
            | 1. Sends RFP / Bounty Milestone via Email
            v
   [ Mermail Gateway ] (`agent@mermail.me`)
            |
            | 2. Fetched via Mermail MCP / Inbox CLI
            v
+-------------------------------------------------------------+
|              mermail-bounty-escrow AGENT SKILL              |
|                                                             |
|  [ Step A: RFP NLP Parsing ]                                |
|    - Extracts bounty scope, compensation, & deadline        |
|                                                             |
|  [ Step B: Agent Wallet Escrow Audit ]                      |
|    - Queries Solana / Base smart contract for locked escrow |
|    - If unfunded: automatically halts and sends SOW terms   |
|                                                             |
|  [ Step C: Cryptographic Proof of Work ]                    |
|    - Traverses build artifacts and computes SHA-256 hashes  |
|    - Produces tamper-evident DELIVERY_MANIFEST.json         |
|                                                             |
|  [ Step D: Milestone Release Dispatch ]                     |
|    - Drafts & dispatches RFC delivery receipt via Mermail   |
|    - Requests automated on-chain escrow release             |
+-------------------------------------------------------------+
            |
            | 3. Outbound Proof-of-Work Receipt + Escrow Claim
            v
   [ Client / Sponsor Inbox & Smart Contract Release ]
```

---

## 3. Key Capabilities & Features

- **Autonomous Email Triaging:** Filters noise and identifies high-value bounty opportunities and milestones in real-time.
- **Autonomous Treasury Armor:** Enforces a strict zero-unfunded-compute policy. If a client has not deposited milestone funds or signed token approvals, the agent gracefully responds with milestone terms rather than burning resources. Escrow is audited directly via public blockchain RPCs (`api.mainnet-beta.solana.com` or `mainnet.base.org`).
- **Tamper-Evident Delivery Manifests:** Traverses complex project directories (GLSL shaders, Three.js repos, compiled binaries) and generates an immutable composite root SHA-256 integrity hash proof.
- **Dual Runtime Support:** Operates seamlessly with live `mermail-mcp`, direct Python FastMCP, and local CLI environments with dynamic wallet configuration (`--wallet`, `AGENT_WALLET_ADDRESS`).

---

## 4. Live 5-Minute Demo Walkthrough

### Prerequisites
- Python 3.10+ installed
- Zero paid API keys required for on-chain RPC auditing

### Step 1: Clone or Navigate to Skill Directory
```bash
cd skills/mermail-bounty-escrow
```

### Step 2: Run the Full End-to-End Demonstration
```bash
python mermail_bounty_escrow.py --action demo
```

### Terminal Output Preview:
```text
================================================================================
  MERMAIL BOUNTY ESCROW // AUTONOMOUS AGENT SETTLEMENT ENGINE
  Protocol: Mermail Email Gateway + Dynamic Agent Wallet + On-chain RPC Escrow
================================================================================

>>> STEP 1: SCAN INCOMING BOUNTY RFPs VIA MERMAIL
[+] Scanning Mermail Agent Inbox: agent@mermail.me ...
[+] Retrieved inbound bounty & deal messages.
--------------------------------------------------------------------------------
Message #1 | ID: MSG-9042 | [ESCROW FUNDED CANDIDATE]
From:    bounties@superteam.fun
Subject: AWARD NOTICE: Superteam Earn - Build and Demo a Mermail Agent Skill
Reward:  $500.00 USDC
--------------------------------------------------------------------------------

>>> STEP 2: VERIFY SUPERTEAM EARN BOUNTY ESCROW VIA ON-CHAIN RPC
[+] Verifying Counterparty Escrow for Deal: MSG-9042
[*] Escrow Address: EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
[*] Querying Solana Public RPC (getTokenAccountBalance)...
[OK] On-chain Escrow Verified: 500.00 USDC locked.
[OK] Agent Execution Approved: Proceeding with deliverable compilation.

>>> STEP 3: COMPILE TAMPER-EVIDENT MILESTONE MANIFEST
[+] Compiling Immutable Milestone Deliverable Manifest
[OK] Manifest generated: 10 files verified.
[OK] Saved receipt manifest to: skills/mermail-bounty-escrow/DELIVERY_MANIFEST.json

>>> STEP 4: DISPATCH MERMAIL DELIVERY & ESCROW RELEASE NOTICE
[+] Composing Delivery Email for Mermail Gateway
[OK] Email accepted by Mermail Gateway: status=queued, id=msg_01J...
[OK] 5-second undo grace window active until: 2026-09-18T03:45:00Z

[✔] COMPLETE AUTONOMOUS CYCLE EXECUTED WITH ZERO RUNTIME ERRORS.
```

---

## 5. Granular CLI Commands

You can also run each stage independently:

```bash
# 1. Scan inbox for bounties (Live or Simulation)
python mermail_bounty_escrow.py --action scan --live

# 2. Verify escrow on a deal via public blockchain RPC
python mermail_bounty_escrow.py --action verify --deal-id MSG-9042 --amount 500 --escrow-address EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v --chain solana

# 3. Generate tamper-evident deliverable hash manifest
python mermail_bounty_escrow.py --action deliver --target-dir . --deal-id SUPERTEAM-MERMAIL-SKILL-500

# 4. Dispatch milestone completion email
python mermail_bounty_escrow.py --action dispatch --deal-id SUPERTEAM-MERMAIL-SKILL-500 --recipient bounties@superteam.fun --live
```

---

## 6. Official Superteam Submission Checklist

- **Skill Specification:** [`SKILL.md`](file:///skills/mermail-bounty-escrow/SKILL.md) (Standard Mermail skill format with `metadata.openclaw`, `references/tools.md`, `references/workflows.md`, and `references/security.md`)
- **Target Repository:** [Nudgen-Marketing/mermail-skills](https://github.com/Nudgen-Marketing/mermail-skills)
- **AI Client Used:** Gemini Pro / Antigravity Agent Runtime + FastMCP
- **Demo Command:** `python mermail_bounty_escrow.py --action demo --target-dir .`
- **Verification Hash:** [`DELIVERY_MANIFEST.json`](file:///skills/mermail-bounty-escrow/DELIVERY_MANIFEST.json) (Composite Root: `c2933f495d1ed9f7d26cc430b7f7cfbe05659c65be6f36a6c99d3a52df5ced16`)
- **Creator / Architect:** Apoorv A S ([@apoorv_xs](https://x.com/apoorv_xs))
- **Settlement Wallet:** Dynamic (Configured via `--wallet` or `AGENT_WALLET_ADDRESS`)


