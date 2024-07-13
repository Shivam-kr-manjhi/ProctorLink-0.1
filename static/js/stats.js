document.addEventListener('DOMContentLoaded', function() {
    let stat = document.getElementById("points");
    fetch('/getstats')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Array of strings:', data);
            stat.textContent=data[0];
            // You can process the array of strings here
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
});
