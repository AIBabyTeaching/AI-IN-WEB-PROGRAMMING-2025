// Resolve the backend base URL from env during dev/prod and fall back to the
// FastAPI default when running the frontend directly via `npm run dev`.
const BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

/**
 * POST JSON to the FastAPI backend.
 *
 * @param {string} path - Relative API path such as "/echo".
 * @param {Record<string, unknown>} body - Serializable payload to send.
 * @returns {Promise<any>} Parsed JSON response from the server.
 * @throws {Error} When the HTTP response is not in the 200 range.
 */
export async function post(path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  if (!res.ok) {
    // Propagate a descriptive error so callers can surface the failure in the UI.
    let message = `HTTP ${res.status}`;
    let detail;
    const contentType = res.headers.get('content-type') || '';

    try {
      if (contentType.includes('application/json')) {
        const data = await res.json();
        detail = typeof data?.detail === 'string'
          ? data.detail
          : Array.isArray(data?.detail)
            ? data.detail.map((item) => item?.msg).filter(Boolean).join('; ')
            : undefined;
        if (!detail && typeof data?.message === 'string') {
          detail = data.message;
        }
      } else {
        const text = await res.text();
        detail = text.trim() || undefined;
      }
    } catch (parseError) {
      // Ignore body parsing errors; fall back to the default message.
    }

    if (detail) {
      message = detail;
    }

    const error = new Error(message);
    error.status = res.status;
    if (detail) {
      error.detail = detail;
    }
    throw error;
  }
  return res.json();
}
