document.addEventListener('DOMContentLoaded', function() {
    const citySelect = document.getElementById('city');
    const districtSelect = document.getElementById('district');

    // Custom notification function (if not available in global scope)
    function showNotification(message, type = 'info', duration = 5000) {
        const popup = document.getElementById('notificationPopup');
        const messageElement = document.getElementById('notificationMessage');
        
        // Reset classes
        popup.className = 'notification-popup';
        
        // Add type class
        if (type === 'success' || type === 'error' || type === 'warning') {
            popup.classList.add(type);
        }
        
        // Set message
        messageElement.textContent = message;
        
        // Show popup
        popup.style.display = 'block';
        
        // Auto hide after duration
        if (duration > 0) {
            setTimeout(() => {
                closeNotification();
            }, duration);
        }
    }
    
    function closeNotification() {
        const popup = document.getElementById('notificationPopup');
        popup.style.animation = 'fadeOut 0.3s';
        
        setTimeout(() => {
            popup.style.display = 'none';
            popup.style.animation = 'slideIn 0.3s ease-out';
        }, 300);
    }

    async function fetchCities() {
        try {
            const response = await fetch('https://provinces.open-api.vn/api/p/');
            const cities = await response.json();
            
            citySelect.innerHTML = '<option value="">Chọn Tỉnh/Thành phố</option>';
            
            cities.forEach(city => {
                const option = document.createElement('option');
                option.value = city.code;
                option.textContent = city.name;
                citySelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching cities:', error);
        }
    }

    async function fetchDistricts(cityCode) {
        try {
            const response = await fetch(`https://provinces.open-api.vn/api/p/${cityCode}?depth=2`);
            const cityData = await response.json();

            districtSelect.innerHTML = '<option value="">Chọn Quận/Huyện</option>';

            cityData.districts.forEach(district => {
                const option = document.createElement('option');
                option.value = district.code;
                option.textContent = district.name;
                districtSelect.appendChild(option);
            });

            districtSelect.disabled = false;
        } catch (error) {
            console.error('Error fetching districts:', error);
        }
    }

    citySelect.addEventListener('change', function() {
        const selectedCityCode = this.value;
        if (selectedCityCode) {
            fetchDistricts(selectedCityCode);
        } else {
            districtSelect.innerHTML = '<option value="">Chọn Quận/Huyện</option>';
            districtSelect.disabled = true;
        }
    });

    fetchCities();
    districtSelect.disabled = true;
    function formatPrice() {
        document.querySelectorAll('.total-price').forEach(priceElement => {
            const price = priceElement.textContent.replace('₫', '').trim();
            const formattedPrice = parseInt(price).toLocaleString('vi-VN') + '₫';
            priceElement.textContent = formattedPrice;
        });

        // Format tổng tiền
        const orderTotal = document.querySelector('.order-total span:last-child');
        if (orderTotal) {
            const totalPrice = orderTotal.textContent.replace('₫', '').trim();
            const formattedTotal = parseInt(totalPrice).toLocaleString('vi-VN') + '₫';
            orderTotal.textContent = formattedTotal;
        }
    }
    formatPrice();

    const paymentInputs = document.querySelectorAll('input[name="payment"]');
    const onlinePaymentDetails = document.getElementById('onlinePaymentDetails');
    const continueButton = document.querySelector('.continue-button');
    continueButton.addEventListener('click', handleOrderSubmission);


    async function handleOrderSubmission() {
        try {
            const paymentMethod = document.querySelector('input[name="payment"]:checked').value;
            const formData = new FormData();

            if (paymentMethod === 'online') {
                const paymentProof = document.getElementById('payment-proof');
                if (paymentProof.files.length > 0) {
                    formData.append('payment_screenshot', paymentProof.files[0]);
                } else {
                    showNotification('Vui lòng tải lên ảnh chứng minh thanh toán', 'error');
                    return;
                }
            }

            const clientName = document.querySelector('.customer-info input[type="text"]').value;
            const phoneNumber = document.querySelector('.customer-info input[type="tel"]').value;
            const email = document.querySelector('.customer-info input[type="email"]').value;
            const cityElement = document.getElementById('city');
            const districtElement = document.getElementById('district');
            const cityName = cityElement.options[cityElement.selectedIndex].text;
            const districtName = districtElement.options[districtElement.selectedIndex].text;
            const address = document.querySelector('.delivery-info input[type="text"]').value;
            const note = document.querySelector('.delivery-info textarea').value;

            
            // console.log('Payment Method:', paymentMethod);
            // console.log('Client Name:', clientName);
            // console.log('Phone Number:', phoneNumber);
            // console.log('Email:', email);
            // console.log('City:', cityName);
            // console.log('District:', districtName);
            // console.log('Address:', address);
            // console.log('Note:', note);

            if (!cityElement.value) {
                showNotification('Vui lòng điền đầy đủ thông tin', 'error');
                return;
            }
            if (!districtElement.value) {
                showNotification('Vui lòng điền đầy đủ thông tin', 'error');
                return;
            }
            // Validate thông tin
            if (!clientName || !phoneNumber || !email || !address) {
                showNotification('Vui lòng điền đầy đủ thông tin', 'error');
                return;
            }

            // Tạo object data
            const data = {
                payment_method: paymentMethod === 'online' ? 'Thanh toán online' : 'Thanh toán khi nhận hàng',
                client_name: clientName,
                client_phone: phoneNumber,
                email: email,
                address: `${address}, ${districtName}, ${cityName}`,
                note: note
            };

            console.log('Request Data Object:');
            console.log('-------------------');
            console.log(data);
            formData.append('data', JSON.stringify(data));

            // Lấy CSRF token từ cookie
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            const response = await fetch('/orders/confirm_payment/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                showNotification('Đặt hàng thành công!', 'success');
                setTimeout(() => {
                    window.location.href = '/orders';
                }, 1500);
            } else {
                throw new Error(result.message || 'Có lỗi xảy ra');
            }

        } catch (error) {
            showNotification('Vui lòng điền đầy đủ thông tin','error');
            console.error('Error:', error);
        }
    }
    paymentInputs.forEach(input => {
        input.addEventListener('change', function() {
            if (this.value === 'online') {
                onlinePaymentDetails.style.display = 'block';
                continueButton.textContent = 'Xác nhận thanh toán';
            } else {
                onlinePaymentDetails.style.display = 'none';
                continueButton.textContent = 'Đặt hàng';
            }
        });
    });

    // Xử lý preview ảnh thanh toán
    const paymentProofInput = document.getElementById('payment-proof');
    const previewContainer = document.getElementById('preview-container');

    paymentProofInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewContainer.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
            }
            reader.readAsDataURL(file);
        }
    });
    
});

