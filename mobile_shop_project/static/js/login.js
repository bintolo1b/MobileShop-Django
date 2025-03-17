document.querySelector("form").onsubmit = async function (e) {
    e.preventDefault(); 
  
    const username = document.querySelector('input[name="username"]').value;
    const password = document.querySelector('input[name="password"]').value;

    // Lấy CSRF token từ input hidden trong form
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
    

    fetch("/users/login/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ username, password }),
        credentials: "include"
    })
    .then(response => response.json().then(data => {
        if (response.ok) {
            window.location.href = '/'; 
        } else {
            alert(`❌ Lỗi ${response.status}: ${data.message || "Unknown error"}`);
        }
    }))
    .catch(error => {
        console.error("🚨 Lỗi mạng:", error);
    });
}
    