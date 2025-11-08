// ---------- DONATE FOOD (register.html) ----------
const donationForm = document.getElementById("donationForm");

if (donationForm) {
  donationForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const phone = document.getElementById("phonenum").value;
    if (phone.length !== 10 || isNaN(phone)) {
      alert("Please enter a valid 10-digit phone number!");
      return;
    }

    const data = {
      donor_name: document.getElementById("donor_name").value,
      food_type: document.querySelector('input[name="food_type"]:checked').value,
      quantity: parseInt(document.getElementById("quantity").value),
      location: document.getElementById("address").value,
      prepared_at: document.getElementById("food_date").value
    };

    try {
      const res = await fetch("http://127.0.0.1:8000/donations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const result = await res.json();
      alert(result.message);
      e.target.reset();
    } catch (error) {
      alert("Failed to connect to server");
      console.error(error);
    }
  });
}


// ---------- RECEIVE FOOD (contact.html) ----------
const donationsContainer = document.getElementById("donationsContainer");

async function loadDonations() {
  try {
    const res = await fetch("http://127.0.0.1:8000/donations");
    const data = await res.json();

    if (data.length === 0) {
      donationsContainer.innerHTML = "<p>No active donations right now.</p>";
      return;
    }

    data.forEach(donation => {
      const card = document.createElement("div");
      card.classList.add("donation-card");
      card.innerHTML = `
        <h3>${donation.donor_name}</h3>
        <p><b>Food:</b> ${donation.food_type}</p>
        <p><b>Quantity:</b> ${donation.quantity} kg</p>
        <p><b>Location:</b> ${donation.location}</p>
        <button class="connect-btn">Connect</button>
      `;
      donationsContainer.appendChild(card);
    });

    // Connect button functionality
    document.querySelectorAll(".connect-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        alert("You can contact this donor via our NGO team!");
      });
    });

  } catch (error) {
    donationsContainer.innerHTML = "<p> Unable to load donations.</p>";
    console.error(error);
  }
}

// Only run this if container exists
if (donationsContainer) loadDonations();

