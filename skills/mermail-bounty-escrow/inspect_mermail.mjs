const endpoint = "https://console.mermail.app/mcp";
const apiKey = process.env.MERMAIL_API_KEY;

async function run() {
  async function call(body) {
    const res = await fetch(endpoint, {
      method: "POST",
      headers: {
        accept: "application/json, text/event-stream",
        "content-type": "application/json",
        "x-api-key": apiKey
      },
      body: JSON.stringify(body)
    });
    return await res.json();
  }

  // 1. Initialize
  await call({
    jsonrpc: "2.0",
    id: 1,
    method: "initialize",
    params: {
      protocolVersion: "2025-03-26",
      capabilities: {},
      clientInfo: { name: "antigravity-agent", version: "1.0.0" }
    }
  });

  // 2. Call list_workspaces
  const wsRes = await call({
    jsonrpc: "2.0",
    id: 2,
    method: "tools/call",
    params: {
      name: "list_workspaces",
      arguments: {}
    }
  });
  console.log("=== WORKSPACES ===");
  console.log(JSON.stringify(wsRes, null, 2));

  // 3. Call list_mailboxes
  const mbRes = await call({
    jsonrpc: "2.0",
    id: 3,
    method: "tools/call",
    params: {
      name: "list_mailboxes",
      arguments: {}
    }
  });
  console.log("=== MAILBOXES ===");
  console.log(JSON.stringify(mbRes, null, 2));
}

run().catch(console.error);
