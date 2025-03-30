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

// Search functionality
const searchInput = document.querySelector('.region-search-input');
const searchSuggestions = document.querySelector('.search-suggestions');

// Show suggestions when input is focused
searchInput.addEventListener('focus', () => {
    searchSuggestions.classList.add('active');
});

// Hide suggestions when clicking outside
document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
        searchSuggestions.classList.remove('active');
    }
});

// Handle suggestion item click
document.querySelectorAll('.suggestion-item').forEach(item => {
    item.addEventListener('click', () => {
        searchInput.value = item.querySelector('span').textContent;
        searchSuggestions.classList.remove('active');
        // Here you can add the logic to perform the search
    });
});

// Handle input changes
searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    const suggestions = document.querySelectorAll('.suggestion-item');
    
    suggestions.forEach(suggestion => {
        const text = suggestion.querySelector('span').textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            suggestion.style.display = 'flex';
            // Highlight matching text
            const span = suggestion.querySelector('span');
            if (searchTerm) {
                const regex = new RegExp(`(${searchTerm})`, 'gi');
                span.innerHTML = text.replace(regex, '<span class="highlight">$1</span>');
            } else {
                span.textContent = text;
            }
        } else {
            suggestion.style.display = 'none';
        }
    });
});

function showBrandPhones(brand) {
    // Get the products container
    const productsContainer = document.querySelector('.products-details-container');
    const productsSlider = productsContainer.querySelector('.products-slider');
    
    // Clear existing content
    productsSlider.innerHTML = '';
    
    // Get phones based on brand
    let phones;
    switch(brand) {
        case 'iPhone':
            phones = document.querySelectorAll('.products-details:nth-child(3) .product-item');
            break;
        case 'Xiaomi':
            phones = document.querySelectorAll('.products-details:nth-child(5) .product-item');
            break;
        case 'Realme':
            phones = document.querySelectorAll('.products-details:nth-child(4) .product-item');
            break;
    }

    // Calculate number of phones per page (2 rows * 5 phones per row = 10 phones per page)
    const phonesPerPage = 10;
    
    // Create pages based on number of phones
    for (let i = 0; i < phones.length; i += phonesPerPage) {
        const productPage = document.createElement('div');
        productPage.className = 'product-page';
        
        // Get phones for this page
        const pagePhones = Array.from(phones).slice(i, i + phonesPerPage);
        
        // Clone and append each phone
        pagePhones.forEach(phone => {
            const phoneClone = phone.cloneNode(true);
            // Add click event listener to the cloned phone
            phoneClone.addEventListener('click', function() {
                const phoneId = this.getAttribute('data-id');
                if (phoneId) {
                    window.location.href = `/products/phone/${phoneId}`;
                }
            });
            productPage.appendChild(phoneClone);
        });
        
        // Add the product page to the slider
        productsSlider.appendChild(productPage);
    }

    // Reset slider position
    productsSlider.style.transform = 'translateX(0)';
    
    // Show/hide navigation arrows based on number of pages
    const prevBtn = productsContainer.querySelector('.chevron-left-container');
    const nextBtn = productsContainer.querySelector('.chevron-right-container');
    
    if (phones.length > phonesPerPage) {
        prevBtn.style.display = 'block';
        nextBtn.style.display = 'block';
    } else {
        prevBtn.style.display = 'none';
        nextBtn.style.display = 'none';
    }
}