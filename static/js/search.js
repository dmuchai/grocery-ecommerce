document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("searchForm").addEventListener("submit", function (event) {
        event.preventDefault();
        const query = document.getElementById("searchInput").value.trim();

        if (query) {
            fetch(`/search?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    displaySearchResults(data);
                })
                .catch(error => console.error("Error:", error));
        }
    });
});

function displaySearchResults(results) {
    let resultsContainer = document.getElementById("searchResults");
    resultsContainer.innerHTML = "";

    if (results.products.length === 0) {
        resultsContainer.innerHTML = "<p>No products found.</p>";
        return;
    }

    results.products.forEach(product => {
	let imageUrl = product.image_url ? `/static/images/${product.image_url}` : "/static/images/default.jpg";
        let productCard = `
            <div class="card mb-3">
                <img src="${imageUrl}" class="card-img-top" alt="${product.name}">
                <div class="card-body">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text">${product.description}</p>
                    <p class="text-success"><strong>Kshs ${parseFloat(product.price).toFixed(2)}</strong></p>
                    <button class="btn btn-success">Add to Cart</button>
                </div>
            </div>
        `;
        resultsContainer.innerHTML += productCard;
    });
}
