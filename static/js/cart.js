$(document).ready(function () {
    // Toggle sticky cart dropdown
    $('#cart-toggle-btn').on('click', function () {
        $('#sticky-cart-dropdown').toggleClass('d-none');
    });

    // Update cart count badge - Fixed to target the correct element
    function updateCartCount(count) {
        const cartBadge = $('.cart-badge'); // Target the cart badge in navbar
        if (count > 0) {
            cartBadge.text(count).show();
        } else {
            cartBadge.text('0').hide();
        }
        
        // Also update sticky cart count if it exists
        const stickyCartBadge = $('#sticky-cart-count');
        if (stickyCartBadge.length) {
            if (count > 0) {
                stickyCartBadge.text(count).show();
            } else {
                stickyCartBadge.text('0').hide();
            }
        }
    }

    function updateCartTotal(total) {
        $('#cart-total').text(`KSh${total.toFixed(2)}`);
        // Also update sticky cart total if it exists
        $('#sticky-cart-total').text(`Kshs ${total.toFixed(2)}`);
    }

    // Load cart content into sticky dropdown and mini cart
    function loadStickyCart() {
        $.get('/cart', function (data) {
            const cartItems = data.cart || [];
            const total = data.total || 0;
            let html = '';
            let miniCartHtml = '';

            if (cartItems.length === 0) {
                html = '<li class="list-group-item text-center">Cart is empty.</li>';
                miniCartHtml = '<li class="list-group-item text-center text-muted">Your cart is empty</li>';
            } else {
                cartItems.forEach(item => {
                    const itemTotal = (item.price * item.quantity).toFixed(2);
                    html += `
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            <div>
                                <small>${item.name}</small><br>
                                <small class="text-muted">Qty: ${item.quantity}</small>
                            </div>
                            <span>Kshs ${itemTotal}</span>
                        </li>`;
                    
                    miniCartHtml += `
                        <li class="list-group-item d-flex justify-content-between align-items-center py-2">
                            <div class="flex-grow-1">
                                <div class="fw-bold small">${item.name}</div>
                                <small class="text-muted">Qty: ${item.quantity} × Kshs ${item.price.toFixed(2)}</small>
                            </div>
                            <span class="text-success fw-bold">Kshs ${itemTotal}</span>
                        </li>`;
                });
            }

            $('#sticky-cart-items').html(html);
            $('#sticky-cart-total').text(`Kshs ${total.toFixed(2)}`);
            
            // Update mini cart
            $('#mini-cart-items').html(miniCartHtml);
            $('#mini-cart-total').text(`Kshs ${total.toFixed(2)}`);
        });
    }

    // Show mini cart temporarily after adding items
    function showMiniCart() {
        const miniCart = $('#mini-cart');
        miniCart.fadeIn(300);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            miniCart.fadeOut(300);
        }, 5000);
    }

    // Mini cart close button
    $('#close-mini-cart').on('click', function() {
        $('#mini-cart').fadeOut(300);
    });

    // Add to cart handler (event delegation for dynamic elements)
    $(document).on('click', '.add-to-cart', function () {
        const productId = $(this).data('id');
        let quantity = $(this).data('quantity') || 1;
        
        // Check if there's a quantity input field on the page
        const quantityInput = $('#quantity');
        if (quantityInput.length && quantityInput.val()) {
            quantity = parseInt(quantityInput.val()) || 1;
        }
        
        const button = $(this);
        
        // Disable button and show loading state
        button.prop('disabled', true);
        const originalText = button.html();
        button.html('<span class="spinner-border spinner-border-sm me-2" role="status"></span>Adding...');

        $.ajax({
            type: 'POST',
            url: '/cart/add',
            contentType: 'application/json',
            data: JSON.stringify({ product_id: productId, quantity }),
            success: function (response) {
                // Update cart count and total immediately
                updateCartCount(response.cart_count || 0);
                updateCartTotal(response.total || 0);
                loadStickyCart();

                // Show success feedback
                button.removeClass('btn-primary').addClass('btn-success');
                button.html('<i class="bi bi-check-lg me-2"></i>Added!');
                
                // Show toast notification with quantity info
                const message = quantity > 1 ? 
                    `${quantity} items added to cart` : 
                    (response.message || 'Item added to cart');
                $('#toast-message').text(message);
                new bootstrap.Toast(document.getElementById('cart-toast')).show();
                
                // Add visual animation to cart icon
                $('.cart-badge').addClass('cart-update-animation');
                setTimeout(() => {
                    $('.cart-badge').removeClass('cart-update-animation');
                }, 800);
                
                // Show mini cart preview
                setTimeout(() => {
                    showMiniCart();
                }, 500);
                
                // Reset button after 2 seconds
                setTimeout(() => {
                    button.prop('disabled', false);
                    button.removeClass('btn-success').addClass('btn-primary');
                    button.html(originalText);
                }, 2000);
            },
            error: function (xhr) {
                // Reset button on error
                button.prop('disabled', false);
                button.html(originalText);
                
                // Add shake animation for error
                $('.cart-badge').addClass('cart-shake');
                setTimeout(() => {
                    $('.cart-badge').removeClass('cart-shake');
                }, 500);
                
                $('#toast-message').text(xhr.responseJSON?.error || 'An error occurred.');
                new bootstrap.Toast(document.getElementById('cart-toast')).show();
            }
        });
    });

    // Initial load and periodic sync
    function syncCartData() {
        $.get('/cart/count', function (data) {
            updateCartCount(data.cart_count || 0);
            updateCartTotal(data.total || 0);
        }).fail(function() {
            console.warn('Failed to sync cart data');
        });
    }

    // Load cart data on page load
    syncCartData();
    loadStickyCart();

    // Sync cart data every 30 seconds to handle multiple tabs/sessions
    setInterval(syncCartData, 30000);

    // Sync when page becomes visible again (user switches back to tab)
    document.addEventListener('visibilitychange', function() {
        if (!document.hidden) {
            syncCartData();
            loadStickyCart();
        }
    });
});
