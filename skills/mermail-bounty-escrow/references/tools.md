# Bounty escrow tool contracts

This persona workflow reuses tools owned by official Mermail skills (`mermail-administer-workspace`, `mermail-manage-inbox`, `mermail-compose-email`, and `mermail-agent-wallet`). It does not invent or claim new tools on the remote Mermail server.

On-chain RPC audits and deliverable manifest hashing are executed locally in the workspace via `mermail_bounty_escrow.py`, with an optional local companion FastMCP server (`mcp_server.py`) for local agent environments.

Pass structured arguments as **native JSON objects**. Never stringify `query` or `body`. Prefer mailbox `public_id` as `mailboxId`.

## Intent to Real Operation Map

| Intent | Operation | Surface / Owner | Description |
| :--- | :--- | :--- | :--- |
| Discover ready mailbox | `list_mailboxes` | `mermail-administer-workspace` | Discovers active agent mailbox |
| Inspect settlement wallet | `get_agent_wallet` | `mermail-agent-wallet` | Queries wallet portfolio and connected addresses |
| Ingest inbound RFPs | `list_emails` / `search_emails` | `mermail-manage-inbox` | Ingests unread bounty announcements and milestone RFPs |
| Read sanitized message | `get_email` / `get_email_context` | `mermail-manage-inbox` | Bounded read with `scan_status: clean` requirement |
| Audit counterparty escrow | `action_verify_escrow` | Local Engine (`--action verify`) | Queries live public Solana/Base RPC for token balance |
| Compile proof-of-work | `action_deliver` | Local Engine (`--action deliver`) | Recursively hashes deliverables and writes `DELIVERY_MANIFEST.json` |
| Draft milestone receipt | `save_draft` | `mermail-compose-email` | Saves delivery preview without sending |
| Dispatch delivery receipt | `send_email` | `mermail-compose-email` | Queues RFC delivery receipt via Mermail gateway |

---

## 1. Official Hosted Mermail MCP Payload Shapes

### `list_mailboxes`
```json
{}
```

### `list_emails`
```json
{
  "mailboxId": "e2e20080-a406-478b-a2e5-28f9b2d6bf17"
}
```

### `get_agent_wallet`
```json
{
  "mailboxId": "e2e20080-a406-478b-a2e5-28f9b2d6bf17"
}
```

### `send_email`
Queues RFC delivery receipts via Mermail gateway:
```json
{
  "mailboxId": "e2e20080-a406-478b-a2e5-28f9b2d6bf17",
  "body": {
    "from": "agent@mermail.me",
    "to": "bounties@superteam.fun",
    "subject": "MILESTONE DELIVERED // SUPERTEAM-500",
    "text": "Dear Sponsor,\n\nMilestone delivery has been sealed with Root SHA-256: 12576321...\nPlease release the escrow balance to 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU."
  }
}
```
Response:
```json
{
  "status": "queued",
  "id": "msg_01J...",
  "undo_until": "2026-09-18T04:00:00Z"
}
```

---

## 2. Local Workspace Engine Commands (`mermail_bounty_escrow.py`)

### On-chain Escrow Audit via Public RPC
```bash
python mermail_bounty_escrow.py --action verify --deal-id MSG-9042 --amount 500 --escrow-address EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v --chain solana
```

### Tamper-Evident Manifest Compilation
```bash
python mermail_bounty_escrow.py --action deliver --target-dir . --deal-id SUPERTEAM-MERMAIL-SKILL-500
```

### End-to-End Verified Autonomous Run
```bash
python mermail_bounty_escrow.py --action demo --target-dir .
```

---

## 3. Optional Local FastMCP Sidecar (`mcp_server.py`)

For local agent environments that require a unified JSON-RPC bridge, the included `mcp_server.py` sidecar exposes local FastMCP wrappers:
- `mermail_get_wallet`
- `mermail_fetch_inbox`
- `mermail_verify_escrow`
- `mermail_send_email`


