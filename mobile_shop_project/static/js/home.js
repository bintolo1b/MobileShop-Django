const logout = async function () {
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

    try {
        const response = await fetch("/users/logout/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
            credentials: "include"
        });

        const data = await response.json();
        if (response.ok) {
            window.location.href = "/"
        } else {
            alert(`❌ Lỗi ${response.status}: ${data.message || "Unknown error"}`);
        }
        } catch (error) {
            console.error("🚨 Lỗi khi đăng xuất:", error);
        }
    };

document.addEventListener("DOMContentLoaded", function () {
    const track = document.querySelector(".advertisement-track");
    const dots = document.querySelectorAll(".dot");
    const images = document.querySelectorAll(".advertisement-img");
    const items = document.querySelectorAll(".advertisement-item"); 
    let index = 0;
    let interval;

    function slideTo(i) {
        index = i;
        track.style.transform = `translateX(-${index * 671}px)`;
        updateDots();
    }

    function updateDots() {
        dots.forEach(dot => dot.classList.remove("active"));
        dots[index].classList.add("active");
    }

    function autoSlide() {
        interval = setInterval(() => {
            index = (index + 1) % images.length;
            slideTo(index);
        }, 3000);
    }

    dots.forEach(dot => {
        dot.addEventListener("click", function () {
            clearInterval(interval);
            slideTo(Number(this.dataset.index));
            autoSlide();
        });
    });

    items.forEach((item, i) => {
        item.addEventListener("click", function () {
            clearInterval(interval);
            slideTo(i);
            autoSlide();
        });
    });

    autoSlide(); 
});

document.querySelectorAll('.product-item').forEach(item => {
    item.addEventListener('click', function () {
        const phoneId = this.getAttribute('data-id');
        if (phoneId) {
            window.location.href = `/products/phone/${phoneId}`;
        }
    });
});
document.addEventListener("DOMContentLoaded", function () {
const sliders = document.querySelectorAll(".products-slider"); 

sliders.forEach((slider) => {
    const pages = slider.querySelectorAll(".product-page");
    const container = slider.closest(".products-details-container"); 
    const prevBtn = container.querySelector(".chevron-left-container");
    const nextBtn = container.querySelector(".chevron-right-container");
    const products = slider.querySelectorAll(".product-item");
    let currentPage = 0;
    const pageWidth = slider.offsetWidth; 

    container.addEventListener("mouseenter", function () {
        if (products.length > 10) {
            prevBtn.style.display = "block";
            nextBtn.style.display = "block";
        }
    });

    container.addEventListener("mouseleave", function () {
        prevBtn.style.display = "none";
        nextBtn.style.display = "none";
    });

    function slideToPage(index) {
        slider.style.transform = `translateX(-${index * pageWidth}px)`; 
    }

    nextBtn.addEventListener("click", function () {
        if (currentPage < pages.length - 1) {
            currentPage++;
            slideToPage(currentPage);
        }
    });

    prevBtn.addEventListener("click", function () {
        if (currentPage > 0) {
            currentPage--;
            slideToPage(currentPage);
        }
    });

    window.addEventListener("resize", function () {
        slider.style.transition = "none"; 
        slideToPage(currentPage);
        setTimeout(() => {
            slider.style.transition = "transform 0.5s ease-in-out";
        }, 100);
    });
});
});

const priceElements = document.querySelectorAll('.product-item-new-price');

priceElements.forEach(item => {
  const price = parseInt(item.dataset.price); 
  item.textContent = price.toLocaleString('vi-VN') + 'đ';
});


document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', function () {
        const brand = item.querySelectorAll('.item-name')[0].textContent;
        if (brand) {
            window.location.href = `/products/phonebybrand/?brand=${brand}&page=1`;
        }
    });
});

document.addEventListener("DOMContentLoaded", async function () {
const loginLink = document.querySelector(".header-item a[href='/login']");
const logoutButton = document.querySelector("#logoutButton");

const usernameDisplay = document.getElementById("usernameDisplay");
const userPopup = document.getElementById("userPopup");

usernameDisplay.addEventListener("click", function (event) {
    event.stopPropagation(); 
    userPopup.classList.add("show");
});

document.addEventListener("click", function (event) {
    if (!userPopup.contains(event.target) && event.target !== usernameDisplay) {
        userPopup.classList.remove("show");
    }
});

    logoutButton.onclick = logout;
});


