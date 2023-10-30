document.addEventListener("DOMContentLoaded", function () {
    const dataEntry1 = document.getElementById("data-entry-1");
    const dataName1 = document.getElementById("data-name-1");
    const dataValue1 = document.getElementById("data-value-1");
    const dataImage1 = document.getElementById("data-image-1");

    const dataEntry2 = document.getElementById("data-entry-2");
    const dataName2 = document.getElementById("data-name-2");
    const dataValue2 = document.getElementById("data-value-2");
    const dataImage2 = document.getElementById("data-image-2");

    const message = document.getElementById("message");
    const guessButton = document.getElementById("guess-button");

    // Function to load a new set of data entries
    function loadNewDataEntries() {
        fetch("/random")
            .then(response => response.json())
            .then(data => {
                dataName1.textContent = data.name;
                dataValue1.textContent = data.value;
                dataImage1.src = data.image_url;

                fetch("/random")
                    .then(response => response.json())
                    .then(data => {
                        dataName2.textContent = data.name;
                        dataValue2.textContent = data.value;
                        dataImage2.src = data.image_url;
                    });
            });
    }

    // Function to check if the user's guess is correct
    function checkGuess() {
        fetch("/correct?id1=0&id2=1&id_guess=0") // Replace with actual URL and parameters
            .then(response => response.json())
            .then(result => {
                if (result) {
                    message.textContent = "Correct! You guessed correctly.";
                } else {
                    message.textContent = "Wrong guess. Try again!";
                }

                // Load new data entries after a brief delay
                setTimeout(() => {
                    loadNewDataEntries();
                    message.textContent = "Which data entry is higher?";
                }, 2000);
            });
    }

    // Event listener for the guess button
    guessButton.addEventListener("click", checkGuess);

    // Initial data loading when the page loads
    loadNewDataEntries();
});
