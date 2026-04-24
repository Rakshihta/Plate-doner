// ================= AUTH TOKEN =================
const authToken = localStorage.getItem("token");

// ================= PARSE JWT =================
function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = atob(base64Url);
    return JSON.parse(base64);
  } catch (e) {
    return null;
  }
}

// ================= GLOBAL USER =================
let user = null;


// ================= INIT (RUN AFTER PAGE LOAD) =================
document.addEventListener("DOMContentLoaded", () => {

  console.log("Token:", authToken);

  if (!authToken) {
    console.log("❌ No token found");
    return;
  }

  user = parseJwt(authToken);
  console.log("✅ Parsed user:", user);

  // ================= AUTO-FILL EMAIL =================
  const emailInput = document.getElementById("email");

  if (emailInput && user?.sub) {
    emailInput.value = user.sub;
    console.log("✅ Email autofilled");
  } else {
    console.log("❌ Email not filled");
  }

  // ================= LOAD DONATIONS =================
  if (document.getElementById("donationsContainer")) {
    loadDonations();
  }
});


// ================= DONATE FOOD =================
const donationForm = document.getElementById("donationForm");

if (donationForm) {
  donationForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!user || !user.sub) {
      alert("User not logged in properly");
      return;
    }

    const phone = document.getElementById("phonenum").value;

    if (phone.length !== 10 || isNaN(phone)) {
      alert("Enter valid 10-digit phone number");
      return;
    }

    const foodTypeElement = document.querySelector(
      'input[name="food_type"]:checked'
    );

    if (!foodTypeElement) {
      alert("Select food type");
      return;
    }

    const data = {
      donor_name: document.getElementById("donor_name").value,
      email: user.sub,
      food_type: foodTypeElement.value,
      quantity: parseInt(document.getElementById("quantity").value),
      location: document.getElementById("address").value,
      prepared_at: document.getElementById("food_date").value
    };

    try {
      const res = await fetch("https://plate-doner.onrender.com/donations/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${authToken}`
        },
        body: JSON.stringify(data)
      });

      const result = await res.json();

      if (res.ok) {
        alert("🎉 Donation added successfully!");

        e.target.reset();

        // 🔥 refill email after reset
        const emailInput = document.getElementById("email");
        if (emailInput && user?.sub) {
          emailInput.value = user.sub;
        }

      } else {
        alert(result.detail || "Failed to add donation");
      }

    } catch (error) {
      console.error(error);
      alert("Server error");
    }
  });
}


// ================= RECEIVE FOOD =================
const donationsContainer = document.getElementById("donationsContainer");

async function loadDonations() {
  try {
    const res = await fetch(
      `https://plate-doner.onrender.com/donations/?email=${user?.sub}`,
      {
        headers: {
          "Authorization": `Bearer ${authToken}`
        }
      }
    );

    const data = await res.json();

    if (!Array.isArray(data) || data.length === 0) {
      donationsContainer.innerHTML = `
        <div class="no-data">
          <h3>🚀 No Donations Yet</h3>
          <p>Be the first to donate food and help someone today!</p>
        </div>
      `;
      return;
    }

    donationsContainer.innerHTML = "";

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

  } catch (error) {
    console.error(error);
    donationsContainer.innerHTML = "<p>Error loading donations</p>";
  }
}


// ================= LOGIN =================
const loginForm = document.getElementById("loginForm");

if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      email: document.getElementById("email").value,
      password: document.getElementById("password").value
    };

    try {
      const res = await fetch("https://plate-doner.onrender.com/users/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const result = await res.json();

      if (result.access_token) {
        localStorage.setItem("token", result.access_token);
        alert("Login successful");
        window.location.href = "index.html";
      } else {
        alert(result.detail || "Login failed");
      }

    } catch (error) {
      alert("Server error during login");
    }
  });
}


// ================= GOOGLE LOGIN =================
function googleLogin() {
  window.location.href = "https://plate-doner.onrender.com/auth/login";
}


// ================= HANDLE GOOGLE TOKEN =================
const params = new URLSearchParams(window.location.search);
const googleToken = params.get("token");

if (googleToken) {
  localStorage.setItem("token", googleToken);

  alert("Google login successful");

  window.history.replaceState({}, document.title, "index.html");
  window.location.href = "index.html";
}


// ================= LOGOUT =================
function logout() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}
