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
    const existingError = document.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
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
            if (data.role == 'staff')
                window.location.href = '/users/staff'; 
            else if (data.role == 'client')
                window.location.href = '/'; 
        } else {
            // Hiển thị thông báo lỗi
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = "Tên đăng nhập hoặc mật khẩu không chính xác";
            document.querySelector('.login-box').insertBefore(errorDiv, document.querySelector('form'));
        }
    }))
    .catch(error => {
        console.error("🚨 Lỗi mạng:", error);
        // Hiển thị thông báo lỗi kết nối
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = "Lỗi kết nối, vui lòng thử lại sau";
        document.querySelector('.login-box').insertBefore(errorDiv, document.querySelector('form'));
    });
}
    