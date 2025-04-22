$(document).ready(function () {
    let autoCloseTimer;

    // 1. Add to cart handler
    $('.add-to-cart').on('click', function () {
        const productId = $(this).data('id');
        const quantity = 1;

        $.ajax({
            type: 'POST',
            url: '/cart/add',
            contentType: 'application/json',
            data: JSON.stringify({ product_id: productId, quantity: quantity }),
            success: function (response) {
                updateCartCount(response.cart_count || 0);
                loadMiniCart();

                if (response.cart_count > 0) {
                    $('#toast-message').text(response.message || 'Item added to cart');
                    $('.toast-container').show();
                    new bootstrap.Toast(document.getElementById('cart-toast')).show();
                } else {
                    $('.toast-container').hide();
                }
            },
            error: function (xhr) {
                $('#toast-message').text(xhr.responseJSON?.error || 'An error occurred.');
                $('.toast-container').show();
                new bootstrap.Toast(document.getElementById('cart-toast')).show();
            }
        });
    });

    // 2. Fetch & render mini-cart
    function loadMiniCart() {
        $.get('/cart', function (data) {
            const cartItems = data.cart || [];
            const total = data.total || 0;
            let html = '';

            if (cartItems.length === 0) {
                $('.toast-container').hide();
                html = '<li class="list-group-item text-center">Cart is empty.</li>';
            } else {
                $('.toast-container').show();
                cartItems.forEach(item => {
                    html += `
                        <li class="list-group-item d-flex justify-content-between align-items-start">
                            <div>
                                <small>${item.name}</small><br>
                                <small class="text-muted">Qty: ${item.quantity}</small>
                            </div>
                            <div class="d-flex flex-column align-items-end">
                                <span>Kshs ${(item.price * item.quantity).toFixed(2)}</span>
                                <button class="btn btn-sm btn-link text-danger p-0 remove-from-cart" data-id="${item.id}">Remove</button>
                            </div>
                        </li>`;
                });
            }

            $('#mini-cart-items').html(html);
            $('#mini-cart-total').text(`Kshs ${total.toFixed(2)}`);
            $('#mini-cart').fadeIn();

            clearTimeout(autoCloseTimer);
            autoCloseTimer = setTimeout(() => {
                $('#mini-cart').fadeOut();
            }, 5000);
        });
    }

    // 3. Remove item from cart handler
    $('#mini-cart-items').on('click', '.remove-from-cart', function () {
        const productId = $(this).data('id');

        $.ajax({
            type: 'POST',
            url: `/cart/remove/${productId}`,
            success: function (response) {
                if (response.cart_count !== undefined) {
                    updateCartCount(response.cart_count);
                }
                loadMiniCart();
            },
            error: function () {
                alert('Could not remove item from cart.');
            }
        });
    });

    // 4. Manual close of mini-cart
    $('#close-mini-cart').on('click', function () {
        $('#mini-cart').fadeOut();
        clearTimeout(autoCloseTimer);
    });

    // 5. Update cart count badge
    function updateCartCount(count) {
        const cartBadge = $('#cart-count');

        if (count > 0) {
            cartBadge.text(count).show();
        } else {
            cartBadge.hide();
        }
    }

    // 6. Initial load: cart count
    $.get('/cart/count', function (data) {
        if (data.cart_count !== undefined) {
            updateCartCount(data.cart_count);
        }
    });

    // 7. Initial load: mini-cart content
    loadMiniCart();
});
