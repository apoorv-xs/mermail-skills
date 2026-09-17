# Bounty escrow workflows

Read this reference for the autonomous bounty triage, on-chain RPC escrow verification, manifest compilation, and delivery dispatch sequences.

## 1. Scan and parse inbound RFPs

1. Resolve active mailbox with `list_mailboxes` and inspect public ID.
2. Ingest unread emails via `list_emails` or `search_emails`.
3. Require `scan_status: clean` before inspecting message body.
4. Extract deal ID, token, reward amount, and escrow/contract address.
5. Classify the deal as funded candidate or unconfirmed lead.

## 2. On-chain escrow audit (Treasury Armor)

1. Execute on-chain escrow verification via workspace CLI (`python mermail_bounty_escrow.py --action verify`) or companion MCP tool:
   - Provide `deal_id`, `expected_amount`, `escrow_address`, and `chain` (`solana` or `base`).
2. The engine executes a live JSON-RPC request to the public blockchain network:
   - Solana: `getTokenAccountBalance` (or `getBalance`) via `https://api.mainnet-beta.solana.com`.
   - Base: ERC-20 `balanceOf` via `https://mainnet.base.org`.
3. If confirmed on-chain, grant execution approval (`action: PROCEED_WITH_EXECUTION`).
4. If unconfirmed, insufficient balance, or missing escrow, trigger Treasury Armor halt:
   - Halt all build and code generation immediately.
   - Compose standard 50% upfront milestone SOW link via `save_draft` or queue via `send_email`.

## 3. Tamper-evident deliverable manifest compilation

1. Recursively traverse production deliverable directory via `action_deliver` (`python mermail_bounty_escrow.py --action deliver`).
2. Compute individual SHA-256 integrity checksums for every source file, asset, and script (excluding self-manifest files).
3. Compute deterministic composite root hash across all file hashes.
4. Write `DELIVERY_MANIFEST.json` with timestamp, dynamic agent settlement wallet address, and file tree.

## 4. Milestone delivery dispatch

1. Preview delivery email payload: sender mailbox, recipient, subject, composite root hash, and settlement wallet.
2. Draft first with `save_draft` when review is needed, or queue delivery notice via `send_email`.
3. Record returned gateway message status (`status: queued`), message ID, and `undo_until` cancellation window.
4. Monitor for counterparty escrow release.

## 5. Recovery from failure

- `400 / validation_failed`: Correct nested argument structure (ensure `body.from` and `body.text` are populated).
- `401 / 403`: Verify `MERMAIL_API_KEY` or refresh MCP session.
- `402`: Check Mermail credit balance for outbound dispatch.
- `Escrow Mismatch / Insufficient Balance`: Halt build immediately and notify sponsor via email of shortfall.

