// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", function() {
    // Get the HTML element to display the dynamically changing value
    var dynamicValueElement = document.getElementById("dynamic-value");

    // Function to update the value
    function updateValue(newValue) {
        dynamicValueElement.textContent = newValue;
    }

    // Make an AJAX request to the Python server
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_value", true);
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Parse the JSON response
            var response = JSON.parse(xhr.responseText);

            // Get the value from the response
            var value = response.value;

            // Update the value in the HTML element
            updateValue(value);
        }
    };
    xhr.send();
});
