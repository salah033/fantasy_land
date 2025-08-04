function selectCategory_show(category, element) {
    // Set input value
    const input = document.getElementById("categoryInput_show");
    if (input) input.value = category;

    // Add "selected" class to clicked card
    document.querySelectorAll(".card-option").forEach(card => card.classList.remove("selected"));
    element.classList.add("selected");

    // Hide all sections
    document.querySelectorAll(".memo-section").forEach(sec => sec.style.display = "none");

    // Show selected section
    const section = document.getElementById(category);
    if (section) section.style.display = "block";

    // Send POST to Django without reload
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch("/accounts/show_memo/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `category=${category}`
    })
    .then(response => {
        if (!response.ok) {
            console.error("Failed to post category.");
        }
    })
    .catch(err => console.error("Fetch error:", err));
}

// On load: show "notes" by default
document.addEventListener("DOMContentLoaded", function () {
    const defaultCard = document.querySelector('.card-option');
    if (defaultCard) {
        selectCategory_show('notes', defaultCard);
    }
});
