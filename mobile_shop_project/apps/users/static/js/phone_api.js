// Function to fetch phone data from API
async function fetchPhoneData() {
    try {
        const response = await fetch('/products/api/phone/');  // Updated URL to be relative
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching phone data:', error);
        return null;
    }
}

// Function to show notification modal
function showNotificationModal(message, isSuccess = true) {
    // Remove any existing modals first
    const existingModals = document.querySelectorAll('.modal-overlay');
    existingModals.forEach(modal => modal.remove());

    // Create modal elements
    const modalOverlay = document.createElement('div');
    modalOverlay.className = 'modal-overlay';
    
    const modalContent = document.createElement('div');
    modalContent.className = `modal-content ${isSuccess ? 'success' : 'error'}`;
    
    const modalMessage = document.createElement('p');
    modalMessage.textContent = message;
    
    const closeButton = document.createElement('button');
    closeButton.textContent = 'Close';
    closeButton.className = 'modal-close-btn';
    
    // Assemble modal
    modalContent.appendChild(modalMessage);
    modalContent.appendChild(closeButton);
    modalOverlay.appendChild(modalContent);
    document.body.appendChild(modalOverlay);
    
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
    .modal-overlay {
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
    
    .modal-content {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        width: 90%;
        text-align: center;
    }
    
    .modal-content.success {
        border-top: 4px solid #2ecc71;
    }
    
    .modal-content.error {
        border-top: 4px solid #e74c3c;
    }
    
    .modal-close-btn {
        margin-top: 15px;
        padding: 8px 16px;
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .modal-close-btn:hover {
        background-color: #2980b9;
    }
`;

// Add styles to document when the script loads
(function() {
    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);
})();

// Example usage:
// fetchPhoneData().then(data => {
//     if (data) {
//         showNotificationModal('Phone data fetched successfully!');
//         console.log(data);
//     } else {
//         showNotificationModal('Failed to fetch phone data!', false);
//     }
// }); 