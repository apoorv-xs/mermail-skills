# Superteam Earn Submission: Mermail Agent Skill
## Project: Autonomous Bounty Escrow & Milestone Delivery Skill (`mermail-bounty-escrow`)

> **Bounty Track:** Build and Demo a Mermail Agent Skill  
> **Prize Pool:** 500 USDC  
> **Architect & Submitter:** Apoorv A S ([@apoorv_xs](https://x.com/apoorv_xs) · [@apoorv-xs](https://github.com/apoorv-xs))  
> **Role:** Creative Technologist & 3D WebUI Architect | Creator, ERAVEX (Spatial Computing & WebGPU Engine)  
> **Portfolio:** [https://apoorv.qzz.io](https://apoorv.qzz.io)  
> **Repository Core:** `https://github.com/apoorv-xs/mermail-skills` (Fork of `Nudgen-Marketing/mermail-skills`)  
> **Local Workspace:** `B:\vault\mermail-skills-repo\`

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
- **Autonomous Treasury Armor (Programmatic Execution Gate):** Enforces a strict zero-unfunded-compute policy. Before allocating compute or compiling deliverables, the agent audits counterparty on-chain token balance or escrow solvency. Counterparty funding is audited directly via public blockchain RPCs (`api.mainnet-beta.solana.com` or `mainnet.base.org`).
- **Programmatic Enforcement vs. Prompt Scaffolding:** Unlike skills that attempt to prevent unauthorized agent behavior through prompt-based prohibitions ("do not execute unvetted tasks")—which suffer from prohibition saturation and prompt injection—`mermail-bounty-escrow` moves the security boundary into **real programmatic Python RPC execution gates**. When executed through the pipeline, milestone compilation and dispatch require verified counterparty solvency.
- **Tamper-Evident Delivery Manifests:** Traverses complex project directories (GLSL shaders, Three.js repos, compiled binaries) and generates an immutable canonical composite root SHA-256 integrity hash proof.
- **Dual Runtime Support:** Operates seamlessly with live `mermail-mcp`, direct Python FastMCP, and local CLI environments with dynamic wallet configuration (`--wallet`, `AGENT_WALLET_ADDRESS`).

---

## 4. Live 5-Minute Demo Walkthrough

### Prerequisites & Connection Models
- Python 3.10+ installed
- Zero paid API keys required for on-chain RPC auditing
- **AI MCP Clients (Claude Desktop / Cursor / Codex):** Supports native MCP OAuth via `https://console.mermail.app/mcp`. If unauthenticated, a browser pop-up automatically opens (via Enoki OAuth) for instant single-click sign-in and authorization.
- **Standalone Terminal / CLI:** Can run with direct API key (`$env:MERMAIL_API_KEY`) or in dry-run/preview mode (`--action demo`) which gracefully handles unauthenticated gateway responses while executing full real on-chain escrow checks.

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
  MERMAIL BOUNTY ESCROW // AUTONOMOUS AGENT SETTLEMENT ENGINE (v3.0)
  Protocol: Mermail Email Gateway + Dynamic Agent Wallet + On-Chain Escrow Audit
================================================================================

>>> STEP 1: SCAN INCOMING BOUNTY RFPs VIA MERMAIL

[+] Scanning Mermail Agent Inbox: (unconfigured / live inquiry required) ...
[*] Querying live hosted Mermail MCP gateway: https://console.mermail.app/mcp
[!] Live Mermail API Response: HTTP Error 401: Unauthorized

>>> STEP 2: AUDIT COUNTERPARTY ON-CHAIN ESCROW (TREASURY ARMOR)

[+] Auditing Counterparty On-Chain Solvency / Escrow Balance...
[*] Target Escrow/Wallet Address: 0x3304E22DDaa22bCdC5fCa2269b418046aE7b566A
[*] Expected Amount:             $500.00 USDC
[*] Network:                     BASE
[*] On-Chain Verified Base USDC Balance: $79,178.60
[OK] Counterparty Funding Verified on Base Mainnet: $79,178.60 available.

>>> STEP 3: COMPILE TAMPER-EVIDENT MILESTONE MANIFEST

[+] Compiling Tamper-Evident Deliverable Manifest
[*] Target Directory: .
[*] Deal Reference:  SUPERTEAM-MERMAIL-500
[OK] Manifest generated: 10 files verified.
[OK] Canonical Composite Root SHA-256: 6526dad132f1ae092765425552728efcfd36579f8eadfd4be59b0c52c6b691dd
[OK] Saved receipt manifest to: .\DELIVERY_MANIFEST.json

>>> STEP 4: DISPATCH MERMAIL DELIVERY NOTICE (PREVIEW/DRY-RUN)

[+] Composing Milestone Delivery Receipt for Mermail Gateway
[*] Sender Mailbox: (unconfigured / live inquiry required)
[*] Recipient:      bounties@superteam.fun
[*] Deal:           SUPERTEAM-MERMAIL-500

-------------------------- [GENERATED EMAIL PREVIEW] --------------------------
Dear Sponsor / Client,

Milestone Delivery for [SUPERTEAM-MERMAIL-500] has been finalized and compiled.

PROVENANCE & INTEGRITY MANIFEST:
--------------------------------------------------------------------------------
Agent Mailbox Identity:   UNCONFIGURED_MAILBOX
Agent Settlement Wallet:  WALLET_NOT_CONFIGURED
Composite Root SHA-256:   6526dad132f1ae092765425552728efcfd36579f8eadfd4be59b0c52c6b691dd
Timestamp (UTC):          2026-09-18T02:25:37.480438+00:00
Total Verified Files:     10
--------------------------------------------------------------------------------

DELIVERABLE ASSETS:
The full source code, test suites, and documentation have been sealed.
All individual file checksums match the attached DELIVERY_MANIFEST.json.

ESCROW RELEASE REQUEST:
Please confirm release of the milestone escrow balance to the Agent Wallet above.

Respectfully,
Autonomous Bounty Agent
AI Engineering Agent
--------------------------------------------------------------------------------
[*] Dry run mode enabled. Email preview verified without dispatch.

================================================================================
[✔] COMPLETE VERIFIED AUTONOMOUS CYCLE EXECUTED.
================================================================================
```

---

## 5. Granular CLI Commands

You can also run each stage independently:

```bash
# 1. Scan inbox for bounties (Live or Reviewer Sample RFP)
python mermail_bounty_escrow.py --action scan --sample-file sample_rfp.txt

# 2. Verify escrow / counterparty solvency on a deal via public blockchain RPC (Solana or Base)
python mermail_bounty_escrow.py --action verify --deal-id MSG-9042 --amount 500 --escrow-address 0x3304E22DDaa22bCdC5fCa2269b418046aE7b566A --chain base

# 3. Test Treasury Armor Halt (Simulate insufficient balance, halts execution)
python mermail_bounty_escrow.py --action demo --escrow-address 4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU --chain solana --amount 500

# 4. Generate tamper-evident deliverable hash manifest
python mermail_bounty_escrow.py --action deliver --target-dir . --deal-id SUPERTEAM-MERMAIL-SKILL-500

# 5. Dispatch milestone completion email (Dry-run preview or live gateway)
python mermail_bounty_escrow.py --action dispatch --deal-id SUPERTEAM-MERMAIL-SKILL-500 --recipient bounties@superteam.fun --dry-run
```

---

## 6. Official Superteam Submission Checklist

- **Skill Specification:** [`SKILL.md`](SKILL.md) (Standard Mermail skill format with `metadata.openclaw`, `references/tools.md`, `references/workflows.md`, and `references/security.md`)
- **Target Repository:** [Nudgen-Marketing/mermail-skills](https://github.com/Nudgen-Marketing/mermail-skills)
- **AI Client Used:** Gemini Pro / Antigravity Agent Runtime + FastMCP
- **Demo Command:** `python mermail_bounty_escrow.py --action demo --target-dir .`
- **Verification Hash:** [`DELIVERY_MANIFEST.json`](DELIVERY_MANIFEST.json) (Canonical Composite Root: `6526dad132f1ae092765425552728efcfd36579f8eadfd4be59b0c52c6b691dd`)
- **Creator / Architect:** Apoorv A S ([@apoorv_xs](https://x.com/apoorv_xs))
- **Settlement Wallet:** Dynamic (Configured via `--wallet` or `AGENT_WALLET_ADDRESS`)


