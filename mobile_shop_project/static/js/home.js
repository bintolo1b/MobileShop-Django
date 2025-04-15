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

// Clear default suggestions
searchSuggestions.innerHTML = '';

// Get CSRF token from cookies
function getCSRFToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Hide suggestions when clicking outside
document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
        searchSuggestions.classList.remove('active');
    }
});

// Debounce function to limit API calls
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Function to format price
function formatPrice(price) {
    return price.toLocaleString('vi-VN') + 'đ';
}

// Function to perform search
async function performSearch(searchTerm) {
    if (!searchTerm.trim()) {
        searchSuggestions.innerHTML = '';
        searchSuggestions.classList.remove('active');
        return;
    }

    try {
        const csrfToken = getCSRFToken();
        const response = await fetch('/products/api/search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                "search_query": searchTerm
            }),
            credentials: 'same-origin'
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Search response:', data); // Debug log
        
        // Clear previous suggestions
        searchSuggestions.innerHTML = '';

        if (data.results && data.results.length > 0) {
            // Display results
            data.results.forEach(phone => {
                const suggestionItem = document.createElement('div');
                suggestionItem.className = 'suggestion-item';
                suggestionItem.innerHTML = `
                    <img src="${phone.image_url}" alt="${phone.name}" class="suggestion-item-img">
                    <div class="suggestion-item-info">
                        <span class="suggestion-item-name">${phone.name}</span>
                        <span class="suggestion-item-price">${formatPrice(phone.min_price)}</span>
                    </div>
                `;
                
                // Add click handler to navigate to product detail
                suggestionItem.addEventListener('click', () => {
                    window.location.href = `/products/phone/${phone.id}`;
                });
                
                searchSuggestions.appendChild(suggestionItem);
            });
            searchSuggestions.classList.add('active');
        } else {
            // Show no results message
            const noResults = document.createElement('div');
            noResults.className = 'suggestion-item no-results';
            noResults.textContent = 'Không tìm thấy sản phẩm';
            searchSuggestions.appendChild(noResults);
            searchSuggestions.classList.add('active');
        }
    } catch (error) {
        console.error('Search error:', error); // Debug log
        searchSuggestions.innerHTML = '';
        const errorMessage = document.createElement('div');
        errorMessage.className = 'suggestion-item no-results';
        errorMessage.textContent = 'Có lỗi xảy ra khi tìm kiếm';
        searchSuggestions.appendChild(errorMessage);
        searchSuggestions.classList.add('active');
    }
}

// Handle input changes with debounce
searchInput.addEventListener('input', debounce((e) => {
    const searchTerm = e.target.value;
    if (searchTerm.length >= 2) { // Only search if 2 or more characters
        performSearch(searchTerm);
    } else {
        searchSuggestions.innerHTML = '';
        searchSuggestions.classList.remove('active');
    }
}, 300)); // Wait 300ms after user stops typing

// Add keyboard navigation
searchInput.addEventListener('keydown', (e) => {
    const suggestions = searchSuggestions.querySelectorAll('.suggestion-item');
    const current = searchSuggestions.querySelector('.suggestion-item.selected');
    
    if (suggestions.length === 0) return;

    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault();
        
        let next;
        if (!current) {
            next = e.key === 'ArrowDown' ? suggestions[0] : suggestions[suggestions.length - 1];
        } else {
            const currentIndex = Array.from(suggestions).indexOf(current);
            current.classList.remove('selected');
            
            if (e.key === 'ArrowDown') {
                next = suggestions[currentIndex + 1] || suggestions[0];
            } else {
                next = suggestions[currentIndex - 1] || suggestions[suggestions.length - 1];
            }
        }
        
        next.classList.add('selected');
        searchInput.value = next.querySelector('.suggestion-item-name').textContent;
    } else if (e.key === 'Enter' && current) {
        e.preventDefault();
        window.location.href = `/products/phone/${current.dataset.id}`;
    }
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
async function updateProductStars(productId, starsContainer) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/products/api/rating/count/${productId}`);
        const data = await response.json();
        
        // Calculate average rating
        let totalStars = 0;
        let totalRatings = 0;
        
        for (let i = 1; i <= 5; i++) {
            totalStars += i * data[i];
            totalRatings += data[i];
        }
        
        const averageRating = totalRatings > 0 ? totalStars / totalRatings : 0;
        
        // Update stars display
        const stars = starsContainer.querySelectorAll('i');
        stars.forEach((star, index) => {
            // Remove all existing classes
            star.className = '';
            
            if (index + 0.5 < averageRating) {
                // Full star
                star.className = 'fa-solid fa-star active';
            } else if (index < averageRating) {
                // Half star
                star.className = 'fa-solid fa-star-half-stroke active';
            } else {
                // Empty star
                star.className = 'fa-regular fa-star';
            }
        });
    } catch (error) {
        console.error('Error fetching rating:', error);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    // Update stars for all products
    document.querySelectorAll('.product-item').forEach(item => {
        const productId = item.getAttribute('data-id');
        const starsContainer = item.querySelector('.product-item-stars');
        if (productId && starsContainer) {
            updateProductStars(productId, starsContainer);
        }
    });
    
    // ... rest of your DOMContentLoaded code ...
});
