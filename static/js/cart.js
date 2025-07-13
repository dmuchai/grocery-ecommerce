$(document).ready(function () {
    // Toggle sticky cart dropdown
    $('#cart-toggle-btn').on('click', function () {
        $('#sticky-cart-dropdown').toggleClass('d-none');
    });

    // Update cart count badge
    function updateCartCount(count) {
        const cartBadge = $('#sticky-cart-count');
        if (count > 0) {
            cartBadge.text(count).show();
        } else {
            cartBadge.text('0').hide();
        }
    }

    function updateCartTotal(total) {
	$('#cart-total').text(`KSh${total.toFixed(2)}`);
    }

    // Load cart content into sticky dropdown
    function loadStickyCart() {
        $.get('/cart', function (data) {
            const cartItems = data.cart || [];
            const total = data.total || 0;
            let html = '';

            if (cartItems.length === 0) {
                html = '<li class="list-group-item text-center">Cart is empty.</li>';
            } else {
                cartItems.forEach(item => {
                    html += `
                        <li class="list-group-item d-flex justify-content-between align-items-center">
                            <div>
                                <small>${item.name}</small><br>
                                <small class="text-muted">Qty: ${item.quantity}</small>
                            </div>
                            <span>Kshs ${(item.price * item.quantity).toFixed(2)}</span>
                        </li>`;
                });
            }

            $('#sticky-cart-items').html(html);
            $('#sticky-cart-total').text(`Kshs ${total.toFixed(2)}`);
        });
    }

    // Add to cart handler (event delegation for dynamic elements)
    $(document).on('click', '.add-to-cart', function () {
        const productId = $(this).data('id');
        const quantity = $(this).data('quantity') || 1;

        $.ajax({
            type: 'POST',
            url: '/cart/add',
            contentType: 'application/json',
            data: JSON.stringify({ product_id: productId, quantity }),
            success: function (response) {
                updateCartCount(response.cart_count || 0);
		updateCartTotal(response.total || 0);
                loadStickyCart();

                $('#toast-message').text(response.message || 'Item added to cart');
                new bootstrap.Toast(document.getElementById('cart-toast')).show();
            },
            error: function (xhr) {
                $('#toast-message').text(xhr.responseJSON?.error || 'An error occurred.');
                new bootstrap.Toast(document.getElementById('cart-toast')).show();
            }
        });
    });

    // Initial load
    $.get('/cart/count', function (data) {
	updateCartCount(data.cart ? data.cart.length : 0);
	updateCartTotal(data.total || 0);
    });

    loadStickyCart();
});
