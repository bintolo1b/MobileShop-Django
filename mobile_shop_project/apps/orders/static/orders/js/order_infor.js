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
});