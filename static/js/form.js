const presentationNameInput = document.querySelector("form input");
const formSubmitButton = document.querySelector("form button");
document.querySelector("form").addEventListener("submit", createPresentation);

function onFormInput(el) {
  if (el.value.length > 0) {
    formSubmitButton.removeAttribute("disabled");
  } else {
    formSubmitButton.setAttribute("disabled", "disabled");
  }
}

// function that sends a POST request to /create-presentation?q= with the content of the input field
function createPresentation(event) {
  event.preventDefault();
  const presentationName = presentationNameInput.value;

  if (presentationName.length < 1) {
    console.error("missing input");
    return;
  }

  presentationNameInput.value = "";

  const data = { presentationName: presentationName };
  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  };
  fetch("/create-presentation?q=" + presentationName, options)
    .then((response) => response.json())
    .then((data) => console.log(data));
}
