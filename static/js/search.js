document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("searchForm").addEventListener("submit", function (event) {
        event.preventDefault();
        const query = document.getElementById("searchInput").value.trim();

        if (query) {
            fetchSearchResults(query, 1);
        }
    });
});

function fetchSearchResults(query, page) {
    const resultsContainer = document.getElementById("searchResults");
    resultsContainer.innerHTML = "<p>Loading...</p>";

    fetch(`/search?q=${query}&page=${page}`)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data);
        })
        .catch(error => {
            console.error("Error:", error);
            resultsContainer.innerHTML = "<p class='text-danger'>An error occurred. Please try again.</p>";
        });
}

function displaySearchResults(data) {
    let resultsContainer = document.getElementById("searchResults");
    resultsContainer.innerHTML = "";

    if (!data.products || data.products.length === 0) {
        resultsContainer.innerHTML = "<p>No products found.</p>";
        return;
    }

    data.products.forEach(product => {
        let imageUrl = product.image_url || "/static/images/default.jpg";
        let productCard = `
            <div class="card mb-3">
                <img src="${imageUrl}" class="card-img-top" alt="${product.name}">
                <div class="card-body">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text">${product.description}</p>
                    <p class="text-success"><strong>Kshs ${parseFloat(product.price).toFixed(2)}</strong></p>
                    <button class="btn btn-success add-to-cart" data-product-id="${product.id}">Add to Cart</button>
                </div>
            </div>
        `;
        resultsContainer.innerHTML += productCard;
    });

    // Attach event listeners to the "Add to Cart" buttons
    document.querySelectorAll(".add-to-cart").forEach(button => {
	button.addEventListener("click", function () {
		let productId = this.getAttribute("data-product-id");
		addToCart(productId, 1); // Default quantity = 1
	});
    });

    if (data.pages > 1) {
        displayPagination(data.q, data.current_page, data.pages);
    }
}

function displayPagination(query, currentPage, totalPages) {
    let paginationContainer = document.getElementById("pagination");
    paginationContainer.innerHTML = "";

    for (let page = 1; page <= totalPages; page++) {
        paginationContainer.innerHTML += `
            <button class="btn btn-outline-primary ${page === currentPage ? 'active' : ''}" onclick="fetchSearchResults('${query}', ${page})">
                ${page}
            </button>
        `;
    }
}

function addToCart(productId, quantity) {
    fetch("/cart/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ product_id: productId, quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Show success or error message
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to add product to cart.");
    });
}
