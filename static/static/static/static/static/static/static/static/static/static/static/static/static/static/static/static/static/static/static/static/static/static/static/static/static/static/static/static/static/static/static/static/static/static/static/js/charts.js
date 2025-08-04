document.addEventListener("DOMContentLoaded", function () {
    // Reset dropdowns on page load (optional)
    document.getElementById('low-stock-category').selectedIndex = 0;
    document.getElementById('best-seller-category').selectedIndex = 0;

    // Chart instances to avoid duplicate rendering
    let lowChartInstance = null;
    let bestChartInstance = null;

    function updateChart(canvasId, labels, values, label, bgColor, borderColor, type) {
        const ctx = document.getElementById(canvasId).getContext('2d');

        // Destroy previous chart if exists
        if (type === 'low' && lowChartInstance) {
            lowChartInstance.destroy();
        }
        if (type === 'best' && bestChartInstance) {
            bestChartInstance.destroy();
        }

        const newChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: values,
                    backgroundColor: bgColor,
                    borderColor: borderColor,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // Store instance
        if (type === 'low') {
            lowChartInstance = newChart;
        } else {
            bestChartInstance = newChart;
        }
    }

    // Event listener for Low Stock dropdown
    document.getElementById('low-stock-category').addEventListener('change', function () {
        const categoryId = this.value;
        fetch(`/filter-low-stock/?category=${categoryId}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById('low-stock-list').innerHTML = data.html;
                updateChart(
                    'lowStockChart',
                    data.labels,
                    data.values,
                    'Quantity Left',
                    'rgba(255, 99, 132, 0.5)',
                    'rgb(255, 99, 132)',
                    'low'
                );
            });
    });

    // Event listener for Best Seller dropdown
    document.getElementById('best-seller-category').addEventListener('change', function () {
        const categoryId = this.value;
        fetch(`/filter-best-seller/?category=${categoryId}`)
            .then(res => res.json())
            .then(data => {
                document.getElementById('best-seller-list').innerHTML = data.html;
                updateChart(
                    'bestSellerChart',
                    data.labels,
                    data.values,
                    'Sold Pieces',
                    'rgba(54, 162, 235, 0.5)',
                    'rgb(54, 162, 235)',
                    'best'
                );
            });
    });

    // Initial chart rendering using global data from Django context
    updateChart(
        'lowStockChart',
        window.lowLabels,
        window.lowValues,
        'Quantity Left',
        'rgba(255, 99, 132, 0.5)',
        'rgb(255, 99, 132)',
        'low'
    );

    updateChart(
        'bestSellerChart',
        window.bestLabels,
        window.bestValues,
        'Sold Pieces',
        'rgba(54, 162, 235, 0.5)',
        'rgb(54, 162, 235)',
        'best'
    );
});
