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
   [ Mermail Gateway ] (`apoorv@mermail.me`)
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
- **Autonomous Treasury Armor:** Enforces a strict zero-unfunded-compute policy. If a client has not deposited milestone funds or signed token approvals, the agent gracefully responds with milestone terms rather than burning resources.
- **Cryptographic Delivery Manifests:** Traverses complex project directories (GLSL shaders, Three.js repos, compiled binaries) and generates an immutable root hash proof.
- **Dual Runtime Support:** Works out of the box in zero-cost local simulation mode (for testing and local agents) and integrates seamlessly with live `mermail-mcp` and `mermail-cli` environments.

---

## 4. Live 5-Minute Demo Walkthrough

### Prerequisites
- Python 3.10+ installed
- Zero paid API keys required

### Step 1: Clone or Navigate to Skill Directory
```bash
cd B:\vault\mermail-skill\
```

### Step 2: Run the Full End-to-End Demonstration
```bash
python mermail_bounty_escrow.py --action demo
```

### Terminal Output Preview:
```text
================================================================================
  MERMAIL BOUNTY ESCROW // AUTONOMOUS AGENT SETTLEMENT ENGINE
  Protocol: Mermail Email Gateway + Agent Wallet + x402 Micro-Escrow
  Architect: Apoorv A S (@apoorv_xs) | Portfolio: https://apoorv.qzz.io
================================================================================

>>> STEP 1: SCAN INCOMING BOUNTY RFPs VIA MERMAIL
[+] Scanning Mermail Agent Inbox: apoorv@mermail.me ...
[+] Retrieved 2 inbound bounty & deal messages.
--------------------------------------------------------------------------------
Message #1 | ID: MSG-9042 | [ESCROW FUNDED]
From:    bounties@superteam.fun
Subject: AWARD NOTICE: Superteam Earn - Build and Demo a Mermail Agent Skill
Reward:  $500.00 USDC
--------------------------------------------------------------------------------

>>> STEP 2: VERIFY SUPERTEAM EARN BOUNTY ESCROW
[+] Verifying Counterparty Escrow for Deal: MSG-9042
[*] Expected Milestone Amount: $500.00 USDC
[OK] On-chain Escrow Verified: 500.00 USDC locked in contract 0x94B0...e81A
[OK] Agent Execution Approved: Proceeding with deliverable compilation.

>>> STEP 3: COMPILE CRYPTOGRAPHIC MILESTONE MANIFEST
[+] Compiling Immutable Milestone Deliverable Manifest
[OK] Manifest generated: 15 files cryptographically signed.
[OK] Saved receipt manifest to: B:\vault\mermail-skill\DELIVERY_MANIFEST.json

>>> STEP 4: DISPATCH MERMAIL DELIVERY & ESCROW RELEASE NOTICE
[+] Composing Cryptographic Delivery Email for Mermail Gateway
[OK] Email queued for instantaneous Mermail SMTP/MCP dispatch.

[✔] COMPLETE AUTONOMOUS CYCLE EXECUTED WITH ZERO RUNTIME ERRORS.
```

---

## 5. Granular CLI Commands

You can also run each stage independently:

```bash
# 1. Scan inbox for bounties (Live or Simulation)
python mermail_bounty_escrow.py --action scan --live

# 2. Verify escrow on a deal
python mermail_bounty_escrow.py --action verify --deal-id MSG-9042 --amount 500

# 3. Generate cryptographic deliverable hash manifest
python mermail_bounty_escrow.py --action deliver --target-dir . --deal-id MSG-9042

# 4. Dispatch milestone completion email
python mermail_bounty_escrow.py --action dispatch --deal-id MSG-9042 --recipient bounties@superteam.fun --live
```

---

## 6. Official Superteam Submission Checklist

- **Skill Specification:** [`SKILL.md`](file:///B:/vault/mermail-skill/SKILL.md) (Standard Mermail skill format with `metadata.openclaw`, `references/tools.md`, `references/workflows.md`, and `references/security.md`)
- **Target Repository:** [Nudgen-Marketing/mermail-skills](https://github.com/Nudgen-Marketing/mermail-skills)
- **AI Client Used:** Gemini Pro / Antigravity Agent Runtime + FastMCP
- **Demo Command:** `python mermail_bounty_escrow.py --action demo --live`
- **Verification Hash:** [`DELIVERY_MANIFEST.json`](file:///B:/vault/mermail-skill/DELIVERY_MANIFEST.json) (Composite Root: `235e030941bceb8817a32b1d34c1f07d56167c16d400381440d3ae5451d86940`)
- **Creator / Architect:** Apoorv A S ([@apoorv_xs](https://x.com/apoorv_xs))
- **Claim Wallet (Solana):** `2PjfGyk1PcnXPj26BpaE4BicdbR5uGce9ULV7NMKpac9`

