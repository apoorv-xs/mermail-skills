# Bounty escrow workflows

Read this reference for the autonomous bounty triage, on-chain escrow verification, manifest compilation, and delivery dispatch sequences.

## 1. Scan and parse inbound RFPs

1. Resolve active mailbox with `list_mailboxes` and inspect public ID.
2. Ingest unread emails via `mermail_fetch_inbox` or `list_emails`.
3. Require `scan_status: clean` before inspecting message body.
4. Extract deal ID, token, reward amount, and contract address via regex.
5. Classify the deal as funded candidate or unconfirmed lead.

## 2. On-chain escrow audit (Treasury Armor)

1. Call `mermail_verify_escrow` with `deal_id` and `expected_amount`.
2. Inspect returned smart contract address (`0x94B0...e81A`) and locked USDC amount.
3. If confirmed, grant execution approval (`action: PROCEED_WITH_EXECUTION`).
4. If unconfirmed or missing, trigger Treasury Armor halt:
   - Halt all build and code generation.
   - Compose and send 50% upfront milestone SOW link via `send_email`.

## 3. Cryptographic proof-of-work compilation

1. Recursively traverse production deliverable directory.
2. Compute individual SHA-256 signatures for every source file, asset, and script.
3. Compute root composite hash across the file manifests.
4. Write `DELIVERY_MANIFEST.json` with timestamp, agent wallet address, and file tree.

## 4. Milestone delivery dispatch

1. Preview delivery email payload: sender mailbox, recipient, subject, root hash, and settlement wallet.
2. Dispatch RFC email receipt via `send_email` or `mermail_send_email`.
3. Record returned delivery ID (`a7fef9b4-...`) and transmission timestamp.
4. Verify on-chain escrow release once confirmed by sponsor.

## 5. Recovery from failure

- `400 / validation_failed`: Correct nested argument structure (ensure `body.from` and `body.text` are populated).
- `401 / 403`: Verify `MERMAIL_API_KEY` or refresh MCP OAuth session.
- `402`: Check Mermail credit balance for outbound dispatch.
- `Escrow Mismatch`: Halt build immediately and notify sponsor via email of shortfall.
