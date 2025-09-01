#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys
cgitb.enable()
form = cgi.FieldStorage()
sys.stdout.reconfigure(encoding='utf-8')

# Database connection
con = pymysql.connect(host="localhost", user="root", password="", database="appointment_booking_system")
cur = con.cursor()

# Initialize message
message = ""

# Process form submission
email = form.getvalue("Email")
password = form.getvalue("Password")
confirm_password = form.getvalue("Confirm_password")

if email and password and confirm_password:
    if password != confirm_password:
        message = "<script>alert('Passwords do not match!');</script>"
    else:
        try:
            sql = "UPDATE doctor_register SET password=%s, confirm_password=%s WHERE email=%s"
            cur.execute(sql, (password, confirm_password, email))
            con.commit()
            message = f"<script>alert('Password successfully updated for {email}'); window.location.href='login-doctor.py';</script>"
        except Exception as e:
            message = f"<script>alert('Error updating password: {str(e)}');</script>"

# Output HTML
print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Doctor Reset Password</title>
<link rel="icon" type="image/svg+xml" href="logo.svg" />
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');
* {{margin:0; padding:0; box-sizing:border-box;}}
body {{font-family:'Outfit', sans-serif; background:#fff; color:#222; padding:0 120px;}}

/* Navbar */
.navbar {{display:flex; align-items:center; justify-content:space-between; padding:0 24px; background:#fff; position:sticky; top:0; z-index:1000; border-bottom:2px solid #000;}}
.navbar img.logo {{width:160px; height:160px; cursor:pointer;}}
.nav-links {{display:flex; gap:40px; list-style:none;}}
.nav-links li a {{text-decoration:none; color:#333; font-weight:500; font-size:0.95rem; padding:10px 5px; position:relative;}}
.nav-links li a:hover {{color:#5f6fff;}}
.navbar-right {{display:flex; align-items:center; gap:16px;}}
.dropdown {{position:relative;}}
.dropbtn {{background:#fff; border:2px solid #5f6fff; color:#5f6fff; font-size:0.9rem; font-weight:600; cursor:pointer; padding:6px 12px; border-radius:20px;}}
.dropbtn:hover {{background:#5f6fff; color:#fff;}}
.dropdown-content {{display:none; position:absolute; top:100%; right:0; background:#fff; border:2px solid #5f6fff; border-radius:8px; min-width:180px;}}
.dropdown-content.show {{display:block;}}
.dropdown-content a {{display:block; padding:12px 16px; text-decoration:none; color:#333;}}
.dropdown-content a:hover {{background:#5f6fff; color:#fff;}}

/* Modal */
.modal-overlay {{display:flex; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:1000; justify-content:center; align-items:center;}}
.modal {{background:#fff; width:90%; max-width:400px; padding:20px; border-radius:10px; box-shadow:0 5px 20px rgba(0,0,0,0.2); animation:slideDown 0.3s ease;}}
@keyframes slideDown {{from {{transform:translateY(-40px); opacity:0;}} to {{transform:translateY(0); opacity:1;}}}}
h2 {{text-align:center; color:#5f6fff;}}
.form-group {{margin-bottom:15px;}}
.form-group label {{font-size:14px; font-weight:500; display:block; margin-bottom:5px;}}
.form-group input {{width:100%; padding:10px; border:1px solid #ccc; border-radius:6px; font-size:14px;}}
.form-group input:focus {{border-color:#5f6fff;}}
.submit-btn, .cancel-btn {{width:100%; padding:12px; font-size:16px; border:none; border-radius:8px; cursor:pointer; margin-top:10px;}}
.submit-btn {{background:#5f6fff; color:#fff;}}
.submit-btn:hover {{background:#3d47d6;}}
.cancel-btn {{background:#ccc; color:#333;}}
.cancel-btn:hover {{background:#aaa;}}
.login-footer {{text-align:center; margin-top:10px; font-size:14px;}}
.login-footer a {{color:#5f6fff; font-weight:bold; text-decoration:none;}}
.login-footer a:hover {{text-decoration:underline;}}

/* Footer */
.footer {{background:white; margin-top:5rem; padding:3rem 1.5rem 1.5rem; font-size:15px; color:#4b5563;}}
.footer-top {{display:flex; flex-direction:column; gap:2.5rem;}}
.footer-left {{max-width:350px; line-height:1.6; text-align:justify;}}
.footer-logo {{width:160px; margin-bottom:1rem;}}
.footer-center, .footer-right {{text-align:center;}}
.footer-title {{font-size:1.125rem; font-weight:bold; color:black; margin-bottom:0.75rem;}}
.footer-center ul, .footer-right ul {{list-style:none; padding:0; margin:0;}}
.footer-center li, .footer-right li {{margin-bottom:0.5rem;}}
.footer-center a {{text-decoration:none; color:#4b5563; transition:0.3s;}}
.footer-center a:hover {{color:#5f6fff; text-decoration:underline;}}
.footer-bottom {{margin-top:2.5rem; text-align:center;}}
.footer-bottom hr {{border:none; border-top:1px solid #5f6fff; margin-bottom:1rem;}}
.footer-bottom p {{font-size:0.9rem; color:#6b7280;}}

/* Responsive */
@media(max-width:500px) {{.modal {{width:95%; padding:15px;}}}}
</style>
</head>
<body>

{message}

<!-- Navbar -->
<nav class="navbar">
  <img src="logo.svg" alt="logo" class="logo" onclick="window.location.href='index.py'">
  <ul class="nav-links">
    <li><a href="index.py">HOME</a></li>
    <li><a href="doctors.py">ALL DOCTORS</a></li>
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
</nav>

<!-- Forgot Password Modal -->
<div class="modal-overlay" id="forgotPasswordModal">
  <div class="modal">
    <h2>Reset Password</h2>
    <form id="resetPasswordForm" method="post" action="">
      <div class="form-group">
        <label for="Email">Registered Email</label>
        <input type="email" id="Email" name="Email" placeholder="Enter your email" required />
      </div>
      <div class="form-group">
        <label for="Password">New Password</label>
        <input type="password" id="Password" name="Password" placeholder="Enter new password" required />
      </div>
      <div class="form-group">
        <label for="Confirm_password">Confirm Password</label>
        <input type="password" id="Confirm_password" name="Confirm_password" placeholder="Confirm new password" required />
      </div>
      <button type="submit" class="submit-btn">Reset Password</button>
      <button type="button" class="cancel-btn" id="cancelBtn">Cancel</button>
    </form>
    <div class="login-footer">
      Remembered your password? <a href="login-doctor.py">Login</a>
    </div>
  </div>
</div>

<!-- Footer -->
<div class="footer">
  <div class="footer-top">
    <div class="footer-left">
      <img src="logo.svg" alt="logofooter" class="footer-logo" />
      <p><strong>Prescriptive is your trusted doctor appointment platform. We connect you with 100+ verified doctors.</strong></p>
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
// Navbar dropdown
function toggleDropdown(id) {{
  document.querySelectorAll('.dropdown-content').forEach(el => {{
    if (el.id !== id) el.classList.remove('show');
  }});
  document.getElementById(id).classList.toggle('show');
}}

// Cancel button
document.getElementById("cancelBtn").addEventListener("click", function() {{
  window.location.href = "login-doctor.py";
}});
</script>

</body>
</html>
""")
