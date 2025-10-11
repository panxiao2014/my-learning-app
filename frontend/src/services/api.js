export async function getPingApi() {
    const res = await fetch("/api/ping");
    if (!res.ok) {
      throw new Error("Network error");
    }
    return res.json();
  }

export async function addUserApi({ name, gender, age }) {
  const res = await fetch("/api/addUser", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, gender, age }),
  });
  if (!res.ok) {
    throw new Error("Failed to add user");
  }
  return res.json();
}

export async function getRandomUserApi() {
  const res = await fetch("/api/randomUser");
  if (!res.ok) {
    throw new Error("Failed to fetch random user");
  }
  return res.json();
}