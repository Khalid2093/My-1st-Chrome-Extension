document.addEventListener("DOMContentLoaded", function () {
  fetchProfileNames();
  document
    .getElementById("profileSelector")
    .addEventListener("change", function () {
      const selectedProfile = this.value;
      fetchAge(selectedProfile);
    });
});

function fetchProfileNames() {
  fetch("http://127.0.0.1:5000/profiles")
    .then((response) => response.json())
    .then((data) => {
      const dropdown = document.getElementById("profileSelector");
      data.forEach((profile) => {
        const option = document.createElement("option");
        option.value = profile.name;
        option.text = profile.name;
        dropdown.appendChild(option);
      });
    })
    .catch((error) => console.error("Error fetching profiles:", error));
}

function fetchAge(profileName) {
  fetch(`http://127.0.0.1:5000/age?name=${profileName}`)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById(
        "ageResult"
      ).textContent = `Approximate Age: ${data.age}`;
    })
    .catch((error) => console.error("Error fetching age:", error));
}
