let map;

// ================= ADD FOOD =================
function addFood() {

    let name = document.getElementById("name").value;
    let quantity = document.getElementById("quantity").value;
    let location = document.getElementById("location").value;
    let expiry = document.getElementById("expiry").value;

    if (!name || !quantity || !location || !expiry) {
        alert("⚠️ Please fill all fields");
        return;
    }

    fetch("http://127.0.0.1:5000/add_food", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, quantity, location, expiry })
    
    })
    .then(res => res.json())
    .then(data => {
        alert("✅ " + data.message);
        getFood();
    })
    .catch(err => console.error(err));
    let foodLocaion = document.getElementById("location").value; }


// ================= GET FOOD =================
function getFood() {

    fetch("http://127.0.0.1:5000/get_food")
    .then(res => res.json())
    .then(data => {

        let table = document.getElementById("foodTable");
        if (!table) return;

        table.innerHTML = "";

        data.forEach(food => {
            table.innerHTML += `
            <tr>
                <td>${food.name}</td>
                <td>${food.quantity}</td>
                <td>${food.location}</td>
                <td>${food.expiry}</td>
                <td><button onclick="requestFood(${food.id})">Request</button></td>
            </tr>`;
        });
    });
}


// ================= FILTER FOOD =================
function filterFood() {

    let filterLocation = document.getElementById("filterLocation").value;

    if (!filterLocation) {
        alert("⚠️ Please enter location");
        return;
    }

    fetch(`http://127.0.0.1:5000/filter_food/${filterLocation}`)
    .then(res => res.json())
    .then(data => {

        let table = document.getElementById("foodTable");
        table.innerHTML = "";

        // Clear old markers
        if (map) {
            map.eachLayer(layer => {
                if (layer instanceof L.Marker) {
                    map.removeLayer(layer);
                }
            });
        }

        if (data.length === 0) {
            table.innerHTML = `<tr><td colspan="5">No food found 😔</td></tr>`;
            return;
        }

        data.forEach(food => {

            // Add to table
            table.innerHTML += `
            <tr>
                <td>${food.name}</td>
                <td>${food.quantity}</td>
                <td>${food.location}</td>
                <td>${food.expiry}</td>
                <td><button onclick="requestFood(${food.id})">Request</button></td>
            </tr>`;

            // Add marker (temporary Pune fallback if no lat/lng)
            let lat = food.lat || 18.5204;
            let lng = food.lng || 73.8567;

            L.marker([lat, lng])
                .addTo(map)
                .bindPopup(`<b>${food.name}</b><br>${food.location}`);
        });

    })
    .catch(err => console.error(err));
}


// ================= REQUEST FOOD =================
function requestFood(id) {

    fetch("http://127.0.0.1:5000/request_food", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            food_id: id,
            ngo_name: "NGO"
        })
    })
    .then(res => res.json())
    .then(data => alert(data.message));
}


// ================= MAP =================
function initMap() {

    if (typeof L === "undefined") {
        console.error("Leaflet not loaded!");
        return;
    }

    map = L.map('map').setView([18.5204, 73.8567], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);

    loadMarkers();
}


// ================= LOAD MARKERS =================
function loadMarkers() {

    fetch("http://127.0.0.1:5000/get_food")
    .then(res => res.json())
    .then(data => {

        data.forEach(food => {

            // TEMP FIX: default coordinates (Pune)
            let lat = 18.5204;
            let lng = 73.8567;

            L.marker([lat, lng])
            .addTo(map)
            .bindPopup(`
                <b>${food.name}</b><br>
                Qty: ${food.quantity}<br>
                ${food.location}
            `);
        });
    });
}


// ================= DELETE / DELIVER =================
async function deliverFood(id) {

    await fetch(`http://127.0.0.1:5000/delete_food/${id}`, {
        method: "DELETE"
    });

    alert("Food Delivered ✅");
    getFood();
}



// ================= AUTO LOAD =================
window.onload = function () {
    if (typeof initMap === "function") initMap();
    getFood();
};

function logout() {
    localStorage.removeItem("role"); // clear session

    alert("Logout successful ✅"); // 👈 success message

    window.location.href = "auth.html"; // redirect to login
}

function getUserLocation() {

    if (navigator.geolocation) {

        navigator.geolocation.getCurrentPosition(function(position) {

            let lat = position.coords.latitude;
            let lng = position.coords.longitude;

            console.log("Lat:", lat, "Lng:", lng);

            // Convert coordinates → readable address
            fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
            .then(res => res.json())
            .then(data => {

                let address = data.display_name;

                // Fill input field automatically
                document.getElementById("location").value = address;

            });

        }, function(error) {
            alert("Location access denied ❌");
        });

    } else {
        alert("Geolocation not supported ❌");
    }
}