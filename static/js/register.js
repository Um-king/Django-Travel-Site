document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll("[data-switch]").forEach((item) => {
    item.addEventListener("click", function (e) {
      e.preventDefault();
      const rightContent = document.querySelector("#right-content");
      rightContent.classList.add("slide-out");

      setTimeout(() => {
        window.location.href = this.getAttribute("href");
      }, 600);
    });
  });
});


