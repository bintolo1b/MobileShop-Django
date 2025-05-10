// Function to show notification modal
function showNotificationModal(message, isSuccess = true, callback) {
    // Remove any existing modals first
    const existingModals = document.querySelectorAll('.variant-modal-overlay');
    existingModals.forEach(modal => modal.remove());

    // Create modal elements
    const modalOverlay = document.createElement('div');
    modalOverlay.className = 'variant-modal-overlay';
    
    const modalContent = document.createElement('div');
    modalContent.className = `variant-modal-content ${isSuccess ? 'variant-success' : 'variant-error'}`;
    
    const modalMessage = document.createElement('p');
    modalMessage.textContent = message;
    
    const closeButton = document.createElement('button');
    closeButton.textContent = 'Close';
    closeButton.className = 'variant-modal-close-btn';
    
    // Assemble modal
    modalContent.appendChild(modalMessage);
    modalContent.appendChild(closeButton);
    modalOverlay.appendChild(modalContent);
    document.body.appendChild(modalOverlay);
    
    // Call the callback if provided
    if (callback && typeof callback === 'function') {
        callback(modalContent);
    }
    
    // Add event listener to close button
    closeButton.addEventListener('click', () => {
        modalOverlay.remove();
    });
    
    // Auto close after 3 seconds
    setTimeout(() => {
        if (modalOverlay.parentNode) {
            modalOverlay.remove();
        }
    }, 3000);
}

// Add styles for the modal
const styles = `
    .variant-modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }
    
    .variant-modal-content {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        width: 90%;
        text-align: center;
    }
    
    .variant-modal-content.variant-success {
        border-top: 4px solid #2ecc71;
    }
    
    .variant-modal-content.variant-error {
        border-top: 4px solid #e74c3c;
    }
    
    .variant-modal-close-btn {
        margin-top: 15px;
        padding: 8px 16px;
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .variant-modal-close-btn:hover {
        background-color: #2980b9;
    }
`;

// Add styles to document
const styleSheet = document.createElement('style');
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);

// Get CSRF token from cookies
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

// Handle form submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('addPhoneVariantForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData();
            
            // Get selected phone and configuration
            const phoneSelect = document.getElementById('phone');
            const configSelect = document.getElementById('configuration');
            const selectedConfig = configSelect.options[configSelect.selectedIndex];
            
            // Get RAM and ROM from the configuration option text
            const [ram, rom] = selectedConfig.text.split('/');
            
            // Add required fields to FormData
            formData.append('phone_id', phoneSelect.value);
            formData.append('ram', ram);
            formData.append('rom', rom);
            formData.append('color', document.getElementById('color').value);
            formData.append('price', document.getElementById('price').value);
            formData.append('stock', document.getElementById('stock').value);
            
            // Add the image file
            const imgFile = document.getElementById('img').files[0];
            if (imgFile) {
                formData.append('img', imgFile);
            }
            
            // Log the data being sent
            console.log('Sending data:');
            for (let pair of formData.entries()) {
                console.log(pair[0] + ': ' + pair[1]);
            }
            
            try {
                const response = await fetch('/products/api/phonevariant/add/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: formData,
                    credentials: 'include'
                });

                console.log('Response status:', response.status);
                const responseText = await response.text();
                console.log('Raw response:', responseText);

                let data;
                try {
                    data = JSON.parse(responseText);
                } catch (parseError) {
                    console.error('JSON Parse Error:', parseError);
                    showNotificationModal('Server response was not in JSON format', false);
                    return;
                }

                if (response.ok) {
                    showNotificationModal(data.message || 'Thêm biến thể điện thoại thành công', true, function(modalContent) {
                        // Add a button to go back to staff home
                        const button = document.createElement('button');
                        button.textContent = 'Quay lại trang chủ';
                        button.style.marginLeft = '15px';
                        button.style.padding = '5px 10px';
                        button.style.backgroundColor = 'white';
                        button.style.color = '#4CAF50';
                        button.style.border = 'none';
                        button.style.borderRadius = '4px';
                        button.style.cursor = 'pointer';
                        button.onclick = function() {
                            window.location.href = '/users/staff/';
                        };
                        modalContent.appendChild(button);
                    });
                } else {
                    showNotificationModal(data.message || 'Failed to add phone variant', false);
                }
            } catch (error) {
                console.error('Error:', error);
                showNotificationModal('An error occurred while adding the phone variant', false);
            }
        });
    }
}); 