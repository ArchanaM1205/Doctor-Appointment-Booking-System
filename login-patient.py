#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys
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
      border-bottom: 2px solid #000;
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

    /* login section */
    .modal-overlay {
      display: flex;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      z-index: 1000;
      justify-content: center;
      align-items: center;
    }

    .modal {
      background: white;
      width: 90%;
      max-width: 400px;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
      animation: slideDown 0.3s ease;
    }

    @keyframes slideDown {
      from { transform: translateY(-50px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }

    h2 {
      text-align: center;
      color: #5f6FFF;
    }

    .form-group {
      margin-bottom: 15px;
    }

    .form-group label {
      font-size: 14px;
      font-weight: 500;
      display: block;
      margin-bottom: 5px;
    }

    .form-group input {
      width: 100%;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 6px;
      font-size: 14px;
      outline: none;
    }

    .form-group input:focus {
      border-color: #5f6FFF;
    }

    .submit-btn,
    .cancel-btn {
      width: 100%;
      padding: 12px;
      font-size: 16px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      margin-top: 10px;
      transition: background 0.3s ease;
    }

    .submit-btn {
      background: #5f6FFF;
      color: white;
    }
    .submit-btn:hover {
      background: #3d47d6;
    }

    .cancel-btn {
      background: red;
      color: white;
    }
    .cancel-btn:hover {
      background: darkred;
    }

    .forgot-password {
      text-align: right;
      font-size: 14px;
      margin-top: -10px;
      margin-bottom: 15px;
    }

    .forgot-password a {
      color: #5f6FFF;
      text-decoration: none;
    }
    .forgot-password a:hover {
      text-decoration: underline;
    }

    .login-footer {
      text-align: center;
      margin-top: 10px;
      font-size: 14px;
    }

    .login-footer a {
      color: #5f6FFF;
      text-decoration: none;
      font-weight: bold;
    }

    .login-footer a:hover {
      text-decoration: underline;
    }

    /* Footer */
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
  </style>
</head>
<body>

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

<div class="modal-overlay" id="loginModal">
  <div class="modal">
    <h2>Patient Login</h2>
    <form id="loginForm" method="post">
      <div class="form-group">
        <label>Username</label>
        <input type="email" id="email" name="email" placeholder="Enter your username" required />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input type="password" id="password" name="password" placeholder="Enter your password" required />
      </div>
      <div class="forgot-password">
        <a href="forgot-password-patient.py">Forgot Password?</a>
      </div>
      <input type="submit" class="submit-btn" value="Login" name="sub">
      <button type="button" class="cancel-btn" id="cancelBtn">Cancel</button>
    </form>
    <div class="login-footer">
      Don't have an account? <a href="register-patient.py">Sign Up</a>
    </div>
  </div>
</div>

<div class="footer">
  <div class="footer-top">
    <div class="footer-left">
      <img src="logo.svg" alt="logofooter" class="footer-logo" />
      <p><strong>Prescriptive is your trusted doctor appointment platform...</strong></p>
    </div>
    <div class="footer-center">
      <p class="footer-title">COMPANY</p>
      <ul>
        <li><a href="index.py">Home</a></li>
        <li><a href="about.py">About Us</a></li>
        <li><a href="contact.py">Contact</a></li>
        <li><a href="privacy-policy.py">Privacy Policy</a></li>
      </ul>
    </div>
    <div class="footer-right">
      <p class="footer-title">GET IN TOUCH</p>
      <ul>
        <li>📞 +1-212-456-7890</li>
        <li>📧 prescriptive@gmail.com</li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <hr />
    <p>© 2025 <strong>Prescriptive</strong> — All Rights Reserved.</p>
  </div>
</div>

<script>
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

document.getElementById("cancelBtn").addEventListener("click", function() {
  window.location.href = "index.py";
});

// ✅ Let form submit naturally to Python backend
document.getElementById("loginForm").addEventListener("submit", function() {
  // No preventDefault() so backend gets data
});
</script>

</body>
</html>
""")

submit = form.getvalue("sub")
if submit != None:
    u_name = form.getvalue("email")
    password = form.getvalue("password")
    q = """select id from patient_register where Email='%s' and Password='%s'""" % (u_name, password)
    cur.execute(q)
    det = cur.fetchone()
    if det != None:
        print("""
        <script>
        alert("Login success");
        window.location.href="patient-dashboard.py?id=%s";
        </script>
        """ % det[0])
    else:
        print("""
        <script>
        alert("User not found");
        </script>
        """)
