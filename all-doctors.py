#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys

cgitb.enable()
form = cgi.FieldStorage()
con = pymysql.connect(host="localhost", user="root", password="", database="appointment_booking_system")
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

# Fetch doctors with correct columns
cur.execute("""SELECT id, Doctor_name, Specialization, Dob, Address_line1, Address_line2, 
                      Hospital_name, Hospital_address, About, Email, Profile_picture 
               FROM doctor_register""")
doctors = cur.fetchall()

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
    *{margin:0;padding:0;box-sizing:border-box;}
    body{font-family:'Outfit',sans-serif;background:#fff;color:#222;padding:0 120px;}
    a{text-decoration:none;}

    /* Navbar */
    .navbar{display:flex;align-items:center;justify-content:space-between;padding:0 24px;background:#fff;position:sticky;top:0;z-index:1000;border-bottom:2px solid #000;}
    .navbar img.logo{width:180px;height:180px;cursor:pointer;}
    .nav-links{display:flex;gap:40px;list-style:none;justify-content:center;flex:1;} /* ✅ center alignment */
    .nav-links a{color:#333;font-weight:500;padding:10px 5px;transition:color 0.3s ease;}
    .nav-links a:hover{color:#5f6fff;}
    .navbar-right{display:flex;align-items:center;gap:16px;}
    .dropbtn{background:#fff;border:2px solid #5f6fff;color:#5f6fff;font-weight:600;cursor:pointer;padding:6px 12px;border-radius:20px;}
    .dropbtn:hover{background:#5f6fff;color:#fff;}
    .dropdown-content{display:none;position:absolute;top:100%;right:0;background:#fff;border:2px solid #5f6fff;border-radius:8px;min-width:180px;}
    .dropdown-content.show{display:block;}
    .dropdown-content a{display:block;padding:12px 16px;color:#333;}
    .dropdown-content a:hover{background:#5f6fff;color:#fff;}

    /* Mobile Menu Button */
    .menu-toggle{display:none;font-size:32px;cursor:pointer;background:none;border:none;color:#333;transition:0.3s;}
    .menu-toggle:hover{color:#5f6fff;}
    .menu-toggle.active{color:#5f6fff;}

    .menu-container{display:flex;align-items:center;gap:20px;}

    /* Doctor Section */
    .doctor-section{padding:3rem 0;}
    .doctor-title{text-align:center;font-size:2.2rem;font-weight:700;color:#5f6fff;margin-bottom:2rem;}
    .doctor-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:2rem;}
    .doctor-card{border:1px solid #ddd;border-radius:12px;padding:1.5rem;text-align:center;transition:all 0.3s ease;box-shadow:0 2px 6px rgba(0,0,0,0.1);cursor:pointer;background:#fff;}
    .doctor-card:hover{transform:translateY(-5px);box-shadow:0 6px 15px rgba(0,0,0,0.15);}
    .doctor-card img{width:120px;height:120px;border-radius:50%;object-fit:cover;margin-bottom:1rem;}
    .doctor-name{font-size:1.2rem;font-weight:600;color:#333;}
    .doctor-specialization{color:#5f6fff;font-weight:500;font-size:0.95rem;}

    /* Modal */
    .modal{display:none;position:fixed;z-index:2000;left:0;top:0;width:100%;height:100%;overflow:auto;background:rgba(0,0,0,0.5);}
    .modal-content{background:#fff;margin:5% auto;padding:2rem;border-radius:12px;width:90%;max-width:600px;position:relative;}
    .close{position:absolute;top:10px;right:20px;font-size:32px;font-weight:bold;color:#333;cursor:pointer;transition:0.3s;}
    .close:hover{color:#5f6fff;}
    .modal img{width:100px;height:100px;border-radius:50%;object-fit:cover;margin-bottom:1rem;}
    .modal h3{margin-bottom:0.5rem;color:#333;}
    .modal p{margin:0.3rem 0;color:#555;font-size:0.95rem;}
    .modal strong{color:#111;}

    /* Footer */
    .footer{background:white;margin-top:5rem;padding:3rem 1.5rem 1.5rem;font-size:15px;color:#4b5563;}
    .footer-top{display:flex;flex-direction:column;gap:2.5rem;}
    .footer-left{max-width:350px;line-height:1.6;text-align:justify;}
    .footer-logo{width:160px;margin-bottom:1rem;}
    .footer-center,.footer-right{text-align:center;}
    .footer-title{font-size:1.125rem;font-weight:bold;color:black;margin-bottom:0.75rem;}
    .footer-center a{text-decoration:none;color:#4b5563;}
    .footer-center a:hover{color:#5f6fff;text-decoration:underline;}
    .footer-bottom{margin-top:2.5rem;text-align:center;}
    .footer-bottom hr{border:none;border-top:1px solid #5f6fff;margin-bottom:1rem;}
    .footer-bottom p{font-size:0.9rem;color:#6b7280;}
    @media(min-width:1024px){.footer-top{flex-direction:row;justify-content:space-between;align-items:flex-start;}.footer-center,.footer-right{text-align:left;}}

    /* Responsive Fixes */
    @media(max-width:1200px){
      body{padding:0 60px;}
      .navbar img.logo{width:150px;height:150px;}
    }
    @media(max-width:992px){
      body{padding:0 40px;}
      .nav-links{gap:20px;}
      .doctor-title{font-size:1.8rem;}
    }
    @media(max-width:768px){
      body{padding:0 20px;}
      .navbar{flex-wrap:wrap;}
      .menu-toggle{display:block;font-size:38px;}
      .menu-container{display:none;flex-direction:column;width:100%;margin-top:10px;}
      .menu-container.show{display:flex;}
      .nav-links{flex-direction:column;gap:12px;align-items:flex-start;width:100%;}
      .navbar-right{flex-direction:column;align-items:flex-start;width:100%;gap:12px;}
      .navbar img.logo{width:140px;height:140px;}
      .doctor-grid{grid-template-columns:repeat(auto-fit,minmax(180px,1fr));}
      .doctor-title{font-size:1.6rem;}
    }
    @media(max-width:576px){
      body{padding:0 10px;}
      .doctor-card img{width:100px;height:100px;}
      .doctor-name{font-size:1rem;}
      .doctor-specialization{font-size:0.85rem;}
      .footer{padding:2rem 1rem;}
    }
    @media(max-width:400px){
      .doctor-grid{grid-template-columns:1fr;}
      .doctor-card{padding:1rem;}
      .doctor-card img{width:90px;height:90px;}
      .doctor-title{font-size:1.4rem;}
    }
  </style>
</head>
<body>

  <!-- Navbar -->
  <nav class="navbar">
    <img src="logo.svg" alt="logo" class="logo" onclick="window.location.href='index.py'">

    <!-- Mobile Menu Toggle -->
    <button class="menu-toggle" onclick="toggleMenu()">☰</button>

    <div class="menu-container">
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
    </div>
  </nav>

  <!-- Doctor List -->
  <section class="doctor-section">
    <h2 class="doctor-title">Our Doctors</h2>
    <div class="doctor-grid">
""")

# Loop through doctors and display
for doc in doctors:
    (doc_id, name, specialization, dob, address1, address2, hospital_name,
     hospital_address, about, email, profile_picture) = doc

    img_src = f"Doctor-register-images/{profile_picture}" if profile_picture else "default-doctor.png"

    print(f"""
      <div class="doctor-card" onclick="openModal({doc_id})">
        <img src='{img_src}' alt='{name}'>
        <div class="doctor-name">{name}</div>
        <div class="doctor-specialization">{specialization}</div>
      </div>

      <!-- Modal for Doctor {doc_id} -->
      <div id="modal-{doc_id}" class="modal">
        <div class="modal-content">
          <span class="close" onclick="closeModal({doc_id})">&times;</span>
          <img src='{img_src}' alt='{name}'>
          <h3>{name}</h3>
          <p><strong>Specialization:</strong> {specialization}</p>
          <p><strong>DOB:</strong> {dob}</p>
          <p><strong>Address:</strong> {address1} {address2}</p>
          <p><strong>Hospital:</strong> {hospital_name}, {hospital_address}</p>
          <p><strong>Email:</strong> {email}</p>
          <p><strong>About:</strong> {about}</p>
        </div>
      </div>
    """)

print("""
    </div>
  </section>

  <!-- Footer -->
  <div class="footer">
    <div class="footer-top">
      <div class="footer-left">
        <img src="logo.svg" alt="logofooter" class="footer-logo" />
        <p><strong>Prescriptive is your trusted doctor appointment platform. Book anytime, anywhere.</strong></p>
      </div>
      <div class="footer-center">
        <p class="footer-title">COMPANY</p>
        <ul>
          <li><a href="index.py">Home</a></li>
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
    function toggleDropdown(id) {
      document.querySelectorAll('.dropdown-content').forEach(el => {
        if (el.id !== id) el.classList.remove('show');
      });
      document.getElementById(id).classList.toggle("show");
    }

    function toggleMenu() {
      const menu = document.querySelector('.menu-container');
      const btn = document.querySelector('.menu-toggle');
      menu.classList.toggle('show');
      btn.textContent = menu.classList.contains('show') ? '✖' : '☰';
      btn.classList.toggle('active');
    }

    function openModal(id) {
      document.getElementById('modal-' + id).style.display = 'block';
    }
    function closeModal(id) {
      document.getElementById('modal-' + id).style.display = 'none';
    }
    window.onclick = function(event) {
      document.querySelectorAll('.modal').forEach(modal => {
        if (event.target === modal) modal.style.display = 'none';
      });
      if (!event.target.matches('.dropbtn')) {
        document.querySelectorAll('.dropdown-content').forEach(el => el.classList.remove('show'));
      }
    };
  </script>
</body>
</html>
""")
