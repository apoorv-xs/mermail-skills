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

  const emailsRes = await call({
    jsonrpc: "2.0",
    id: 2,
    method: "tools/call",
    params: {
      name: "list_emails",
      arguments: {
        mailboxId: "ricksanchez@mermail.app"
      }
    }
  });
  console.log("=== LIVE EMAILS IN ricksanchez@mermail.app ===");
  console.log(JSON.stringify(emailsRes, null, 2));
}

run().catch(console.error);
