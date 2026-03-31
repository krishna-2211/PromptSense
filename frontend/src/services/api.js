const API_BASE_URL = "http://127.0.0.1:8000/api";

export async function improvePrompt(payload) {
  const response = await fetch(`${API_BASE_URL}/improve`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Failed to improve prompt");
  }

  return response.json();
}
