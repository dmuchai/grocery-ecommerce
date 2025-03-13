document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function () {
            let productId = this.getAttribute("data-id");

            fetch("/cart", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: 1, product_id: productId, quantity: 1 })
            })
            .then(response => response.json())
            .then(data => alert("Added to cart!"))
            .catch(error => console.error("Error:", error));
        });
    });
});
