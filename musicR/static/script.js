// Get the form element
const form = document.getElementById("spotifyForm");

// Attach an event listener to the form submission
form.addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent the default form submission

  // Get the artist name and song name inputs
  const artistNameInput = document.getElementById("artistName");
  const songNameInput = document.getElementById("songName");

  // Get the values from the inputs
  const artistName = artistNameInput.value;
  const songName = songNameInput.value;

  // Redirect to the recommendations page with the artist name and song name as query parameters
  window.location.href = `/recommendations?artist=${encodeURIComponent(
    artistName
  )}&song=${encodeURIComponent(songName)}`;
});
