document.addEventListener('DOMContentLoaded', function() {
    // URL of the Flask server endpoint
    const url = '/getresult';

    // Fetch data from the server
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const statsContainer = document.getElementById('statscontainer');

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
        .catch(error => console.error('Error fetching data:', error));
});