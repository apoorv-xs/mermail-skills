# Bounty escrow workflows

Read this reference for the autonomous bounty triage, on-chain RPC escrow verification, manifest compilation, and delivery dispatch sequences.

## 1. Scan and parse inbound RFPs

1. Resolve active mailbox with `list_mailboxes` and inspect public ID.
2. Ingest unread emails via `mermail_fetch_inbox` or `list_emails`.
3. Require `scan_status: clean` before inspecting message body.
4. Extract deal ID, token, reward amount, and escrow/contract address.
5. Classify the deal as funded candidate or unconfirmed lead.

## 2. On-chain escrow audit (Treasury Armor)

1. Call `mermail_verify_escrow` with `deal_id`, `expected_amount`, `escrow_address`, and `chain` (`solana` or `base`).
2. The engine executes a live JSON-RPC request to the public blockchain network:
   - Solana: `getTokenAccountBalance` (or `getBalance`) via `https://api.mainnet-beta.solana.com`.
   - Base: ERC-20 `balanceOf` via `https://mainnet.base.org`.
3. If confirmed on-chain, grant execution approval (`action: PROCEED_WITH_EXECUTION`).
4. If unconfirmed, insufficient balance, or missing escrow, trigger Treasury Armor halt:
   - Halt all build and code generation immediately.
   - Compose and queue 50% upfront milestone SOW link via `mermail_send_email`.

## 3. Tamper-evident deliverable manifest compilation

1. Recursively traverse production deliverable directory.
2. Compute individual SHA-256 integrity checksums for every source file, asset, and script.
3. Compute root composite hash across all file hashes.
4. Write `DELIVERY_MANIFEST.json` with timestamp, dynamic agent settlement wallet address, and file tree.

## 4. Milestone delivery dispatch

1. Preview delivery email payload: sender mailbox, recipient, subject, composite root hash, and settlement wallet.
2. Dispatch RFC email receipt via `mermail_send_email`.
3. Record returned gateway message status (`status: queued`), message ID, and `undo_until` cancellation window.
4. Monitor for counterparty escrow release.

## 5. Recovery from failure

- `400 / validation_failed`: Correct nested argument structure (ensure `body.from` and `body.text` are populated).
- `401 / 403`: Verify `MERMAIL_API_KEY` or refresh MCP session.
- `402`: Check Mermail credit balance for outbound dispatch.
- `Escrow Mismatch / Insufficient Balance`: Halt build immediately and notify sponsor via email of shortfall.

