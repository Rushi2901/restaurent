function AddCartCard(action, itemId, change = 0) {  
    const updateUrl = document.getElementById('cart-container').dataset.updateUrl;

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


    $.ajax({
        type: "POST",
        url: updateUrl,
        headers: {
            "X-CSRFToken": csrfToken
        },
        data: JSON.stringify({
            action: action,
            item_id: itemId,
            change: change
        }),
        contentType: "application/json",
        success: function(response) {
            if (response.success) {
                console.log(response);
                
                // Clear existing cart items
                $('.cart-items').empty();
                
                // Append updated items
                response.items.forEach(item => {
                    $('.cart-items').append(`
                        <div class="cart-item">
                            <img src="${item.image}" alt="" class="cart-item-image">
                            <div class="cart-item-details">
                                <h3>${item.title}</h3>
                                <p>${item.description}</p>
                            </div>
                            <div class="cart-item-price">₹${item.price}</div>
                            <div class="cart-item-qty">
                                <button onclick="AddCartCard('remove', ${item.id}, 1)" class="qty-btn">-</button>
                                <span>${item.quantity}</span>
                                <button onclick="AddCartCard('add', ${item.id}, 1)" class="qty-btn">+</button>
                            </div>
                            <div class="cart-item-total">₹${item.total_price}</div>
                            <button onclick="AddCartCard('delete', ${item.id})" class="remove-item">✖</button>
                        </div>
                    `);
                });

                // Update the total cost
                $('#cart-total').text(`Total Cost: ₹${response.total_cost}`);
            } else {
                alert(response.message); // Show error message
            }
        },
        error: function(xhr, status, error) {
            console.error("AJAX error:", error);
        }
    });
}
