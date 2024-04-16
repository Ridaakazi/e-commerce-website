// for cart count button
  $(document).ready(function () {
   
    displayFlashMessages("{{ get_flashed_messages() }}");

    $('.add-to-cart-btn').on('click', function () {
        var productId = $(this).data('id');

        $.ajax({
            url: '/add_to_cart/' + productId,
            method: 'POST',
            success: function (response) {
                displayFlashMessages(response.message);
                $('#cart-count').text(response.cart_count);
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
});
// to display alert flash messages
function displayFlashMessages(messages) {
    // Clear existing messages
    $('#flash-messages-container').empty();

    // Check if messages is defined and not empty
    if (messages && messages.length > 0) {
        messages.forEach(function (message) {
            $('#flash-messages-container').append('<div class="flash-message" role="alert">' + message + '</div>');
        });
    }

}
// for the remove from cart button
   $(document).ready(function () {

        $('.remove-from-cart-btn').click(function () {
            var productId = $(this).closest('form').find('input[name="product_id"]').val();

            // Send an AJAX request to remove one quantity
            $.ajax({
                url: '/remove_one_from_cart/' + productId,
                method: 'POST',
                success: function (response) {
                    alert(response.message);
                    location.reload();
                },
                error: function (error) {
                    console.log(error);
                }
            });
        });
    });
    
// add to cart button
    function addToCart(button) {
        var productId = $(button).data('id');
    
        $.ajax({
            url: '/add_to_cart/' + productId,
            method: 'POST',
            success: function(response) {
                alert(response.message);
                $('#cart-count').text(response.cart_count);
            },
            error: function(error) {
                console.log(error);
            }
        });
    }

// add to wishlist button
    function addToWishlist(button) {
        const productId = button.getAttribute('data-id');

        fetch(`/add_to_wishlist/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    // to remove items from the wishlist
    $(document).ready(function () {
        $('.remove-from-wishlist-btn').click(function () {
            var productId = $(this).closest('.remove-from-wishlist-form').data('product-id');
            var cardToRemove = $(this).closest('.col');
    
            // using ajax to remove from wishlist
            $.ajax({
                url: '/remove_from_wishlist/' + productId,
                method: 'POST',
                success: function (response) {
                    if (response && response.message) {
                        alert(response.message);
                        cardToRemove.remove();
                    } else {
                        console.error('Invalid response format:', response);
                    }
                },
                error: function (error) {
                    console.error('Error:', error);
                }
            });
        });
    });
    
    
    function redirectToCart() {

        window.location.href = "{{ url_for('cart') }}";
    }


        $(document).on('click', '.remove-from-cart-btn', function (event) {
            event.preventDefault();

            var productId = $(this).closest('form').find('input[name="product_id"]').val();

            $.ajax({
                url: '/remove_one_from_cart/' + productId,
                method: 'POST',
                success: function (response) {
                    console.log(response); 
                    window.location.href = '/cart';
                },
                error: function (error) {
                    console.log(error);
                }
            });
        });

//to add in the cart page
        $(document).on('click', '.add-to-cart-btn', function (event) {
            event.preventDefault();

            var productId = $(this).closest('form').find('input[name="product_id"]').val();

            $.ajax({
                url: '/add_to_cart/' + productId,
                method: 'POST',
                success: function (response) {

                    window.location.href = '/cart';
                },
                error: function (error) {
                    console.log(error);
                }
            });
        });
  

