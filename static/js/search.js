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
    const resultsContainer = document.getElementById("searchResults");
    resultsContainer.innerHTML = "";

    if (!data.products || data.products.length === 0) {
        resultsContainer.innerHTML = `
            <p class="text-danger mt-4">No results found for "<strong>${data.q}</strong>".</p>
        `;
        return;
    }

    // Add heading
    const heading = document.createElement("h5");
    heading.className = "mt-4 mb-3";
    heading.innerHTML = `Search Results for <span class="text-white">"${data.q}"</span>`;
    resultsContainer.appendChild(heading);

    // Create a row container for product cards
    const row = document.createElement("div");
    row.className = "row justify-content-center";

    data.products.forEach(product => {
        const col = document.createElement("div");
        col.className = "col-md-4 mb-4";

        const imageUrl = product.image_url || "/static/images/default.jpg";

        col.innerHTML = `
            <div class="card h-100">
                <a href="/products/${product.id}">
                    <img src="${imageUrl}" class="card-img-top" alt="${product.name}">
                </a>
                <div class="card-body d-flex flex-column">
                    <a href="/products/${product.id}" class="text-decoration-none text-dark">
                        <h5 class="card-title">${product.name}</h5>
                    </a>
                    <p class="card-text">${product.description}</p>
                    <p class="text-success"><strong>Kshs ${parseFloat(product.price).toFixed(2)}</strong></p>
                    <a href="/products/${product.id}" class="btn btn-outline-primary mt-auto mb-2">View Product</a>
                    <button class="btn btn-success mt-auto add-to-cart" data-product-id="${product.id}">Add to Cart</button>
                </div>
            </div>
        `;

        row.appendChild(col);
    });

    resultsContainer.appendChild(row);

    // Attach event listeners to the "Add to Cart" buttons
    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", function () {
            const productId = this.getAttribute("data-product-id");
            addToCart(productId, 1); // Default quantity = 1
        });
    });

    if (data.pages > 1) {
        displayPagination(data.q, data.current_page, data.pages);
    }
}

function displayPagination(query, currentPage, totalPages) {
    const paginationContainer = document.getElementById("pagination");
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
