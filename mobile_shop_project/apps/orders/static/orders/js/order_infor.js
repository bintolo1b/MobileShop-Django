document.addEventListener('DOMContentLoaded', function() {
    const citySelect = document.getElementById('city');
    const districtSelect = document.getElementById('district');

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