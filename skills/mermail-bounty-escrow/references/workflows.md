# Mermail Bounty Escrow Workflows

## Standard 4-Stage Autonomous Settlement Flow

```mermaid
sequenceDiagram
    autonumber
    actor Client as Bounty Sponsor / Client
    participant Mermail as Mermail Gateway (agent@mermail.me)
    participant Agent as Autonomous Bounty Escrow Agent
    participant Escrow as On-Chain Escrow (Solana / Base)
    participant Artifacts as Build & Deliverable Manifest

    Client->>Mermail: Sends Bounty Milestone / RFP Email
    Mermail->>Agent: Fetched via mermail_fetch_inbox()
    Agent->>Escrow: Audits lock via mermail_verify_escrow()
    alt Escrow Verified (500 USDC locked)
        Agent->>Artifacts: Compiles & hashes assets (DELIVERY_MANIFEST.json)
        Agent->>Mermail: Dispatches receipt via mermail_send_email()
        Mermail->>Client: Email Delivered with Root SHA-256 Proof
        Client->>Escrow: Releases escrow to Agent Wallet
    else Escrow Missing / Unfunded
        Agent->>Mermail: Dispatches SOW 50% Deposit Notice
        Mermail->>Client: Requires upfront milestone before compute
    end
```

## CLI Usage

### Stage 1: Inbound Discovery
```bash
python mermail_bounty_escrow.py --action scan --live
```

### Stage 2: Escrow Verification
```bash
python mermail_bounty_escrow.py --action verify --deal-id MSG-9042 --amount 500.0
```

### Stage 3: Seal Deliverables
```bash
python mermail_bounty_escrow.py --action deliver --target-dir . --deal-id MSG-9042
```

### Stage 4: Dispatch Proof of Work
```bash
python mermail_bounty_escrow.py --action dispatch --deal-id MSG-9042 --recipient bounties@superteam.fun --live
```
