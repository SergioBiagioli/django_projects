document.querySelectorAll(".auto-row").forEach(function(row) {
    row.addEventListener("click", function() {
    window.location = row.dataset.href;
    });
});

function initTableScroll() {
    const tableWrapper = document.querySelector('.table-responsive');
    tableWrapper.addEventListener('scroll', function() {
    if (tableWrapper.scrollTop + tableWrapper.clientHeight >= tableWrapper.scrollHeight) {
        console.log("Reached the end of the table, loading more data...");
        loadMoreData();
    }
    });
}

let offset = 10;

function loadMoreData() {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', '{% url "vehicles:load_more_aplications" %}?offset=' + offset);
    xhr.onload = function() {
    if (xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
        document.querySelector('#table-body').insertAdjacentHTML('beforeend', response.html);
        offset += 10;
    } else {
        console.error('Failed to load more data:', xhr.statusText);
    }
    };
    xhr.onerror = function() {
    console.error('Error loading more data.');
    };
    xhr.send();
}



function searchAplications(query) {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', '{% url "vehicles:search_aplications" %}?q=' + encodeURIComponent(query));
    xhr.onload = function() {
    if (xhr.status === 200) {
        console.log('Search results received.');
        const response = JSON.parse(xhr.responseText);
        document.querySelector('#table-body').innerHTML = response.html;
    } else {
        console.error('Failed to fetch search results:', xhr.statusText);
    }
    };
    xhr.onerror = function() {
    console.error('Error fetching search results.');
    };
    xhr.send();
}

