import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";

const apiKey = process.env.MERMAIL_API_KEY;
const transport = new SSEClientTransport(new URL("https://console.mermail.app/mcp"), {
  eventSourceInit: {
    headers: { "x-api-key": apiKey }
  },
  requestInit: {
    headers: { "x-api-key": apiKey }
  }
});

const client = new Client({ name: "antigravity-mermail", version: "1.0.0" }, { capabilities: {} });
await client.connect(transport);
const res = await client.callTool({ name: "list_mailboxes", arguments: {} });
console.log("=== LIVE MERMAIL MAILBOXES ===");
console.log(JSON.stringify(res, null, 2));
await client.close();
