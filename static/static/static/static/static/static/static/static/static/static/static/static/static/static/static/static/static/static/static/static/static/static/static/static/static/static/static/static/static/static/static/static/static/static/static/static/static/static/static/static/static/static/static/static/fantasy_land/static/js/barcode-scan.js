document.addEventListener('DOMContentLoaded', () => {
    const barcodeInput = document.getElementById('barcodeInput');
    const saleTableBody = document.querySelector('#saleTable tbody');
    const totalAmountDiv = document.getElementById('totalAmount');
    const saleProducts = new Map();

    function updateTable() {
        saleTableBody.innerHTML = '';
        let total = 0;

        saleProducts.forEach(({ name, price, qty, subtotal }, id) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><button class="delete-btn" data-id="${id}">❌</button></td>
                <td>${name}</td>
                <td>${price.toFixed(2)}</td>
                <td>${qty}</td>
                <td>${subtotal.toFixed(2)}</td>
            `;
            saleTableBody.appendChild(row);
            total += subtotal;
        });

        document.querySelectorAll('.delete-btn').forEach(button => {
            button.addEventListener('click', (e) => {
                const idToDelete = parseInt(e.target.getAttribute('data-id'), 10);
                saleProducts.delete(idToDelete);
                updateTable();
            });
        });

        totalAmountDiv.textContent = `Total: ${total.toFixed(2)} DT`;
    }

    let barcodeTimer = null;

    barcodeInput.addEventListener('input', () => {
        clearTimeout(barcodeTimer);

        barcodeTimer = setTimeout(() => {
            const barcode = barcodeInput.value.trim();
            if (!barcode) return;

            fetch(`/sales/ajax/get-product/?barcode=${encodeURIComponent(barcode)}`)
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        showQuantityModal(`Enter quantity for "${data.name}"`).then(quantity => {
                            if (quantity === null || isNaN(quantity) || quantity <= 0) {
                                showAlert("Invalid quantity entered.");
                                barcodeInput.focus();
                                return;
                            }

                            const id = data.id;
                            if (saleProducts.has(id)) {
                                let product = saleProducts.get(id);
                                product.qty += quantity;
                                product.subtotal = product.price * product.qty;
                                saleProducts.set(id, product);
                            } else {
                                saleProducts.set(id, {
                                    name: data.name,
                                    price: data.price,
                                    qty: quantity,
                                    subtotal: data.price * quantity,
                                });
                            }
                            updateTable();
                            barcodeInput.focus();
                        });
                    } else {
                        showAlert(data.error);
                        barcodeInput.focus();
                    }
                })
                .catch(() => {
                    showAlert('Error fetching product info.');
                    barcodeInput.focus();
                });

            barcodeInput.value = '';
        }, 1000);
    });

    document.getElementById('confirmSaleBtn').addEventListener('click', () => {
        if (saleProducts.size === 0) {
            showAlert("No products to confirm.");
            return;
        }

        showModal("Are you sure you want to confirm this sale?")
            .then(confirmed => {
                if (!confirmed) return;

                const saleData = Array.from(saleProducts.entries()).map(([id, data]) => ({
                    id: id,
                    qty: data.qty
                }));

                fetch('/sales/ajax/confirm-sale/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ products: saleData })
                })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) {
                            showAlert("Sale confirmed successfully!");
                            saleProducts.clear();
                            updateTable();
                            window.open(`/sales/receipt/${data.sale_id}/`, '_blank');
                            barcodeInput.focus();
                        } else {
                            showAlert("Error: " + data.error);
                            barcodeInput.focus();
                        }
                    })
                    .catch(() => {
                        showAlert("Something went wrong. Please try again.");
                        barcodeInput.focus();
                    });
            });
    });

    function getCSRFToken() {
        return document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken'))
            ?.split('=')[1];
    }

    function showModal(message) {
        return new Promise((resolve) => {
            const modal = document.getElementById('customModal');
            const msg = document.getElementById('modalMessage');
            const cancelBtn = document.getElementById('modalCancel');
            const confirmBtn = document.getElementById('modalConfirm');

            msg.innerHTML = `<p style="font-size: 1.1rem;">${message}</p>`;
            modal.style.display = 'flex';

            cancelBtn.style.display = '';
            confirmBtn.textContent = 'Confirm';

            cancelBtn.onclick = () => {
                modal.style.display = 'none';
                resolve(false);
                barcodeInput.focus();
            };
            confirmBtn.onclick = () => {
                modal.style.display = 'none';
                resolve(true);
                barcodeInput.focus();
            };

            confirmBtn.focus();
        });
    }

    function showAlert(message) {
        const modal = document.getElementById('customModal');
        const msg = document.getElementById('modalMessage');
        const cancelBtn = document.getElementById('modalCancel');
        const confirmBtn = document.getElementById('modalConfirm');

        msg.innerHTML = `<p style="font-size: 1.1rem;">${message}</p>`;
        cancelBtn.style.display = 'none';
        confirmBtn.textContent = 'OK';

        modal.style.display = 'flex';

        confirmBtn.onclick = () => {
            modal.style.display = 'none';
            cancelBtn.style.display = '';
            confirmBtn.textContent = 'Confirm';
            barcodeInput.focus();
        };

        confirmBtn.focus();
    }

    function showQuantityModal(message) {
        return new Promise((resolve) => {
            const modal = document.getElementById('customModal');
            const msg = document.getElementById('modalMessage');
            const cancelBtn = document.getElementById('modalCancel');
            const confirmBtn = document.getElementById('modalConfirm');

            msg.innerHTML = `<p style="font-size: 1.1rem;">${message}</p><input type="number" id="quantityInput" style="margin-top:10px;width:80%;font-size:1.2rem;padding:5px;">`;
            modal.style.display = 'flex';

            cancelBtn.style.display = '';
            confirmBtn.textContent = 'Confirm';

            const quantityInput = document.getElementById('quantityInput');
            quantityInput.focus();

            confirmBtn.onclick = () => {
                const qty = parseInt(quantityInput.value, 10);
                modal.style.display = 'none';
                resolve(qty);
                barcodeInput.focus();
            };

            cancelBtn.onclick = () => {
                modal.style.display = 'none';
                resolve(null);
                barcodeInput.focus();
            };

            quantityInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    confirmBtn.click();
                }
            });
        });
    }
});