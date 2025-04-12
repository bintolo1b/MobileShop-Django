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
    
    stars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = this.getAttribute('data-rating');
            stars.forEach(s => s.classList.remove('active'));
            
            stars.forEach(s => {
                if (s.getAttribute('data-rating') <= rating) {
                    s.classList.add('active');
                }
            });
            
            console.log('Rating selected:', rating);
        });
    });
    


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
