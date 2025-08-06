document.addEventListener('DOMContentLoaded', function() {
  const toggleButton = document.getElementById("theme-toggle");
  const body = document.body;

  function updateThemeIcon() {
    if (body.classList.contains("dark-mode")) {
      toggleButton.textContent = "☀️"; // Sun for switching to light
    } else {
      toggleButton.textContent = "🌙"; // Moon for switching to dark
    }
  }

  // Load preference on page load
  if (localStorage.getItem("theme") === "dark") {
    body.classList.add("dark-mode");
  }
  updateThemeIcon();

  // Toggle handler
  toggleButton?.addEventListener("click", () => {
    body.classList.toggle("dark-mode");

    // Save preference
    if (body.classList.contains("dark-mode")) {
      localStorage.setItem("theme", "dark");
    } else {
      localStorage.setItem("theme", "light");
    }

    updateThemeIcon();
  });
});