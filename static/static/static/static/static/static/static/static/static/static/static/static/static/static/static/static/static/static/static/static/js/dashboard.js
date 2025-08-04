document.addEventListener("DOMContentLoaded", function () {
  const categorySelector = document.getElementById("categorySelector");
  const sections = {
    note: document.getElementById("noteInput"),
    shop_order: document.getElementById("shopOrderSection"),
    customer: document.getElementById("customerSection"),
    customer_order: document.getElementById("customerOrderSection"),
  };

  function hideAllSections() {
    Object.values(sections).forEach(el => {
      if (el) el.style.display = "none";
    });
  }

  categorySelector.addEventListener("change", function () {
    hideAllSections();
    const selected = categorySelector.value;
    if (sections[selected]) {
      sections[selected].style.display = "block";
    }
  });

  // Initialize correct display on load
  hideAllSections();
  sections["note"].style.display = "block";
});
