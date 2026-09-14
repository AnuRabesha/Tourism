const BASE_URL = "/api";

const api = {
  get: async (path) => {
    try {
      const res = await fetch(`${BASE_URL}${path}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    } catch (e) {
      console.error("GET error:", path, e);
      return { error: "Could not connect to server." };
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
      return { error: "Could not connect to server." };
    }
  },
};

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("nav ul a").forEach((link) => {
    if (link.href === location.href) link.classList.add("active");
  });
});
