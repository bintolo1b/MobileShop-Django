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
    const statusElemnt= document.getElementById("status-info");
    const phoneId = document.getElementById("prodId");
    let selectedVariantId = null;

    document.querySelectorAll('.color-options input').forEach(input => {
        input.addEventListener('change', function () {
            let selectedLabel = this.closest('label');
            let newImage = selectedLabel.getAttribute('data-image');
            document.getElementById("main-image").src = newImage;
        });
    });

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
                priceElement.textContent = parseInt(data.price).toLocaleString('vi-VN') + "đ";
                statusElemnt.textContent = data.stock;
            })
            .catch(error => console.error("Lỗi khi fetch dữ liệu:", error));
    }
    
    

    fetchProductData();
    memoryOptions.forEach(input => input.addEventListener("change", fetchProductData));
    colorOptions.forEach(input => input.addEventListener("change", fetchProductData));


    function initializeVariants() {
        document.querySelectorAll('[id^="memory-"]').forEach(element => {
            const dataVariants = element.getAttribute('data-variants');
            if (dataVariants) {
                console.log(`Loaded variants for ${element.id}:`, dataVariants);
            }
        });
    }

    function updateSelectedVariant() {
        const selectedColor = document.querySelector('input[name="color"]:checked');
        const selectedMemory = document.querySelector('input[name="memory"]:checked');
        
        if (selectedColor && selectedMemory) {
            const variants = JSON.parse(selectedMemory.getAttribute('data-variants'));
            selectedVariantId = variants[selectedColor.value];
            console.log('Selected variant ID:', selectedVariantId);
        }
    }

    // Thêm event listeners cho color và memory inputs
    document.querySelectorAll('input[name="color"], input[name="memory"]')
        .forEach(input => input.addEventListener('change', updateSelectedVariant));

    initializeVariants();
    updateSelectedVariant();

    const addToCartBtn = document.getElementById('add-to-cart-btn');
    
    addToCartBtn.addEventListener('click', async function() {
        const productImage = document.getElementById('main-image');
        const all_cart = document.querySelectorAll('.item-icon-container');
        const cart = all_cart[2];

        const flyingImage = productImage.cloneNode();
        const productRect = productImage.getBoundingClientRect();
        const cartRect = cart.getBoundingClientRect();

        const cartCenterX = cartRect.left + (cartRect.width / 2);
        const cartCenterY = cartRect.top + (cartRect.height / 2);

        flyingImage.classList.add('flying-image');
        flyingImage.style.width = productRect.width + 'px';
        flyingImage.style.height = productRect.height + 'px';
        flyingImage.style.left = productRect.left + 'px';
        flyingImage.style.top = productRect.top + 'px';

        document.body.appendChild(flyingImage);

        setTimeout(() => {
            flyingImage.classList.add('flying');
            flyingImage.style.left = cartCenterX + 'px';
            flyingImage.style.top = cartCenterY + 'px';
        }, 0);
        
        const animateCart = async () => {
            // Start cart animation
            cart.classList.add('cart-animation');
            
            // Add flying image
            document.body.appendChild(flyingImage);
    
            // Start flying animation
            await new Promise(resolve => {
                setTimeout(() => {
                    flyingImage.classList.add('flying');
                    flyingImage.style.left = cartCenterX + 'px';
                    flyingImage.style.top = cartCenterY + 'px';
                    resolve();
                }, 0);
            });
    
            // Remove flying image and cart animation
            await new Promise(resolve => {
                setTimeout(() => {
                    flyingImage.remove();
                    cart.classList.remove('cart-animation');
                    resolve();
                }, 800); // Match transition time from CSS
            });
        };
        await animateCart();
        


        console.log("Clicking add to cart with variant ID:", selectedVariantId);
        if (!selectedVariantId) {
            alert('Vui lòng chọn màu sắc và bộ nhớ');
            return;
        }
    
        const apiUrl = 'http://127.0.0.1:8000/cart/add-to-cart/';
        console.log("Cart API URL:", apiUrl);
        
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
            body: JSON.stringify({
                phone_variant_id: selectedVariantId,
                quantity: 1
            })
        })
        .then(response => {
            if (response.ok) {
                // alert('Đã thêm sản phẩm vào giỏ hàng');
            } else if (response.status === 401) {
                alert('Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng');
                window.location.href = '/login';
            } else {
                response.text().then(text => {
                    console.error("Error response:", text);
                    alert(`Có lỗi xảy ra khi thêm vào giỏ hàng: ${text}`);
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Có lỗi xảy ra khi thêm vào giỏ hàng');
        });
    });
    const stars = document.querySelectorAll('.star-rating i');
    const ratingInput = document.querySelector('.rating-input');
    const submitRatingBtn = document.getElementById('submitRating');
    let selectedRating = 0;
    
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('vi-VN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    function createStarRating(rating) {
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            stars += `<i class="fa-solid fa-star${i <= rating ? ' active' : ''}"></i>`;
        }
        return stars;
    }

    function updateStarCounts(ratings) {
        const counts = [0, 0, 0, 0, 0];
        ratings.forEach(rating => {
            counts[rating.star - 1]++;
        });
        for (let i = 1; i <= 5; i++) {
            document.getElementById(`star${i}-count`).textContent = counts[i-1];
        }
    }

    function displayRatings(ratings) {
        const ratingsList = document.querySelector('.ratings-list');
        const productId = document.getElementById('prodId').value;
        
        // First fetch the current user's rating
        fetch(`http://127.0.0.1:8000/products/api/rating/client/${productId}`)
            .then(response => response.json())
            .then(userRating => {
                // Now display all ratings, marking the user's rating as "Bạn"
                ratingsList.innerHTML = ratings.map(rating => `
                    <div class="rating-item">
                        <div class="rating-user-avatar">
                            <i class="fa-solid fa-user"></i>
                        </div>
                        <div class="rating-content">
                            <div class="rating-header">
                                <span class="rating-user-name">${userRating && rating.id === userRating.id ? 'Bạn' : rating.client}</span>
                                <span class="rating-date">${formatDate(rating.created_at)}</span>
                            </div>
                            <div class="rating-stars">
                                ${Array(5).fill().map((_, i) => 
                                    `<i class="fa-solid fa-star${i < rating.star ? ' active' : ''}"></i>`
                                ).join('')}
                            </div>
                            <div class="rating-comment">${rating.comment}</div>
                        </div>
                    </div>
                `).join('');
                updateStarCounts(ratings);
            })
            .catch(error => {
                // If fetching user rating fails, just display ratings normally
                console.error('Error fetching user rating:', error);
                displayRatingsWithoutUser(ratings);
            });
    }

    // Fallback function if we can't fetch user rating
    function displayRatingsWithoutUser(ratings) {
        const ratingsList = document.querySelector('.ratings-list');
        ratingsList.innerHTML = ratings.map(rating => `
            <div class="rating-item">
                <div class="rating-user-avatar">
                    <i class="fa-solid fa-user"></i>
                </div>
                <div class="rating-content">
                    <div class="rating-header">
                        <span class="rating-user-name">${rating.client}</span>
                        <span class="rating-date">${formatDate(rating.created_at)}</span>
                    </div>
                    <div class="rating-stars">
                        ${Array(5).fill().map((_, i) => 
                            `<i class="fa-solid fa-star${i < rating.star ? ' active' : ''}"></i>`
                        ).join('')}
                    </div>
                    <div class="rating-comment">${rating.comment}</div>
                </div>
            </div>
        `).join('');
        updateStarCounts(ratings);
    }

    function fetchRatings() {
        const productId = document.getElementById('prodId').value;
        fetch(`http://127.0.0.1:8000/products/api/rating/${productId}`)
            .then(response => response.json())
            .then(data => {
                console.log('Ratings data:', data);
                if (Array.isArray(data.ratings)) {
                    displayRatings(data.ratings);
                }
            })
            .catch(error => console.error('Error fetching ratings:', error));
    }

    stars.forEach(star => {
        star.addEventListener('click', function() {
            selectedRating = parseInt(this.getAttribute('data-rating'));
            stars.forEach(s => s.classList.remove('active'));
            
            stars.forEach(s => {
                if (parseInt(s.getAttribute('data-rating')) <= selectedRating) {
                    s.classList.add('active');
                }
            });
            
            ratingInput.style.display = 'flex';
        });
    });

    submitRatingBtn.addEventListener('click', function() {
        if (!selectedRating) {
            alert('Vui lòng chọn số sao đánh giá');
            return;
        }

        const comment = document.getElementById('ratingComment').value;
        const productId = document.getElementById('prodId').value;

        fetch('http://127.0.0.1:8000/products/api/rating/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
            body: JSON.stringify({
                product_id: productId,
                star: selectedRating,
                comment: comment
            })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else if (response.status === 401) {
                alert('Vui lòng đăng nhập để đánh giá sản phẩm');
                window.location.href = '/login';
                throw new Error('Unauthorized');
            }
            throw new Error('Network response was not ok');
        })
        .then(data => {
            console.log('Rating submitted:', data);
            // Reset form
            selectedRating = 0;
            document.getElementById('ratingComment').value = '';
            ratingInput.style.display = 'none';
            stars.forEach(s => s.classList.remove('active'));
            
            // Fetch all ratings again to get the updated list
            fetch(`http://127.0.0.1:8000/products/api/rating/${productId}`)
                .then(response => response.json())
                .then(data => {
                    if (Array.isArray(data.ratings)) {
                        displayRatings(data.ratings);
                    }
                })
                .catch(error => console.error('Error fetching updated ratings:', error));
        })
        .catch(error => {
            console.error('Error:', error);
            if (error.message !== 'Unauthorized') {
                alert('Có lỗi xảy ra khi gửi đánh giá');
            }
        });
    });

    // Fetch initial ratings
    fetchRatings();
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
function getCookie(name) {
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

// Rating functionality
let selectedRating = 0;
const starRating = document.querySelector('.star-rating');
const ratingInput = document.querySelector('.rating-input');
const submitRatingBtn = document.getElementById('submitRating');
const ratingsList = document.querySelector('.ratings-list');

// Initialize rating display
function initializeRatings(ratings) {
    const counts = [0, 0, 0, 0, 0];
    let total = 0;
    
    ratings.forEach(rating => {
        counts[rating.stars - 1]++;
        total++;
    });
    
    // Update star counts and bars
    for (let i = 0; i < 5; i++) {
        const percent = total ? (counts[i] / total * 100) : 0;
        document.getElementById(`star${i+1}-count`).textContent = counts[i];
        document.querySelector(`.qa-row:nth-child(${5-i}) .bar`).style.setProperty('--rating-percent', `${percent}%`);
    }
    
    // Display ratings
    displayRatings(ratings);
}

// Handle star selection
starRating.addEventListener('click', (e) => {
    if (e.target.matches('i.fa-star')) {
        selectedRating = parseInt(e.target.dataset.rating);
        updateStarDisplay();
        ratingInput.style.display = 'block';
    }
});

// Update star display
function updateStarDisplay() {
    const stars = starRating.querySelectorAll('i.fa-star');
    stars.forEach((star, index) => {
        if (index < selectedRating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

// Handle hover effects
starRating.addEventListener('mouseover', (e) => {
    if (e.target.matches('i.fa-star')) {
        const hoverRating = parseInt(e.target.dataset.rating);
        const stars = starRating.querySelectorAll('i.fa-star');
        stars.forEach((star, index) => {
            if (index < hoverRating) {
                star.style.color = '#ffd700';
            } else {
                star.style.color = '#ddd';
            }
        });
    }
});

// Reset stars when mouse leaves
starRating.addEventListener('mouseleave', () => {
    const stars = starRating.querySelectorAll('i.fa-star');
    stars.forEach((star, index) => {
        if (index < selectedRating) {
            star.style.color = '#ffd700';
        } else {
            star.style.color = '#ddd';
        }
    });
});

// Handle rating submission
submitRatingBtn.addEventListener('click', async () => {
    if (!selectedRating) {
        alert('Vui lòng chọn số sao đánh giá');
        return;
    }
    
    const comment = document.getElementById('ratingComment').value;
    const productId = document.querySelector('[data-product-id]').dataset.productId;
    
    try {
        const response = await fetch('/api/ratings/submit/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                product_id: productId,
                stars: selectedRating,
                comment: comment
            })
        });
        
        if (response.ok) {
            const newRating = await response.json();
            // Add new rating to list and update stats
            const ratings = [...document.querySelectorAll('.rating-item')].map(item => ({
                stars: parseInt(item.dataset.stars),
                comment: item.querySelector('.rating-comment').textContent,
                user: item.querySelector('.rating-user').textContent,
                date: item.querySelector('.rating-date').textContent
            }));
            ratings.unshift(newRating);
            initializeRatings(ratings);
            
            // Reset form
            selectedRating = 0;
            updateStarDisplay();
            document.getElementById('ratingComment').value = '';
            ratingInput.style.display = 'none';
        } else {
            alert('Có lỗi xảy ra khi gửi đánh giá');
        }
    } catch (error) {
        console.error('Error submitting rating:', error);
        alert('Có lỗi xảy ra khi gửi đánh giá');
    }
});

// Helper function to get CSRF token
function getCookie(name) {
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

// Initialize ratings when page loads
document.addEventListener('DOMContentLoaded', () => {
    const productId = document.querySelector('[data-product-id]').dataset.productId;
    fetch(`/api/ratings/${productId}/`)
        .then(response => response.json())
        .then(ratings => initializeRatings(ratings))
        .catch(error => console.error('Error fetching ratings:', error));
});
