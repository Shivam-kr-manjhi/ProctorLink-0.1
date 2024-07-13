document.addEventListener('DOMContentLoaded', function() {
    const url = '/getresult';
    const loading = document.getElementById('loading');
    const statsContainer = document.getElementById('statscontainer');

    // Fetch data from the server
    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Hide the loading indicator
            loading.style.display = 'none';

            // Show the stats container
            statsContainer.style.display = 'flex';

            // Iterate over the dictionary keys and values
            Object.entries(data).forEach(([key, value]) => {
                const statDiv = document.createElement('div');
                statDiv.className = 'stats';

                const resultDiv = document.createElement('div');
                resultDiv.className = 'result';
                resultDiv.textContent = `${value}%`; // Assuming the score is a percentage

                const resultTitleDiv = document.createElement('div');
                resultTitleDiv.className = 'result-title';
                resultTitleDiv.textContent = key;

                statDiv.appendChild(resultDiv);
                statDiv.appendChild(resultTitleDiv);

                statsContainer.appendChild(statDiv);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            loading.textContent = 'Error loading data.';
        });
});