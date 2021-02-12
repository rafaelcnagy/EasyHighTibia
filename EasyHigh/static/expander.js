
function openTab(element) {
  var frags_content = element.parentNode.parentNode.querySelector(".frags-tab");
  var expand_button = element.querySelector(".expand-icon");
  if (frags_content.style.display === "none") {
    frags_content.style.display = "block";
    expand_button.style.transform = "scaleY(-1)"
  }
  else {
    frags_content.style.display = "none";
    expand_button.style.transform = "scaleY(1)"
  }
}
