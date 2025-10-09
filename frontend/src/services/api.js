export async function getPingApi() {
    const res = await fetch("/api/ping");
    if (!res.ok) {
      throw new Error("Network error");
    }
    return res.json();
  }