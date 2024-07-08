function initSearchTable(data, headers, fields, title, updateUrlTemplate, deleteUrlTemplate) {
    console.log("Initializing search table...");

    const input = document.getElementById('search_here');
    const results = document.getElementById('results');

    console.log("Displaying results...");
    const displayResults = (arr) => {
        let table = `<table class="table table-hover">
                       <thead>
                         <tr>`;
        headers.forEach(header => {
            table += `<th>${header}</th>`;
        });
        table += `<th>Actions</th></tr></thead><tbody>`;

        arr.forEach(obj => {
            let rowClass = '';
            let rowHref = '';
            if (title === 'Aplication') {
                rowClass = 'clickable-row';
                rowHref = `/vehicles/aplication/${obj.id}/`;
            } else if (title === 'Part') {
                rowClass = 'clickable-row';
                rowHref = `/vehicles/part/${obj.id}/`;
            }

            table += `<tr class="${rowClass}" data-href="${rowHref}">`;
            fields.forEach(field => {
                table += `<td class="clickable-cell">${obj[field]}</td>`;
            });
            const updateUrl = updateUrlTemplate.replace('${id}', obj.id);
            const deleteUrl = deleteUrlTemplate.replace('${id}', obj.id);
            table += `<td class="action-buttons">
                        <button type="button" class="btn btn-update btn-sm" data-bs-toggle="modal" data-url="${updateUrl}">Update</button>
                        <button type="button" class="btn btn-delete btn-sm" data-bs-toggle="modal" data-url="${deleteUrl}">Delete</button>
                      </td></tr>`;
        });
        table += `</tbody></table>`;
        results.innerHTML = table;

        console.log("Adding event listeners to rows...");
        const rows = document.querySelectorAll(".clickable-row");
        rows.forEach(row => {
            row.addEventListener("click", (event) => {
                if (!event.target.closest('.action-buttons')) {
                    const href = row.dataset.href;
                    console.log("Row clicked, href:", href);
                    if (href) {
                        window.location.href = href;
                    }
                }
            });
        });

        console.log("Adding event listeners to update buttons...");
        const updateButtons = document.querySelectorAll(".btn-update");
        updateButtons.forEach(button => {
            button.addEventListener("click", (event) => {
                event.preventDefault();
                const url = button.getAttribute('data-url');
                console.log("Update button clicked, URL:", url);
                openUpdateModal(url);
            });
        });

        console.log("Adding event listeners to delete buttons...");
        const deleteButtons = document.querySelectorAll(".btn-delete");
        deleteButtons.forEach(button => {
            button.addEventListener("click", (event) => {
                event.preventDefault();
                const url = button.getAttribute('data-url');
                console.log("Delete button clicked, URL:", url);
                openDeleteModal(url);
            });
        });
    };

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

    // Close modals on Escape key press
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                modalInstance.hide();
            });
        }
    });
}

function openUpdateModal(url) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
            document.getElementById('updateFormContent').innerHTML = html;
            const formElement = document.querySelector('#updateFormTemplate');
            formElement.setAttribute('action', url); // Set the form action to the update URL
            const modal = new bootstrap.Modal(document.getElementById('updateModalTemplate'));
            modal.show();
            initModalForm();  // Initialize form event listener
        });
}

function openDeleteModal(url) {
    const modal = new bootstrap.Modal(document.getElementById('deleteModalTemplate'));
    document.getElementById('deleteFormTemplate').action = url;
    modal.show();
}

function initModalForm() {
    const updateForm = document.getElementById('updateFormTemplate');
    updateForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(updateForm);
        const url = updateForm.getAttribute('action');

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Close modal
                const modal = bootstrap.Modal.getInstance(document.getElementById('updateModalTemplate'));
                modal.hide();
                // Reload table data
                updateTable();
            } else {
                // Replace form content with the new form
                document.getElementById('updateFormContent').innerHTML = data.html_form;
                initModalForm();  // Reinitialize form event listener
            }
        });
    });
}

function updateTable() {
    const url = window.location.href;
    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.text())
    .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newTableBody = doc.getElementById('table-body').innerHTML;
        document.getElementById('table-body').innerHTML = newTableBody;
        initSearchTable(data, headers, fields, title, updateUrlTemplate, deleteUrlTemplate);  // Reinitialize event listeners
    });
}
