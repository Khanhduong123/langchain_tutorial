const form = document.getElementById("name-form");
const spinner = document.getElementById("spinner");
const result = document.getElementById("result");

form.addEventListener("submit", (ev) => {
    ev.preventDefault();

    result.style.display = "none";
    spinner.style.display = "block";  // Ensure spinner is displayed

    const formData = new FormData(form);

    fetch("/process", { method: "POST", body: formData })
        .then(response => {
            if (response.ok) return response.json();
            throw new Error("POST request failed");
        })
        .then(data => {
            // Update the profile image and summary
            document.getElementById("profile-pic").src = data.picture_url;
            document.getElementById("summary").textContent = data.summary_and_facts.summary;

            // Create HTML list for facts
            createHtmlList(document.getElementById("facts"), data.summary_and_facts.facts);

            // Create HTML list for ice breakers (uncommented)
            createHtmlList(document.getElementById("ice-breakers"), data.ice_breakers.ice_breakers);

            // Create HTML list for topics of interest (uncommented)
            createHtmlList(document.getElementById("topics-of-interest"), data.interests.topics_of_interest);

            spinner.style.display = "none";
            result.style.display = "block";
        })
        .catch(error => {
            console.error("Error:", error);
            spinner.style.display = "none";
            result.style.display = "block";
        });
});

function createHtmlList(element, items) {
    // Ensure the items is an array and is not undefined
    if (!Array.isArray(items)) {
        element.innerHTML = "<p>No items available.</p>";
        return;
    }

    const ul = document.createElement("ul");

    // Loop through the items and create list elements
    items.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        ul.appendChild(li);
    });

    // Clear previous content and append the new list
    element.innerHTML = "";
    element.appendChild(ul);
}
