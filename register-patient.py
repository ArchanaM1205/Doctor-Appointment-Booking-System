#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys, os
cgitb.enable()
form = cgi.FieldStorage()
con = pymysql.connect(host="localhost", user="root", password="", database="appointment_booking_system")
cur = con.cursor()
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
    /* ✅ your CSS kept as-is */
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

    /* register section */

.registration-container {
  max-width: 850px;
  margin: 40px auto;
  background: #ffffff;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.1);
  font-family: 'Outfit', sans-serif;
}

.form-title {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  color: #5f6FFF;
  margin-bottom: 25px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 6px;
  color: #333;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 15px;
  transition: 0.3s;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #5f6FFF;
  box-shadow: 0 0 6px rgba(95, 111, 255, 0.4);
}

.profile-upload {
  text-align: center;
}

.profile-preview {
  width: 120px;
  height: 120px;
  margin: 10px auto;
  border: 2px dashed #ccc;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9ff;
}

.profile-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-btn {
  margin-top: 8px;
  padding: 10px 18px;
  background: #5f6FFF;
  color: white;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
}

.upload-btn:hover {
  background: #3d47d6;
}

.form-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.submit-btn,
.cancel-btn {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s;
}

.submit-btn {
  background: #5f6FFF;
  color: white;
}
.submit-btn:hover {
  background: #3d47d6;
}

.cancel-btn {
  background: #f50606;
}
.cancel-btn:hover {
  background: #999;
}

.login-text {
  text-align: center;
  font-size: 14px;
  margin-top: 10px;
}

.login-text a {
  color: #5f6FFF;
  font-weight: bold;
  text-decoration: none;
}
.login-text a:hover {
  text-decoration: underline;
}

/* ✅ Responsive */
@media (min-width: 600px) {
  .form-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .profile-upload.full {
    grid-column: span 2;
  }

  .form-buttons {
    grid-column: span 2;
    flex-direction: row;
    justify-content: space-between;
  }

  .login-text {
    grid-column: span 2;
  }
}


    /* register ended */

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

  <!-- ✅ your Navbar HTML kept as-is -->
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


  

  <!-- Register patient section -->
<div class="registration-container">
  <h2 class="form-title">Patient Registration</h2>
  <form id="patientRegisterForm" method="post" enctype="multipart/form-data" class="form-grid">

    <div class="form-group">
      <label for="patientName">Full Name</label>
      <input type="text" id="patientName" name="patientName" required>
    </div>

    <div class="form-group">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required>
    </div>

    <div class="form-group">
      <label for="phone">Phone</label>
      <input type="tel" id="phone" name="phone" required>
    </div>

    <div class="form-group">
      <label for="dob">Date of Birth</label>
      <input type="date" id="dob" name="dob" required>
    </div>

    <div class="form-group">
      <label for="gender">Gender</label>
      <select id="gender" name="gender" required>
        <option value="">Select</option>
        <option>Male</option>
        <option>Female</option>
        <option>Other</option>
      </select>
    </div>

    <div class="form-group">
      <label for="maritalStatus">Marital Status</label>
      <select id="maritalStatus" name="maritalStatus" required>
        <option value="">Select</option>
        <option>Single</option>
        <option>Married</option>
        <option>Divorced</option>
      </select>
    </div>

    <div class="form-group">
      <label for="address1">Address Line 1</label>
      <input type="text" id="address1" name="address1" required>
    </div>

    <div class="form-group">
      <label for="address2">Address Line 2</label>
      <input type="text" id="address2" name="address2">
    </div>

    <div class="form-group">
      <label for="password">Password</label>
      <input type="password" id="password" name="password" required>
    </div>

    <div class="form-group">
      <label for="confirmPassword">Confirm Password</label>
      <input type="password" id="confirmPassword" name="confirmPassword" required>
    </div>

    <div class="form-group profile-upload full">
      <label>Profile Picture</label>
      <div class="profile-preview" id="profilePreview">
        <img src="upload_area.png" alt="Upload" />
      </div>
      <input type="file" id="profilePic" accept="image/*" name="profile_pic" hidden />
      <button type="button" class="upload-btn" onclick="document.getElementById('profilePic').click()">Upload</button>
    </div>

    <div class="form-buttons">
      <button type="submit" class="submit-btn" name="sub">Create Account</button>
      <button type="button" class="cancel-btn" id="cancelBtn" onclick="goHome()">Cancel</button>
    </div>

    <p class="login-text">
      Already have an account? <a href="login-patient.py">Login</a>
    </p>

  </form>
</div>
<!-- Register ended -->

<!-- ✅ Footer kept as-is -->
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
  // ✅ Navbar JS unchanged
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

  // Cancel → Redirect to Home
  function goHome(){
    window.location.href = "index.py";
  }

  // Live Profile Picture Preview
  const profilePicInput = document.getElementById("profilePic");
  const profilePreview = document.getElementById("profilePreview");
  profilePicInput.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        profilePreview.innerHTML = `<img src="${e.target.result}" alt="Profile Picture">`;
      };
      reader.readAsDataURL(file);
    }
  });

  // Validate Passwords → allow submit only if valid
  document.getElementById("patientRegisterForm").addEventListener("submit", function (e) {
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
      e.preventDefault();
      alert("Passwords do not match!");
    }
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

# ✅ Backend handling
Submit = form.getvalue("sub")
if Submit is not None:
    if len(form) != 0:
        Profile_image = form["profile_pic"]
        pi = ""
        if Profile_image.filename:
            if not os.path.exists("Patient-register-images"):
                os.makedirs("Patient-register-images")
            pi = os.path.basename(Profile_image.filename)
            with open("Patient-register-images/" + pi, "wb") as f:
                f.write(Profile_image.file.read())

        Patient_name = form.getvalue("patientName")
        Gender = form.getvalue("gender")
        Dob = form.getvalue("dob")
        Email = form.getvalue("email")
        Phone = form.getvalue("phone")
        Address_line1 = form.getvalue("address1")
        Address_line2 = form.getvalue("address2")
        Password = form.getvalue("password")
        Confirm_password = form.getvalue("confirmPassword")
        Marital_Status = form.getvalue("maritalStatus")

        sql = """INSERT INTO patient_register
        (Patient_name, Gender, Dob, Email, Phone, Address_line1, Address_line2, Password, Confirm_password, Profile_image, Marital_Status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        cur.execute(sql, (Patient_name, Gender, Dob, Email, Phone, Address_line1, Address_line2, Password, Confirm_password, pi, Marital_Status))
        con.commit()

        print("""
        <script>
        alert("Patient account created successfully!");
        window.location.href = "login-patient.py";
        </script>
        """)
