// Talks to the Kibbly AI server (ai_v2). In the demo the server runs on the owner's laptop,
// so the address is editable and kept per browser. See docs/esp32_server_protocol.md.

const URL_KEY = "kibbly_server_url";
export const DEFAULT_SERVER = "http://localhost:8000";

export function getServerUrl() {
  try {
    return localStorage.getItem(URL_KEY) || DEFAULT_SERVER;
  } catch {
    return DEFAULT_SERVER;
  }
}

export function setServerUrl(url) {
  try {
    localStorage.setItem(URL_KEY, url);
  } catch {
    // A private window may block storage; the address just will not be remembered.
  }
}

function base() {
  return getServerUrl().replace(/\/+$/, "");
}

// Ask Kibbly about one dog, non streaming. Throws on a network or server error.
export async function askKibbly({ dog, question, facts }) {
  const response = await fetch(`${base()}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, dog, facts }),
  });
  if (!response.ok) {
    throw new Error(`The Kibbly server answered ${response.status}.`);
  }
  return response.json();
}

// Stream the answer as the local model writes it, so words show within a second or two.
// Calls onChunk(textPiece) for each piece. Throws on a network or server error.
export async function streamKibbly({ dog, question, facts }, onChunk) {
  const response = await fetch(`${base()}/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, dog, facts }),
  });
  if (!response.ok || !response.body) {
    throw new Error(`The Kibbly server answered ${response.status}.`);
  }
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    const piece = decoder.decode(value, { stream: true });
    if (piece) onChunk(piece);
  }
}
