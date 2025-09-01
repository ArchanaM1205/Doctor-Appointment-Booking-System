#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql,cgi,cgitb,sys
cgitb.enable()
form=cgi.FieldStorage()
con=pymysql.connect(host="localhost",user="root",password="",database="appointment_booking_system")
cur=con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

print("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Doctor Booking</title>
  <link rel="icon" type="image/svg+xml" href="logo.svg" />
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');

    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Outfit', sans-serif;
      background: #fff;
      color: #222;
      padding: 0 120px;
    }

    /* Title Bar */
    .title-bar {
      background: #5f6fff;
      padding: 5px 20px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .title-bar img {
      width: 60px;
      height: 60px;
    }

    /* Navbar */
    .navbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
      background: #fff;
      position: sticky;
      top: 0;
      z-index: 1000;
      border-bottom: 2px solid #000; /* HR line attached */
    }

    .navbar img.logo {
      width: 160px;
      height: 160px;
      cursor: pointer;
    }

    .nav-links {
      display: flex;
      gap: 40px;
      list-style: none;
    }

    .nav-links li {
      position: relative;
    }

    .nav-links a {
      text-decoration: none;
      color: #333;
      font-weight: 500;
      font-size: 0.95rem;
      padding: 10px 5px;
      position: relative;
      transition: color 0.3s ease;
    }

    @media (min-width: 601px) {
      .nav-links a::after {
        content: "";
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 0%;
        height: 2px;
        background: #5f6fff;
        transition: width 0.3s ease;
      }
      .nav-links a:hover {
        color: #5f6fff;
      }
      .nav-links a:hover::after {
        width: 100%;
      }
    }

    .navbar-right {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    /* Dropdown */
    .dropdown {
      position: relative;
    }

    .dropbtn {
      background: #fff;
      border: 2px solid #5f6fff;
      color: #5f6fff;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      padding: 6px 12px;
      border-radius: 20px;
      transition: background 0.2s ease, color 0.2s ease;
    }

    .dropbtn:hover {
      background: #5f6fff;
      color: #fff;
    }

    .dropdown-content {
      display: none;
      position: absolute;
      top: 100%;
      right: 0;
      background: #fff;
      border: 2px solid #5f6fff;
      border-radius: 8px;
      box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.15);
      min-width: 180px;
      opacity: 0;
      transform: translateY(-10px);
      transition: all 0.3s ease-in-out;
      overflow: hidden;
    }

    .dropdown-content.show {
      display: block;
      opacity: 1;
      transform: translateY(0);
    }

    .dropdown-content a {
      display: block;
      padding: 12px 16px;
      text-decoration: none;
      color: #333;
      font-size: 0.9rem;
      background: #fff;
      transition: background 0.3s ease, color 0.3s ease;
    }

    .dropdown-content a:hover {
      background: #5f6fff;
      color: #fff;
    }

    /* Mobile Menu */
    .menu-icon {
      width: 40px;
      cursor: pointer;
      display: none;
    }

    .mobile-menu {
      position: fixed;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100vh;
      background: #fff;
      z-index: 2000;
      padding: 20px;
      transition: left 0.3s ease-in-out;
    }

    .mobile-menu.show {
      left: 0;
    }

    .mobile-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .mobile-header img.logo {
      width: 140px;
      height: 140px;
    }

    .close-icon {
      width: 32px;
      cursor: pointer;
    }

    .mobile-links {
      list-style: none;
      margin-top: 30px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .mobile-links a,
    .mobile-dropdown-btn {
      text-decoration: none;
      color: #333;
      font-size: 1rem;
      font-weight: 500;
      padding: 12px;
      border-radius: 6px;
      transition: background 0.3s ease, color 0.3s ease;
    }

    .mobile-links a:hover,
    .mobile-dropdown-btn:hover {
      background: #5f6fff;
      color: #fff;
    }

    .mobile-dropdown {
      display: none;
      flex-direction: column;
      margin-left: 20px;
      gap: 10px;
    }

    .mobile-dropdown.show {
      display: flex;
    }

    @media (max-width: 992px) {
      .nav-links {
        display: none;
      }
      .navbar-right {
        display: none;
      }
      .menu-icon {
        display: block;
      }
      body {
        padding: 0 40px;
      }
    }

    @media (max-width: 600px) {
      .navbar img.logo {
        width: 140px;
        height: 140px;
      }
      body {
        padding: 0 20px;
      }
    }
/* Header section */
.header {
  background: #5f6fff;
  padding: 2.5rem 1.5rem;
  color: white;
}

.header-container {
  display: flex;
  flex-direction: column-reverse;
  align-items: center;
  justify-content: space-between;
  gap: 2.5rem;
}

.header-left {
  flex: 1;
  text-align: center;
}

.header-title {
  font-size: 2rem;
  font-weight: 600;
  line-height: 1.3;
}

.header-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.group-img {
  width: 7rem;
}

.header-desc {
  font-size: 0.9rem;
  text-align: center;
}

.header-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: #fff;
  color: #5f6fff;
  font-weight: 600;
  padding: 12px 24px;
  border-radius: 9999px;
  text-decoration: none;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  margin-top: 1.5rem;
  transition: all 0.3s ease;
}

