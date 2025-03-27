document.addEventListener('DOMContentLoaded', function() {
    const citySelect = document.getElementById('city');
    const districtSelect = document.getElementById('district');

    // Fetch all provinces/cities
    async function fetchCities() {
        try {
            const response = await fetch('https://provinces.open-api.vn/api/p/');
            const cities = await response.json();
            
            // Clear existing options
            citySelect.innerHTML = '<option value="">Chọn Tỉnh/Thành phố</option>';
            
            // Add new options
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

    // Fetch districts for selected city
    async function fetchDistricts(cityCode) {
        try {
            const response = await fetch(`https://provinces.open-api.vn/api/p/${cityCode}?depth=2`);
            const cityData = await response.json();
            
            // Clear existing options
            districtSelect.innerHTML = '<option value="">Chọn Quận/Huyện</option>';
            
            // Add new options
            cityData.districts.forEach(district => {
                const option = document.createElement('option');
                option.value = district.code;
                option.textContent = district.name;
                districtSelect.appendChild(option);
            });

            // Enable district select
            districtSelect.disabled = false;
        } catch (error) {
            console.error('Error fetching districts:', error);
        }
    }

    // Event listener for city selection
    citySelect.addEventListener('change', function() {
        const selectedCityCode = this.value;
        if (selectedCityCode) {
            fetchDistricts(selectedCityCode);
        } else {
            // Clear and disable district select if no city is selected
            districtSelect.innerHTML = '<option value="">Chọn Quận/Huyện</option>';
            districtSelect.disabled = true;
        }
    });

    // Initial city fetch
    fetchCities();
    
    // Initially disable district select
    districtSelect.disabled = true;
});