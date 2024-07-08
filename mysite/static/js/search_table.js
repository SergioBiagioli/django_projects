function initSearchTable(data, headers, fields, title) {
    console.log(data);

    const input = document.getElementById('search_here');
    const results = document.getElementById('results');
    console.log(input);

    let filteredArr = [];

    const displayResults = (arr) => {
        let table = `<table class="table table-hover">
                       <thead>
                         <tr>`;
        headers.forEach(header => {
            table += `<th>${header}</th>`;
        });
        table += `<th>Actions</th>
                   </tr>
                 </thead>
                 <tbody>`;
        arr.forEach(obj => {
            table += `<tr>`;
            fields.forEach(field => {
                table += `<td>${obj[field]}</td>`;
            });
            table += `<td>
                        <a href="/vehicles/${title.toLowerCase()}/${obj.id}/update/">Update</a> |
                        <a href="/vehicles/${title.toLowerCase()}/${obj.id}/delete/">Delete</a>
                      </td>
                    </tr>`;
        });
        table += `</tbody></table>`;
        results.innerHTML = table;
    };

    // Display initial data
    displayResults(data);

    input.addEventListener('keyup', (e) => {
        const value = e.target.value.toLowerCase().trim();
        const words = value.split(/\s+/); // Divide la entrada en palabras separadas por espacios

        if (value === "") {
            displayResults(data);
        } else {
            filteredArr = data.filter(obj => {
                const combinedText = fields.map(field => obj[field].toString().toLowerCase()).join(' ');
                // Verifica que cada palabra de la entrada esté en el texto combinado
                return words.every(word => combinedText.includes(word));
            });
            console.log(filteredArr);
            displayResults(filteredArr);
        }
    });
}
