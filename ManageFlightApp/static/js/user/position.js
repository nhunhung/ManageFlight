document.addEventListener('DOMContentLoaded', function () {
    // Load click events for seat icons
    loadOnClick();

    // Hide certain elements on page load
    hideBusi();

    // Add click event for the button toggle details
    {% for f in flights %}
        var btnToggleDetails{{ f.id }} = document.getElementById('btnToggleDetails{{ f.id }}');
        var collapseExample{{ f.id }} = document.getElementById('collapseExample{{ f.id }}');

        btnToggleDetails{{ f.id }}.addEventListener('click', function () {
            // Toggle the visibility of the collapse element
            if (collapseExample{{ f.id }}.classList.contains('show')) {
                collapseExample{{ f.id }}.classList.remove('show');
            } else {
                collapseExample{{ f.id }}.classList.add('show');
            }
        });
    {% endfor %}
});

// Function to handle seat icon clicks
function loadOnClick() {
    var listSeat = document.getElementsByClassName('seat-icon-check');

    for (const seat of listSeat) {
        seat.addEventListener("click", function () {
            if (seat.classList.contains("seat-icon-disable")) {
                return;
            }

            if (seat.classList.contains("seat-icon-empty")) {
                seat.classList.remove("seat-icon-empty");
                seat.classList.add("seat-icon-select");
                toList(seat.getAttribute("value"), 1);
                return;
            }

            if (seat.classList.contains("seat-icon-select")) {
                seat.classList.remove("seat-icon-select");
                seat.classList.add("seat-icon-empty");
                toList(seat.getAttribute("value"), 2);
                return;
            }
        });
    }
}

// Function to hide certain elements
function hideBusi() {
    document.getElementById("busi-seat").style.display = "none";
    document.getElementById("dex-seat").style.display = "none";
    document.getElementById("eco-seat").style.display = "none";
    document.getElementById("info-pick").style.display = "none";
}

// Function to show additional content based on type
function showAdd() {
    if (document.getElementById("type").value == '2') {
        document.getElementById("eco-seat").style.display = "flex";
    }
}

// Function to send data to server
function sendDataToServer() {
    fetch("/enter_flight_detail", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json;charset=UTF-8'
        },
        body: JSON.stringify({ seatArr: seatArr, price: price })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Data sent successfully");
    })
    .catch(error => {
        console.error("Error sending data: ", error);
    });
}

// Example data
var jsonData = {
    seat: 'seatArr',
    price: 'price'
};

function pos(id, name, status) {
    event.preventDefault();
    fetch("/api/info", {
        method: "POST",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "status": status
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        // Handle the response data if needed
    })
    .catch(error => {
        console.error("Error in POST request: ", error);
    });
}

