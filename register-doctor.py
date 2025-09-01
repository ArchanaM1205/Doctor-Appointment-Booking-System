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
    /* (Your full CSS remains unchanged here) */
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

/* register */

@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');

body {
  font-family: 'Outfit', sans-serif;
  background: #f9f9ff;
  color: #333;
  padding: 20px;
}

.register-container {
  max-width: 800px;
  background: #fff;
  margin: 40px auto;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.1);
}

.register-title {
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  color: #5f6fff;
  margin-bottom: 1.5rem;
}

form {
  display: grid;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: 500;
  margin-bottom: 6px;
}

input,
select,
textarea {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

input:focus,
select:focus,
textarea:focus {
  border-color: #5f6fff;
  outline: none;
  box-shadow: 0 0 5px rgba(95, 111, 255, 0.3);
}

textarea {
  resize: vertical;
  min-height: 100px;
}

.profile-upload {
  text-align: center;
}

.profile-preview {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: #f1f1f1;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 10px auto;
  overflow: hidden;
  border: 2px solid #ccc;
}

.profile-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.upload-btn {
  padding: 8px 12px;
  background: #5f6fff;
  color: #fff;
  font-size: 0.9rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.upload-btn:hover {
  background: #3d47d6;
}

.button-group {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.btn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: #5f6fff;
  color: #fff;
}

.btn-primary:hover {
  background: #3d47d6;
}

.btn-secondary {
  background:red;
  color: #333;
}

.btn-secondary:hover {
  background: #ddd;
}

.login-quote {
  text-align: center;
  margin-top: 20px;
  font-size: 0.95rem;
}

.login-quote a {
  color: #5f6fff;
  font-weight: 600;
  text-decoration: none;
}

.login-quote a:hover {
  text-decoration: underline;
}

/* ✅ Responsive */
@media (min-width: 768px) {
  form {
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }
  .form-group.full {
    grid-column: span 2;
  }
  .button-group {
    grid-column: span 2;
  }
  .login-quote {
    grid-column: span 2;
  }
}


/* register-ended */

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

  <!-- register  -->

<div class="register-container">
  <h1 class="register-title">Doctor Registration</h1>

  <form id="doctorForm" method="post" enctype="multipart/form-data">
    <div class="form-group">
      <label for="doctorName">Doctor Name</label>
      <input type="text" id="doctorName" name="name" required />
    </div>

    <div class="form-group">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required />
    </div>

    <div class="form-group">
      <label for="password">Password</label>
      <input type="password" id="password" name="password" required />
    </div>

    <div class="form-group">
      <label for="confirmPassword">Confirm Password</label>
      <input type="password" id="confirmPassword" name="confirm" required />
    </div>

    <div class="form-group">
      <label for="specialization">Specialization</label>
      <select id="specialization" name="specialist" required>
        <option value="">Select Specialization</option>
        <option value="General Physician">General Physician</option>
        <option value="Gynecologist">Gynecologist</option>
        <option value="Dermatologist">Dermatologist</option>
        <option value="Pediatrician">Pediatrician</option>
        <option value="Neurologist">Neurologist</option>
        <option value="Gastroenterologist">Gastroenterologist</option>
        <option value="Orthopedic">Orthopedic</option>
        <option value="Psychiatrist">Psychiatrist</option>
        <option value="Dentist">Dentist</option>
        <option value="Ophthalmologist">Ophthalmologist</option>
        <option value="Urologist">Urologist</option>
        <option value="Pulmonologist">Pulmonologist</option>
        <option value="Oncologist">Oncologist</option>
        <option value="Nephrologist">Nephrologist</option>
        <option value="Endocrinologist">Endocrinologist</option>
        <option value="Rheumatologist">Rheumatologist</option>
        <option value="Surgeon (General)">Surgeon (General)</option>
        <option value="Plastic Surgeon">Plastic Surgeon</option>
        <option value="Radiologist">Radiologist</option>
        <option value="Pathologist">Pathologist</option>
        <option value="Hematologist">Hematologist</option>
        <option value="Allergist / Immunologist">Allergist / Immunologist</option>
        <option value="Infectious Disease Specialist">Infectious Disease Specialist</option>
      </select>
    </div>

    <div class="form-group">
      <label for="experience">Experience (Years)</label>
      <input type="number" id="experience" name="exp" min="0" required />
    </div>

    <div class="form-group">
      <label for="dob">Date of Birth</label>
      <input type="date" id="dob" name="dob" required />
    </div>

    <div class="form-group">
      <label for="gender">Gender</label>
      <select id="gender" name="gender" required>
        <option value="">Select Gender</option>
        <option value="Male">Male</option>
        <option value="Female">Female</option>
        <option value="Other">Other</option>
      </select>
    </div>

    <div class="form-group">
      <label for="address1">Address Line 1</label>
      <input type="text" id="address1" name="add_line1" required />
    </div>

    <div class="form-group">
      <label for="address2">Address Line 2</label>
      <input type="text" id="address2" name="add_line2" />
    </div>

    <div class="form-group">
      <label for="phone">Phone Number</label>
      <input type="tel" id="phone" name="phone_no" pattern="[0-9]{10}" max_length="10" required />
    </div>

    <div class="form-group">
      <label for="hospitalName">Hospital Name</label>
      <input type="text" id="hospitalName" name="hospital_name" required />
    </div>

    <div class="form-group">
      <label for="hospitalAddress">Hospital Address</label>
      <input type="text" id="hospitalAddress" name="hospital_address" required />
    </div>

    <div class="form-group full">
      <label for="about">About</label>
      <textarea id="about" name="about"></textarea>
    </div>

    <div class="form-group profile-upload full">
      <label>Profile Picture</label>
      <div class="profile-preview" id="profilePreview">
        <img src="upload_area.png" alt="Upload" />
      </div>
      <input type="file" id="profilePic" name="profile_pic" accept="image/*" hidden />
      <button type="button" class="upload-btn" onclick="document.getElementById('profilePic').click()">Upload</button>
    </div>

    <div class="button-group">
      <input type="submit" class="btn btn-primary" name="sub" value="Create Account">
      <button type="button" onClick="goHome()" class="btn btn-secondary">Cancel</button>
    </div>

    <p class="login-quote">
      Already have an account? <a href="login-doctor.py">Login here</a>
    </p>
  </form>
</div>

<!-- Footer Section -->
<div class="footer">
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


  <!-- (Footer code unchanged) -->
</div>

<script>
  // Navbar JS (unchanged)
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




  function goHome(){
    window.location.href="index.py";
  }

  // Profile preview
  document.getElementById("profilePic").addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        document.getElementById("profilePreview").innerHTML =
          `<img src="${e.target.result}" alt="Profile" />`;
      };
      reader.readAsDataURL(file);
    }
  });

  // ✅ Password Validation & Allow Submit
  document.getElementById("doctorForm").addEventListener("submit", function (e) {
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    if (password !== confirmPassword) {
      e.preventDefault(); // block only if mismatch
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

# Backend form handling
Submit = form.getvalue("sub")
if Submit != None:
    if len(form) != 0:
        Profile_picture = form["profile_pic"]
        pi = ""
        if Profile_picture.filename:
            pi = os.path.basename(Profile_picture.filename)
            open("Doctor-register-images/" + pi, "wb").write(Profile_picture.file.read())
        Doctor_name = form.getvalue("name")
        Email = form.getvalue("email")
        Password = form.getvalue("password")
        Confirm_password = form.getvalue("confirm")
        Specialization = form.getvalue("specialist")
        Experience = form.getvalue("exp")
        Dob = form.getvalue("dob")
        Gender = form.getvalue("gender")
        Address_line1 = form.getvalue("add_line1")
        Address_line2 = form.getvalue("add_line2")
        Phone = form.getvalue("phone_no")
        Hospital_name = form.getvalue("hospital_name")
        Hospital_address = form.getvalue("hospital_address")
        About = form.getvalue("about")

        q = """INSERT INTO doctor_register(Doctor_name,Email,Password,Confirm_password,Specialization,Experience,Dob,Gender,Address_line1,Address_line2,Phone,Hospital_name,Hospital_address,About,Profile_picture)
        VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" % (
        Doctor_name, Email, Password, Confirm_password, Specialization, Experience, Dob, Gender, Address_line1,
        Address_line2, Phone, Hospital_name, Hospital_address, About, pi)

        cur.execute(q)
        con.commit()
        print("""
        <script>
        alert("Registered successfully");
        window.location.href="login-doctor.py";
        </script>
        """)
