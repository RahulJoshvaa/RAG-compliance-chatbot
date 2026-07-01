// Thin client for the generation backend.
// Requests go to /api/* and are proxied to the Flask server (see vite.config.js).

export async function sendChat(query, mode) {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, mode }),
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.error || `Request failed (${res.status})`);
  }

  return data;
}

export async function getHealth() {
  try {
    const res = await fetch("/api/health");
    return await res.json();
  } catch {
    return { live: false, error: "backend unreachable" };
  }
}
