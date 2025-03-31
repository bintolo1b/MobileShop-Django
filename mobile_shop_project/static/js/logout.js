document.querySelector("#logoutButton").onclick = async function () {
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith("csrftoken=")) {
                    cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                    break;
                }
            }
        }
        return cookieValue;
    }

    fetch("/users/logout/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        credentials: "include"
    })
    .then(response => response.json().then(data => {
        if (response.ok) {
            window.location.href = "/login"; // Chuyển về trang login
        } else {
            alert(`❌ Lỗi ${response.status}: ${data.message || "Unknown error"}`);
        }
    }))
    .catch(error => {
        console.error("🚨 Lỗi mạng:", error);
    });
};
