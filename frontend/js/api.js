// Relative URL — works because Flask serves both frontend and API from the same server
const BASE_URL = "/api";

const api = {
  get: async (path) => {
    try {
      const res = await fetch(`${BASE_URL}${path}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    } catch (e) {
      console.error("GET error:", path, e);
      return { error: "Could not connect to server. Make sure the backend is running on port 5000." };
    }
  },
  post: async (path, body) => {
    try {
      const res = await fetch(`${BASE_URL}${path}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    } catch (e) {
      console.error("POST error:", path, e);
      return { error: "Could not connect to server. Make sure the backend is running on port 5000." };
    }
  },
};

// Highlight active nav link
document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll("nav ul a");
  links.forEach((link) => {
    if (link.href === location.href) link.classList.add("active");
  });
});
