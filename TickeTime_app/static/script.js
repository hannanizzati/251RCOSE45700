function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    sidebar.classList.toggle('open');
    overlay.classList.toggle('active');
}

document.getElementById('overlay').addEventListener('click', () => {
    document.getElementById('sidebar').classList.remove('open');
    document.getElementById('overlay').classList.remove('active');
});

function scrollCarousel(direction) {
    const carousel = document.querySelector('.carousel');
    const scrollAmount = 300; // Pixels to scroll

    if (direction === 'left') {
        carousel.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    } else {
        carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
}

// New functionality for the search bar
document.getElementById('search-btn').addEventListener('click', () => {
    const keyword = document.getElementById('search-keyword').value;
    const location = document.getElementById('location-filter').value;
    const date = document.getElementById('date-filter').value;

    // Construct the URL with query parameters
    const url = `/search?keyword=${encodeURIComponent(keyword)}&location=${encodeURIComponent(location)}&date=${encodeURIComponent(date)}`;
    window.location.href = url; // Redirect to the search results
});

// Optional: Add an event listener to reset the location filter if needed
document.getElementById('location-filter').addEventListener('change', (event) => {
    if (!event.target.value) {
        // Handle the case when no location is selected
        console.log("No location selected, showing all locations.");
    }
});

function chooseMyOwnSeats() {
    document.getElementById("seat-map").style.display = "block";
}

function selectSeat(seat) {
    const seatButton = document.querySelector(`[data-seat="${seat}"]`);
    if (seatButton.classList.contains("booked")) {
        alert("This seat is already booked.");
    } else {
        seatButton.classList.toggle("selected");
        alert(`You selected seat: ${seat}`);
    }
}

function pickRandomSeat(url) {
    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(data.error);
            } else {
                alert(`Randomly assigned seat: ${data.seat}`);
                location.reload(); // Reload the page to reflect changes
            }
        })
        .catch((error) => console.error("Error:", error));
}








