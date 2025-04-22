document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const searchForm = document.getElementById("searchForm");
    const suggestionsBox = document.getElementById("searchSuggestions");

    let debounceTimer;
    let activeIndex = -1; // Track selected suggestion

    // 🔍 Handle input typing for suggestions
    searchInput.addEventListener("input", function () {
        const query = this.value.trim();

        clearTimeout(debounceTimer);
        if (!query) {
            suggestionsBox.innerHTML = "";
            suggestionsBox.style.display = "none";
            activeIndex = -1;
            return;
        }

        debounceTimer = setTimeout(() => {
            fetch(`/search/suggest?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsBox.innerHTML = "";
                    activeIndex = -1;

                    if (data.length === 0) {
                        suggestionsBox.style.display = "none";
                        return;
                    }

                    data.forEach(product => {
                        const item = document.createElement("a");
                        item.classList.add("list-group-item", "list-group-item-action", "d-flex", "align-items-center");
                        item.href = `/products/${product.id}`;
                        item.tabIndex = -1; // prevent tab stop

                        const img = document.createElement("img");
                        img.src = product.image_url;
                        img.alt = product.name;
                        img.classList.add("me-2");
                        img.style.width = "40px";
                        img.style.height = "40px";
                        img.style.objectFit = "cover";
                        img.style.borderRadius = "5px";

                        const text = document.createElement("span");
                        text.textContent = product.name;

                        item.appendChild(img);
                        item.appendChild(text);
                        suggestionsBox.appendChild(item);
                    });

                    suggestionsBox.style.display = "block";
                })
                .catch(err => {
                    console.error("Suggest error:", err);
                });
        }, 300);
    });

    // 🧠 Handle form submission (Enter key or button click)
    searchForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const query = searchInput.value.trim();
        if (query) {
            window.location.href = `/search?q=${encodeURIComponent(query)}`;
        }
    });

    // 👀 Hide suggestions if user clicks outside
    document.addEventListener("click", function (e) {
        if (!suggestionsBox.contains(e.target) && e.target !== searchInput) {
            suggestionsBox.style.display = "none";
        }
    });

    // ⌨️ Keyboard navigation
    searchInput.addEventListener("keydown", function (e) {
        const items = Array.from(suggestionsBox.querySelectorAll("a"));

        if (suggestionsBox.style.display === "none" || items.length === 0) return;

        if (e.key === "ArrowDown") {
            e.preventDefault();
            activeIndex = (activeIndex + 1) % items.length;
            updateActiveSuggestion(items);
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            activeIndex = (activeIndex - 1 + items.length) % items.length;
            updateActiveSuggestion(items);
        } else if (e.key === "Enter") {
            if (activeIndex >= 0 && activeIndex < items.length) {
                window.location.href = items[activeIndex].href;
                suggestionsBox.style.display = "none";
                e.preventDefault();
            }
        }
    });

    function updateActiveSuggestion(items) {
        items.forEach((item, index) => {
            if (index === activeIndex) {
                item.classList.add("active");
                item.scrollIntoView({ block: "nearest" });
            } else {
                item.classList.remove("active");
            }
        });
    }
});
