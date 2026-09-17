# Mermail Bounty Escrow Tool Contract

Read this reference when configuring or invoking FastMCP tools for the `mermail-bounty-escrow` skill.

## Native FastMCP Tools

### 1. `mermail_get_wallet`
Returns the active agent settlement wallet and supported tokens.
- **Input:** None (`{}`)
- **Response:**
  ```json
  {
    "status": "connected",
    "chain": "Solana SPL",
    "wallet_address": "2PjfGyk1PcnXPj26BpaE4BicdbR5uGce9ULV7NMKpac9",
    "token_supported": ["USDC", "SOL"]
  }
  ```

### 2. `mermail_fetch_inbox`
Scans the Mermail agent inbox for incoming RFPs and bounty award notices.
- **Input:**
  ```json
  {
    "query": "bounty",
    "limit": 5,
    "live": true
  }
  ```
- **Response:**
  ```json
  {
    "source": "LIVE_MERMAIL_GATEWAY",
    "mailbox": "ricksanchez@mermail.app",
    "count": 2,
    "inbox": [...]
  }
  ```

### 3. `mermail_verify_escrow`
Audits counterparty smart contract escrow before burning GPU or agent compute.
- **Input:**
  ```json
  {
    "deal_id": "MSG-9042",
    "expected_amount": 500.0
  }
  ```
- **Response:**
  ```json
  {
    "deal_id": "MSG-9042",
    "verified": true,
    "locked_amount_usdc": 500.0,
    "contract": "0x94B0...e81A",
    "action": "PROCEED_WITH_EXECUTION"
  }
  ```

### 4. `mermail_send_email`
Dispatches RFC delivery receipts and milestone claims through the Mermail gateway.
- **Input:**
  ```json
  {
    "to": "bounties@superteam.fun",
    "subject": "MILESTONE DELIVERED // SUPERTEAM-500",
    "body": "Cryptographic proof-of-work attached...",
    "live": true
  }
  ```
