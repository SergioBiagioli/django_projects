function initSearchTable(data, headers, fields, title, updateUrlTemplate, deleteUrlTemplate) {
    const input = document.getElementById('search_here');
    const results = document.getElementById('results');

    const displayResults = (arr) => {
        let table = `<table class="table table-hover">
                       <thead>
                         <tr>`;
        headers.forEach(header => {
            table += `<th>${header}</th>`;
        });
        table += `<th>Actions</th></tr></thead><tbody>`;

        arr.forEach(obj => {
            table += `<tr class="${title === 'Aplication' ? 'clickable-row' : ''}" data-href="${title === 'Aplication' ? `/${title.toLowerCase()}/${obj.id}/` : ''}">`;
            fields.forEach(field => {
                table += `<td>${obj[field]}</td>`;
            });
            const updateUrl = updateUrlTemplate.replace('99999', obj.id);
            const deleteUrl = deleteUrlTemplate.replace('99999', obj.id);
            table += `<td>
                        <a href="${updateUrl}" class="btn btn-update btn-sm">Update</a>
                        <a href="${deleteUrl}" class="btn btn-delete btn-sm">Delete</a>
                      </td></tr>`;
        });
        table += `</tbody></table>`;
        results.innerHTML = table;

        // Añadir el event listener para las filas clickeables
        const rows = document.querySelectorAll(".clickable-row");
        rows.forEach(row => {
            row.addEventListener("click", () => {
                const href = row.dataset.href;
                if (href) {
                    window.location.href = href;
                }
            });
        });
    };

    // Display initial data
    displayResults(data);

    input.addEventListener('keyup', (e) => {
        const value = e.target.value.toLowerCase().trim();
        const words = value.split(/\s+/);

        if (value === "") {
            displayResults(data);
        } else {
            const filteredArr = data.filter(obj => {
                const combinedText = fields.map(field => obj[field].toString().toLowerCase()).join(" ");
                return words.every(word => combinedText.includes(word));
            });
            displayResults(filteredArr);
        }
    });
}
w