document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("div[class*='language-']").forEach((block) => {
    const languageClass = [...block.classList].find((className) =>
      className.startsWith("language-")
    );

    if (!languageClass) return;

    const language = languageClass
      .replace("language-", "")
      .toLowerCase();

    if (!["bash", "sh", "shell", "python", "py", "yaml", "m"].includes(language)) {
      return;
    }

    const pre = block.querySelector("pre");
    const code = block.querySelector("pre > code");

    if (!pre || !code) return;
    if (pre.querySelector(".copy-code-button")) return;

    const button = document.createElement("button");
    button.type = "button";
    button.className = "copy-code-button";
    button.setAttribute("aria-label", "Copy");

    // Overlapping-squares copy icon

    button.innerHTML = `
      <svg
        viewBox="0 0 24 24"
        aria-hidden="true"
        focusable="false"
      >
        <rect x="9" y="9" width="9" height="9" rx="2"></rect>
        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
      </svg>
      <span class="copy-code-tooltip">Copy</span>
    `;


    button.addEventListener("click", async () => {
      try {
        const text = code.textContent.replace(/\n$/, "");

        await navigator.clipboard.writeText(text);

        button.classList.add("copied");
        button.setAttribute("aria-label", "Copied!");

        const tooltip = button.querySelector(".copy-code-tooltip");
        tooltip.textContent = "Copied!";

        setTimeout(() => {
          button.classList.remove("copied");
          button.setAttribute("aria-label", "Copy code");
          tooltip.textContent = "Copy";
        }, 1500);

      } catch (error) {
        console.error("Failed to copy code:", error);

        const tooltip = button.querySelector(".copy-code-tooltip");
        tooltip.textContent = "Failed";

        setTimeout(() => {
          tooltip.textContent = "Copy";
        }, 1500);
      }
    });

    pre.appendChild(button);
  });
});