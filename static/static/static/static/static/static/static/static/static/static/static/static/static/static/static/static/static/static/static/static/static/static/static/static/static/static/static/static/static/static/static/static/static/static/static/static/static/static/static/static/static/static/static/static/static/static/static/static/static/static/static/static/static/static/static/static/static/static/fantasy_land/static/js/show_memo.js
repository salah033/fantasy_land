function selectCategory_show(category, element) {
    // UI update
    document.querySelectorAll(".card-option").forEach(card => card.classList.remove("selected"));
    element.classList.add("selected");

    // Send AJAX request
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch("/accounts/show_memo/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `category=${encodeURIComponent(category)}`
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("memo-content").innerHTML = data.html;
    })
    .catch(err => {
        console.error("Error loading memo content:", err);
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const defaultCard = document.querySelector('.card-option');
    if (defaultCard) {
        selectCategory_show('notes', defaultCard);
    }
});
