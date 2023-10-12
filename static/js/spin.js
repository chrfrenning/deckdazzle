let currentIndex = 0;
let interval;
let spinning = false;
let fileNamesData;
let fileNames;

function noPresentations() {
    const container = document.getElementById("container");
    container.textContent = "No presentations to spin";
}

function startSpinning() {
    if (!spinning) {
        fileNamesData = document.getElementById("fileNames").value;
        fileNames = JSON.parse(fileNamesData);

        const strippedFileNames = fileNames.map(fileName => {
            if (fileName.endsWith(".pptx")) {
                return fileName.slice(0, -5); // Remove the last 5 characters (".pptx")
            } else {
                return fileName;
            }
        });

        const spinButton = document.getElementById("spinButton");
        spinButton.disabled = true;

        const min = 3000;
        const max = 4000;
        const randomValue = Math.floor(Math.random() * (max - min + 1)) + min;
        let spinDuration = randomValue; // Adjust this value to control spin duration (in milliseconds).

        function spin() {
            interval = setInterval(displayNextFileName, 100);
        }

        function displayNextFileName() {
            document.getElementById("container").textContent = fileNames[currentIndex];
            currentIndex++;
            if (currentIndex >= fileNames.length) {
                currentIndex = 0;
            }
        }

        // Randomly stop after the spin duration
        setTimeout(stopSpinning, spinDuration);

        function stopSpinning() {
            clearInterval(interval);
            spinButton.disabled = false;
            chosenFileName = fileNames[currentIndex];

            // Remove the chosen file name from the list
            fileNames.splice(currentIndex, 1);

            // Update the hidden input value with the modified fileNames array
            document.getElementById("fileNames").value = JSON.stringify(fileNames);

            // Create a link for the chosen file and make it clickable
            const presentationLink = document.createElement("a");
            presentationLink.href = `/presentations/${chosenFileName.endsWith(".pptx") ? chosenFileName.slice(0, -5) : chosenFileName}/download`;
            presentationLink.textContent = chosenFileName;
            presentationLink.style.cursor = "pointer"; 

            // Get the "container" element by its ID
            const container = document.getElementById("container");

            // Remove existing content in the "container" and append the link
            container.innerHTML = '';
            container.appendChild(presentationLink);
            
            const fileItems = document.querySelectorAll(".file-item");
            fileItems.forEach((fileItem) => {
                if (fileItem.textContent === chosenFileName) {
                    fileItem.classList.add("chosen-file");
                }
            });
            
            // Send a request to delete the chosen file on the server
            fetch('/delete_file', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ chosenFileName: chosenFileName }),
            })
            .then(response => {
                if (response.status === 200) {
                    console.log('File ' + chosenFileName + ' deleted successfully');
                } else if (response.status === 404) {
                    console.error('File not found');
                } else {
                    console.error('Error:', response.statusText);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });

            spinning = false;
        }

        spin();
        spinning = true;
    }
}