.header-btn:hover {
  background: #e5e9ff;
  color: #3d47d6;
}

.btn-arrow {
  width: 16px;
  height: 16px;
}

.header-right {
  flex: 1;
}

.header-img {
  width: 100%;
  max-width: 450px;
  display: block;
  margin: 0 auto;
}

/* Responsive */
@media (min-width: 768px) {
  .header-container {
    flex-direction: row;
  }

  .header-left {
    text-align: left;
  }

  .header-title {
    font-size: 2.5rem;
  }

  .header-group {
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    text-align: left;
  }

  .header-desc {
    font-size: 1rem;
    text-align: left;
  }

  .desktop-only {
    display: inline;
  }
}

@media (max-width: 767px) {
  .desktop-only {
    display: none;
  }
}


/* Header ended */

/* Speciality */

.speciality-section {
  padding: 2rem 1rem;
  text-align: center;
}

.speciality-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.speciality-desc {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
}

.speciality-grid {
  display: flex;
  justify-content: center;
  gap: 1.5rem; /* smaller gap */
  overflow-x: auto;
  padding: 0.5rem 0;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

.speciality-grid::-webkit-scrollbar {
  display: none; /* hide scrollbar */
}

.speciality-item {
  flex: 0 0 auto;
  text-align: center;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.speciality-item:hover {
  transform: scale(1.05);
}

.speciality-img {
  width: 70px;
  height: 70px;
  object-fit: contain;
}

.speciality-item p {
  font-size: 0.9rem;
  margin-top: 5px;
}

@media (min-width: 768px) {
  .speciality-img {
    width: 90px;
    height: 90px;
  }
  .speciality-item p {
    font-size: 1rem;
  }
}


/* Speciality ended */

/* Bannersection */
    .banner {
  position: relative;
  background: #5f6fff;
  margin-top: 4rem;
  padding: 1rem 1.5rem;
  overflow: visible;
}

.banner-container {
  display: flex;
  flex-direction: column-reverse;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
}

.banner-text {
  flex: 1;
  text-align: center;
}

.banner-title {
  font-size: 2rem;
  font-weight: 800;
  color: #fff;
  line-height: 1.3;
}

.banner-btn {
  background: #fff;
  color: #5f6fff;
  padding: 12px 24px;
  border-radius: 50px;
  font-weight: 600;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  margin-top: 1rem;
  transition: all 0.3s ease;
  border: none;
}

.banner-btn:hover {
  background: #e5e9ff;
  color: #3d47d6;
}

.banner-image {
  flex: 1;
  position: relative;
  padding-left: 1rem;
}

.banner-image img {
  width: 100%;
  max-width: 350px;
  margin: 0 auto;
  display: block;
  object-fit: contain;
  margin-top: -2rem;
}

/* Responsive */
@media (min-width: 768px) {
  .banner {
    padding: 1rem 2.5rem;
  }

  .banner-container {
    flex-direction: row;
  }

  .banner-text {
    text-align: left;
  }

  .banner-title {
    font-size: 2.5rem;
  }

  .banner-image {
    padding-left: 2.5rem;
  }

  .banner-image img {
    max-width: 400px;
    margin-top: -3rem;
    margin-bottom: -3rem;
  }

  .desktop-only {
    display: inline;
  }

  .mobile-only {
    display: none;
  }
}

@media (max-width: 767px) {
  .desktop-only {
    display: none;
  }
  .mobile-only {
    display: block;
  }
}

/* Banner ended */

/* Footer section */

.footer {
  background: white;
  margin-top: 5rem;
  padding: 3rem 1.5rem 1.5rem;
  font-size: 15px;
  color: #4b5563;
}

.footer-top {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.footer-left {
  max-width: 350px;
  line-height: 1.6;
  text-align: justify;
}

.footer-logo {
  width: 160px;
  margin-bottom: 1rem;
}

.footer-center,
.footer-right {
  text-align: center;
}

.footer-title {
  font-size: 1.125rem;
  font-weight: bold;
  color: black;
  margin-bottom: 0.75rem;
}

.footer-center ul,
.footer-right ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-center li,
.footer-right li {
  margin-bottom: 0.5rem;
}

.footer-center a {
  text-decoration: none;
  color: #4b5563;
  transition: color 0.3s ease, text-decoration 0.3s ease;
}

.footer-center a:hover {
  color: #5f6fff;
  text-decoration: underline;
}

.footer-bottom {
  margin-top: 2.5rem;
  text-align: center;
}

.footer-bottom hr {
  border: none;
  border-top: 1px solid #5f6fff;
  margin-bottom: 1rem;
}

.footer-bottom p {
  font-size: 0.9rem;
  color: #6b7280;
}

/* ✅ Responsive */
@media (min-width: 1024px) {
  .footer-top {
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
  }

  .footer-center,
  .footer-right {
    text-align: left;
  }
}


/* Footer ended */

  </style>
</head>
<body>


  <!-- Navbar -->
  <nav class="navbar">
    <img src="logo.svg" alt="logo" class="logo" onclick="window.location.href='index.py'">

    <ul class="nav-links">
      <li><a href="index.py">HOME</a></li>
      <li><a href="all-doctors.py">ALL DOCTORS</a></li>
      <li><a href="about.py">ABOUT</a></li>
      <li><a href="contact.py">CONTACT</a></li>
    </ul>

    <div class="navbar-right">
      <div class="dropdown">
        <button class="dropbtn" onclick="toggleDropdown('registerDropdown')">Register ▾</button>
        <div class="dropdown-content" id="registerDropdown">
          <a href="register-doctor.py">Doctor</a>
          <a href="register-patient.py">Patient</a>
        </div>
      </div>

      <div class="dropdown">
        <button class="dropbtn" onclick="toggleDropdown('loginDropdown')">Login ▾</button>
        <div class="dropdown-content" id="loginDropdown">
          <a href="login-doctor.py">Doctor</a>
          <a href="login-patient.py">Patient</a>
          <a href="login-admin.py">Admin</a>
        </div>
      </div>
    </div>

    <img src="menu_icon.svg" class="menu-icon" onclick="openMenu()" alt="menu" />
  </nav>

  <!-- Mobile Menu -->
  <div class="mobile-menu" id="mobileMenu">
    <div class="mobile-header">
      <img src="logo.svg" alt="logo" class="logo" />
      <img src="cross_icon.png" alt="close" class="close-icon" onclick="closeMenu()">
    </div>
    <ul class="mobile-links">
      <li><a href="index.py">HOME</a></li>
      <li><a href="all-doctors.py">ALL DOCTORS</a></li>
      <li><a href="about.py">ABOUT</a></li>
      <li><a href="contact.py">CONTACT</a></li>
      <li>
        <div class="mobile-dropdown-btn" onclick="toggleMobileDropdown('regDrop')">Register ▾</div>
        <div class="mobile-dropdown" id="regDrop">
          <a href="register-doctor.py">Doctor</a>
          <a href="register-patient.py">Patient</a>
        </div>
      </li>
      <li>
        <div class="mobile-dropdown-btn" onclick="toggleMobileDropdown('loginDrop')">Login ▾</div>
        <div class="mobile-dropdown" id="loginDrop">
          <a href="login-doctor.py">Doctor</a>
          <a href="login-patient.py">Patient</a>
          <a href="login-admin.py">Admin</a>
        </div>
      </li>
    </ul>
  </div>

  <!-- Navbar ended -->
   <!-- Header section -->
<div class="header">
  <div class="header-container">
    <!-- Left Side -->
    <div class="header-left">
      <p class="header-title">
        Book Appointment <br /> With Trusted Doctors
      </p>

      <div class="header-group">
        <img src="group_profiles.png" alt="icons" class="group-img" />
        <p class="header-desc">
          Simply browse through our extensive list of trusted doctors,
          <br class="desktop-only" />
          schedule your appointment hassle-free.
        </p>
      </div>

      <a href="#speciality" class="header-btn">
        Book Appointment
        <img src="arrow_icon.svg" alt="arrow" class="btn-arrow" />
      </a>
    </div>

    <!-- Right Side -->
    <div class="header-right">
      <img src="header_img.png" alt="header" class="header-img" />
    </div>
  </div>
</div>

<!-- Header section ended -->

<!-- SpecialityMenu -->
<div id="speciality" class="speciality-section">
  <h1 class="speciality-title">Find by Speciality</h1>

  <p class="speciality-desc">
    Simply browse through our extensive list of trusted doctors,
    <br class="desktop-only" />
    schedule your appointments hassle-free
  </p>

  <div class="speciality-grid" id="specialityGrid">
    <div class="speciality-item" data-target="#general-physician">
      <img src="General_physician.svg" alt="General Physician" class="speciality-img" />
      <p>General Physician</p>
    </div>
    <div class="speciality-item" data-target="#gynecologist">
      <img src="Gynecologist.svg" alt="Gynecologist" class="speciality-img" />
      <p>Gynecologist</p>
    </div>
    <div class="speciality-item" data-target="#dermatologist">
      <img src="Dermatologist.svg" alt="Dermatologist" class="speciality-img" />
      <p>Dermatologist</p>
    </div>
    <div class="speciality-item" data-target="#pediatricians">
      <img src="Pediatricians.svg" alt="Pediatricians" class="speciality-img" />
      <p>Pediatricians</p>
    </div>
    <div class="speciality-item" data-target="#neurologist">
      <img src="Neurologist.svg" alt="Neurologist" class="speciality-img" />
      <p>Neurologist</p>
    </div>
    <div class="speciality-item" data-target="#gastroenterologist">
      <img src="Gastroenterologist.svg" alt="Gastroenterologist" class="speciality-img" />
      <p>Gastroenterologist</p>
    </div>
  </div>
</div>


<!-- SpecialityMenu Ended -->

<!-- Top Doctors -->



<!-- top Doctors ended -->

<!-- Banner -->
  <div class="banner">
  <div class="banner-container">
    <!-- Left Side -->
    <div class="banner-text">
      <div>
        <p class="banner-title">
          Book Appointment <span class="desktop-only">With 100+ Trusted Doctors</span>
        </p>
        <p class="banner-title mobile-only">With 100+ Trusted Doctors</p>
      </div>
      <button class="banner-btn" id="createAccountBtn">
        Create Account
      </button>
    </div>

    <!-- Right Side Image -->
    <div class="banner-image">
      <img src="appointment_img.png" alt="banner" />
    </div>
  </div>
</div>
<!-- Banner Section Ended -->

<!-- Footer Section -->

<div class="footer">
  <!-- Top Section -->
  <div class="footer-top">
    <!-- Left Section -->
    <div class="footer-left">
      <img src="logo.svg" alt="logofooter" class="footer-logo" />
      <p>
        <strong>
          Prescriptive is your trusted doctor appointment platform. We connect
          you with 100+ verified doctors. Book appointments anytime, anywhere.
          Track appointment history with ease. Your health, our
          priority—Prescriptive cares.
        </strong>
      </p>
    </div>

    <!-- Center Section -->
    <div class="footer-center">
      <p class="footer-title">COMPANY</p>
      <ul>
        <li><a href="index.py">Home</a></li>
        <li><a href="about.py">About Us</a></li>
        <li><a href="contact.py">Contact</a></li>
        <li><a href="privacy-policy.py">Privacy Policy</a></li>
      </ul>
    </div>

    <!-- Right Section -->
    <div class="footer-right">
      <p class="footer-title">GET IN TOUCH</p>
      <ul>
        <li>📞 +1-212-456-7890</li>
        <li>📧 prescriptive@gmail.com</li>
      </ul>
    </div>
  </div>

  <!-- Bottom Section -->
  <div class="footer-bottom">
    <hr />
    <p>© 2025 <strong>Prescriptive</strong> — All Rights Reserved.</p>
  </div>
</div>


<!-- Footer ended -->


  <script>

    //Navbar
    function openMenu() {
      document.getElementById("mobileMenu").classList.add("show");
    }
    function closeMenu() {
      document.getElementById("mobileMenu").classList.remove("show");
    }
    function toggleMobileDropdown(id) {
      document.getElementById(id).classList.toggle("show");
    }
    function toggleDropdown(id) {
      document.querySelectorAll('.dropdown-content').forEach(el => {
        if (el.id !== id) el.classList.remove('show');
      });
      document.getElementById(id).classList.toggle("show");
    }
    window.onclick = function(event) {
      if (!event.target.matches('.dropbtn')) {
        document.querySelectorAll('.dropdown-content').forEach(el => {
          el.classList.remove('show');
        });
      }
    };

    // Banner section

    document.getElementById("createAccountBtn").addEventListener("click", function () {
  window.location.href = "login.py";
  window.scrollTo({ top: 0, behavior: "smooth" });
});

//Header section

document.querySelectorAll(".header-btn").forEach((btn) => {
  btn.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector("#speciality");
    if (target) {
      target.scrollIntoView({ behavior: "smooth" });
    }
  });
});

//Speciality

document.querySelectorAll(".speciality-item").forEach(item => {
  item.addEventListener("click", () => {
    const target = item.getAttribute("data-target");
    if (target && document.querySelector(target)) {
      document.querySelector(target).scrollIntoView({
        behavior: "smooth"
      });
    }
  });
});

//Footer Section
document.querySelectorAll('.footer-center a').forEach(link => {
  link.addEventListener('click', e => {
    if (link.getAttribute('href').startsWith('#')) {
      e.preventDefault();
      document.querySelector(link.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    }
  });
});



  </script>

</body>
</html>

""")