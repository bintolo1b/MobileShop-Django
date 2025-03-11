document.querySelector("form").onsubmit = async function (e) {
    e.preventDefault(); 

    const username = document.querySelector(".username").value;
    const password = document.querySelector(".password").value;
    const confirm_password = document.querySelector(".confirm_password").value;
    const firstname = document.querySelector(".firstname").value;
    const lastname = document.querySelector(".lastname").value;
    const email = document.querySelector(".email").value;
    const phone = document.querySelector(".phone").value;
    const address = document.querySelector(".address").value;

    // Lấy CSRF token từ cookie
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

    // Kiểm tra xác nhận mật khẩu
    if (password !== confirm_password) {
        alert("❌ Mật khẩu xác nhận không khớp!");
        return;
    }

    // Gửi yêu cầu đăng ký
    fetch("/users/logup/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ 
            username, password, confirm_password, firstname, lastname, email, phone, address 
        }),
        credentials: "include"
    })
    .then(response => response.json().then(data => {
        if (response.ok) {
            alert("✅ Đăng ký thành công! Hãy đăng nhập.");
            window.location.href = "/login"; // Chuyển hướng đến trang đăng nhập
        } else {
            alert(`❌ Lỗi ${response.status}: ${data.message || "Unknown error"}`);
        }
    }))
    .catch(error => {
        console.error("🚨 Lỗi mạng:", error);
    });
};
