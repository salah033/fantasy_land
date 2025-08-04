function selectCategory(value, element) {
    document.getElementById("categoryInput").value = value;

    // remove 'selected' class from all
    document.querySelectorAll(".card-option").forEach(el => el.classList.remove("selected"));
    element.classList.add("selected");

    // hide all sections
    document.querySelectorAll(".note-section").forEach(sec => sec.style.display = "none");

    // show selected section
    if (value === "note") document.getElementById("noteSection").style.display = "block";
    else if (value === "shop_order") document.getElementById("shopOrderSection").style.display = "block";
    else if (value === "customer") document.getElementById("customerSection").style.display = "block";
    else if (value === "customer_order") document.getElementById("customerOrderSection").style.display = "block";
}