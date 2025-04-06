// Load header and footer
document.addEventListener('DOMContentLoaded', function() {
    loadComponent('header-placeholder', 'components/header.html');
    loadComponent('footer-placeholder', 'components/footer.html');
    setupSearch();
});

// Load component function
function loadComponent(elementId, url) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById(elementId).innerHTML = data;
        })
        .catch(error => console.error('Error loading component:', error));
}

// Setup search functionality
function setupSearch() {
    const searchInputs = ['searchInput', 'searchInput2'];
    let debounceTimer;

    searchInputs.forEach(inputId => {
        const input = document.getElementById(inputId);
        if (!input) return;

        input.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            const query = this.value.trim();
            
            if (query.length < 2) {
                document.getElementById('searchResults').innerHTML = `
                    <div class="initial-message text-center text-muted">
                        Start typing to see results...
                    </div>`;
                return;
            }

            // Show loading indicator
            document.getElementById('searchResults').innerHTML = `
                <div class="text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                </div>`;

            // Debounce the search to avoid too many requests
            debounceTimer = setTimeout(() => {
                performSearch(query);
            }, 300);
        });
    });
}

// Perform search
function performSearch(query) {
    const serverUrl = 'http://localhost:8000';
    fetch(`${serverUrl}/search?q=${encodeURIComponent(query)}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mode: 'cors'
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(`Server error: ${text}`);
            });
        }
        return response.json();
    })
    .then(results => {
        displayResults(results);
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('searchResults').innerHTML = `
            <div class="alert alert-danger">
                <h5>Error fetching results:</h5>
                <p>${error.message || 'Please try again'}</p>
                <small>If this error persists, please check if the server is running and the Excel files are properly formatted.</small>
            </div>`;
    });
}

// Display results function
function displayResults(results) {
    const container = document.getElementById('searchResults');
    
    if (!Array.isArray(results)) {
        container.innerHTML = `
            <div class="alert alert-danger">
                Invalid response format from server
            </div>`;
        return;
    }

    if (results.length === 0) {
        container.innerHTML = `
            <div class="alert alert-info">
                No results found. Try a different search term.
            </div>`;
        return;
    }

    let html = '<div class="list-group">';
    results.forEach(item => {
        html += `
            <div class="list-group-item">
                <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">${item['HS Code'] || item['HS Code'] || 'N/A'}</h5>
                </div>
                <p class="mb-1">${item['Description'] || item['Description'] || 'N/A'}</p>
            </div>`;
    });
    html += '</div>';
    
    container.innerHTML = html;
}
