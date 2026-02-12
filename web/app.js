const buttons = document.querySelectorAll("button");

buttons.forEach((btn) => {
  btn.addEventListener("click", () => {
    btn.classList.add("clicked");
    setTimeout(() => btn.classList.remove("clicked"), 300);
  });
});
