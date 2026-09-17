# Bounty escrow tool contracts

This workflow uses FastMCP tools for counterparty escrow verification, deliverable sealing, and milestone delivery receipt composition. It composes existing Mermail tools and FastMCP gates.

Pass structured arguments as **native JSON objects**. Never stringify `query` or `body`. Prefer mailbox `public_id` as `mailboxId`.

## Intent to Real Operation Map

| Intent | Real operation | Surface | Description |
| :--- | :--- | :--- | :--- |
| Discover ready mailbox | `list_mailboxes` | Hosted Mermail MCP | Discovers active agent mailbox |
| Inspect settlement wallet | `mermail_get_wallet` | FastMCP | Queries agent public address and supported tokens |
| Read inbound RFPs | `list_emails` / `mermail_fetch_inbox` | Hosted Mermail MCP / FastMCP | Ingests unread bounty announcements and milestone RFPs |
| Verify counterparty escrow | `mermail_verify_escrow` | FastMCP | Queries on-chain smart contract for locked milestone funds |
| Compile proof-of-work | `action_deliver` | Local FastMCP Engine | Hashes project deliverables and writes `DELIVERY_MANIFEST.json` |
| Dispatch delivery receipt | `send_email` / `mermail_send_email` | Hosted Mermail MCP / FastMCP | Sends cryptographic delivery receipt via Mermail gateway |

---

## Native FastMCP Payload Shapes

### `mermail_get_wallet`
Returns the active agent settlement wallet and network:
```json
{}
```
Response:
```json
{
  "status": "connected",
  "chain": "Solana SPL",
  "wallet_address": "2PjfGyk1PcnXPj26BpaE4BicdbR5uGce9ULV7NMKpac9",
  "token_supported": ["USDC", "SOL"]
}
```

### `mermail_fetch_inbox`
Queries unread emails from the Mermail gateway:
```json
{
  "query": "bounty",
  "limit": 5,
  "live": true
}
```

### `mermail_verify_escrow`
Audits on-chain counterparty contract locks prior to burning compute:
```json
{
  "deal_id": "MSG-9042",
  "expected_amount": 500.0
}
```
Response:
```json
{
  "deal_id": "MSG-9042",
  "verified": true,
  "locked_amount_usdc": 500.0,
  "contract": "0x94B0...e81A",
  "action": "PROCEED_WITH_EXECUTION"
}
```

### `mermail_send_email`
Dispatches RFC delivery receipts via Mermail gateway:
```json
{
  "mailboxId": "e2e20080-a406-478b-a2e5-28f9b2d6bf17",
  "body": {
    "from": "ricksanchez@mermail.app",
    "to": "bounties@superteam.fun",
    "subject": "MILESTONE DELIVERED // SUPERTEAM-500",
    "text": "Dear Sponsor,\n\nMilestone delivery has been sealed with Root SHA-256: 235e0309...\nPlease release the escrow balance to 2PjfGyk1PcnXPj26BpaE4BicdbR5uGce9ULV7NMKpac9."
  }
}
```
