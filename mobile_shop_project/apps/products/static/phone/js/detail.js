function changeImage(src) {
    document.getElementById('main-image').src = src;
}
document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('btn-info-ev');
    const modal = document.getElementById('modal1');
    const overlay = document.querySelector('.modal__overlay');

    button.addEventListener('click', function () {
        modal.style.display = 'flex';
    });

    overlay.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    const memoryOptions = document.querySelectorAll(".memory-container input[type='radio']");
    const colorOptions = document.querySelectorAll(".color-container input[type='radio']");
    if (memoryOptions.length > 0 && !document.querySelector(".memory-container input:checked")) {
        memoryOptions[0].checked = true;
    }
    if (colorOptions.length > 0 && !document.querySelector(".color-container input:checked")) {
        colorOptions[0].checked = true;
    }
    const mainImage = document.getElementById("main-image");
    const priceElement = document.getElementById("product-price");
    const phoneId = document.getElementById("prodId");

    function getSelectedValue(name) {
        const selected = document.querySelector(`input[name="${name}"]:checked`);
        return selected ? selected.value : null;
    }

    function fetchProductData() {
        const ram = getSelectedValue("memory")?.split("-")[0];
        const rom = getSelectedValue("memory")?.split("-")[1];
        const color = getSelectedValue("color");

        if (!ram || !rom || !color) {
            return;
        }

        const apiUrl = `http://127.0.0.1:8000/products/api/phonevariant/?phone_id=${phoneId.value}&ram=${ram}&rom=${rom}&color=${encodeURIComponent(color)}`;
        console.log("Fetching data from:", apiUrl);
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                console.log("Dữ liệu API nhận được:", data);
                priceElement.textContent = data.price+"đ";
            })
            .catch(error => console.error("Lỗi khi fetch dữ liệu:", error));
    }
    

    fetchProductData();
    memoryOptions.forEach(input => input.addEventListener("change", fetchProductData));
    colorOptions.forEach(input => input.addEventListener("change", fetchProductData));

});
function toggleReview() {
    let content = document.querySelector(".review-content");
    let button = document.querySelector(".toggle-btn");

    if (content.classList.contains("expanded")) {
        content.classList.remove("expanded");
        button.textContent = "Xem thêm bài viết";
    } else {
        content.classList.add("expanded");
        button.textContent = "Ẩn bớt";
    }
}
