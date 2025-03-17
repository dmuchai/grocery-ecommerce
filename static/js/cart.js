document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function () {
            let productId = this.getAttribute("data-id");

            fetch("/cart/add", {  // ✅ Fix endpoint to "/cart/add"
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ product_id: productId, quantity: 1 })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert("Error: " + data.error);
                } else {
                    alert(data.message);  // ✅ Show success message
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
