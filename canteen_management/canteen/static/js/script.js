// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {
    // 1. Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 2. Auto-dismiss alerts after 5 seconds
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (bootstrap.Alert.getInstance(alert)) {
                bootstrap.Alert.getInstance(alert).close();
            }
        }, 5000);
    });

    // 3. Quantity adjustment and price calculation
    const quantityInput = document.querySelector('.quantity-input');
    const unitPriceElement = document.querySelector('.unit-price');
    const totalPriceElement = document.querySelector('.total-price');
    const decreaseBtn = document.querySelector('.decrease-quantity');
    const increaseBtn = document.querySelector('.increase-quantity');

    if (quantityInput && unitPriceElement && totalPriceElement) {
        // Get initial unit price (remove currency symbol)
        const unitPrice = parseFloat(unitPriceElement.textContent.replace(/[^0-9.]/g, ''));

        // Function to update total price
        function updateTotalPrice() {
            let quantity = parseInt(quantityInput.value);
            if (isNaN(quantity) quantity = 1;
            if (quantity < 1) quantity = 1;
            
            const totalPrice = quantity * unitPrice;
            totalPriceElement.textContent = '₹' + totalPrice.toFixed(2);
            
            // Update hidden form field if exists
            const totalPriceField = document.getElementById('id_total_price');
            if (totalPriceField) {
                totalPriceField.value = totalPrice.toFixed(2);
            }
        }

        // Button event handlers
        if (decreaseBtn && increaseBtn) {
            decreaseBtn.addEventListener('click', function(e) {
                e.preventDefault();
                let quantity = parseInt(quantityInput.value);
                if (quantity > 1) {
                    quantityInput.value = quantity - 1;
                    updateTotalPrice();
                }
            });

            increaseBtn.addEventListener('click', function(e) {
                e.preventDefault();
                let quantity = parseInt(quantityInput.value);
                quantityInput.value = quantity + 1;
                updateTotalPrice();
            });
        }

        // Input event handlers
        quantityInput.addEventListener('change', updateTotalPrice);
        quantityInput.addEventListener('input', updateTotalPrice);

        // Initial calculation
        updateTotalPrice();
    }
});