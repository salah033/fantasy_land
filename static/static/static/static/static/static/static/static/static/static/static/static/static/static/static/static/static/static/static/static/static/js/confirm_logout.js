const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");

document.getElementById("logout-link").addEventListener("click", function(event) {
    event.preventDefault();
    document.getElementById("logout-modal").style.display = "flex";
    document.getElementById("confirm-logout").focus();
});

document.getElementById("cancel-logout").addEventListener("click", function() {
    document.getElementById("logout-modal").style.display = "none";
});

function confirmLogout() {
    fetch("/accounts/logout/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        }
    });
}

document.getElementById("confirm-logout").addEventListener("click", confirmLogout);

document.addEventListener("keydown", function(event) {
    const modal = document.getElementById("logout-modal");
    if (modal.style.display === "flex") {
        if (event.key === "Escape") {
            modal.style.display = "none";
        } else if (event.key === "Enter") {
            confirmLogout();
        }
    }
});
