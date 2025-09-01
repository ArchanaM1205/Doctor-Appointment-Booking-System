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


/* About us */

.about-container {
  padding: 2.5rem 1rem;
  max-width: 1200px;
  margin: auto;
}

.about-title {
  font-size: 2.5rem;
  font-weight: bold;
  text-align: center;
  color: #5f6fff;
  margin-bottom: 3rem;
}

.about-content {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
  align-items: center;
  margin-bottom: 3rem;
}

.about-image img {
  width: 100%;
  max-width: 550px;
  border-radius: 1rem;
}

.about-text {
  max-width: 600px;
  font-size: 1rem;
  color: #374151;
  line-height: 1.6;
}

.vision-title {
  font-size: 1.25rem;
  font-weight: bold;
  color: #5f6fff;
  margin-top: 1.5rem;
  margin-bottom: 0.5rem;
}

.why-choose {
  text-align: center;
}

.why-title {
  font-size: 1.75rem;
  font-weight: bold;
  color: #5f6fff;
  margin-bottom: 2rem;
}

.why-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

.why-item {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.why-item:hover {
  background: #5f6fff;
  color: #fff;
}

.why-item h3 {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

/* ✅ Responsive */
@media (min-width: 768px) {
  .about-content {
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
  }

  .why-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .why-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}


/* About Us ended */

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

  <!-- About us -->

 <div class="about-container">
  <!-- Heading -->
  <h1 class="about-title">ABOUT US</h1>

  <!-- Image and Description Section -->
  <div class="about-content">
    <div class="about-image">
      <img src="about_image.png" alt="About Prescripto" />
    </div>
    <div class="about-text">
      <p>
        Prescripto is a revolutionary healthcare platform designed to simplify
        your doctor appointment booking process. We empower patients with easy
        access to expert medical professionals across a range of specialties.
        Our streamlined system ensures quick scheduling and a seamless patient
        experience.
      </p>
      <p>
        Whether you're booking from home or on the go, Prescripto provides
        reliable and personalized healthcare connections at your fingertips.
        With a user-friendly interface, advanced search filters, and smart
        matching technology, you’ll always find the right doctor with ease.
      </p>
      <div>
        <h2 class="vision-title">Our Vision</h2>
        <p>
          To bridge the gap between patients and healthcare providers by
          creating a transparent, accessible, and personalized platform that
          transforms the way appointments are made and healthcare is delivered.
        </p>
      </div>
    </div>
  </div>

  <!-- Why Choose Us Section -->
  <div class="why-choose">
    <h2 class="why-title">WHY CHOOSE US</h2>
    <div class="why-grid">
      <div class="why-item">
        <h3>Efficiency</h3>
        <p>
          Book appointments in just a few clicks with minimal wait time. Get
          access to healthcare faster than ever before.
        </p>
      </div>
      <div class="why-item">
        <h3>Convenience</h3>
        <p>
          Access a wide network of doctors and schedule visits at times that
          suit your busy lifestyle.
        </p>
      </div>
      <div class="why-item">
        <h3>Personalization</h3>
        <p>
          Receive tailored recommendations and stay connected with your
          healthcare journey all in one place.
        </p>
      </div>
    </div>
  </div>
</div>



  <!-- About Us Ended -->

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

//About section

document.addEventListener("scroll", () => {
  document.querySelectorAll(".why-item").forEach((item) => {
    const rect = item.getBoundingClientRect();
    if (rect.top < window.innerHeight - 50) {
      item.style.opacity = 1;
      item.style.transform = "translateY(0)";
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