#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys, os, shutil
cgitb.enable()

form = cgi.FieldStorage()

# DB connection
con = pymysql.connect(host="localhost", user="root", password="", database="appointment_booking_system", charset="utf8mb4")
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

# ---------------- Handle Form Submission ----------------
msg = ""
if form.getvalue("submit"):
    # ✅ Convert all inputs to strings (avoids eval errors)
    def safe_get(field):
        val = form.getvalue(field)
        return str(val).strip() if val else None

    name = safe_get("fullname")
    dob = safe_get("dob")
    gender = safe_get("gender")
    marital = safe_get("marital")
    phone = safe_get("phone")
    email = safe_get("email")
    password = safe_get("password")
    cpassword = safe_get("cpassword")
    address1 = safe_get("address1")
    address2 = safe_get("address2")

    # File upload
    fileitem = form["profile"] if "profile" in form else None
    filename = None
    if fileitem is not None and fileitem.filename:
        upload_dir = "Patient-register-images"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        filename = os.path.basename(fileitem.filename)
        filepath = os.path.join(upload_dir, filename)
        with open(filepath, "wb") as f:
            shutil.copyfileobj(fileitem.file, f)

    # ✅ Password & Confirm Password Check
    if not password or not cpassword:
        msg = "<p style='color:red;text-align:center;'>❌ Password fields cannot be empty!</p>"
    elif password != cpassword:
        msg = "<p style='color:red;text-align:center;'>❌ Password and Confirm Password do not match!</p>"
    elif len(password) < 6:
        msg = "<p style='color:red;text-align:center;'>❌ Password must be at least 6 characters long!</p>"
    else:
        try:
            cur.execute("""
                INSERT INTO patient_register
                (Patient_name, Dob, Gender, Marital_Status, Phone, Email, Password, Confirm_password, Address_line1, Address_line2, Profile_image)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (name, dob, gender, marital, phone, email, password, cpassword, address1, address2, filename))
            con.commit()
            msg = "<p style='color:green;text-align:center;'>✅ Patient Registered Successfully!</p>"
        except Exception as e:
            msg = f"<p style='color:red;text-align:center;'>❌ Error: {str(e)}</p>"

# ---------------- Render HTML ----------------
print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Add Patient</title>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Outfit', sans-serif; background: #f8f9ff; }}
    .dashboard-container {{ display: flex; min-height: 100vh; }}
    .sidebar {{ background: #5f6FFF; color: #fff; width: 250px; padding: 20px; flex-shrink: 0; transition: transform 0.3s ease; }}
    .sidebar-header {{ display: flex; justify-content: space-between; align-items: center; }}
    .sidebar-header h2 {{ font-size: 20px; }}
    .close-sidebar {{ background: none; border: none; font-size: 22px; color: white; cursor: pointer; display: none; }}
    .sidebar-menu {{ list-style: none; padding: 0; margin-top: 20px; }}
    .sidebar-menu li {{ margin-bottom: 15px; }}
    .sidebar-menu a {{ text-decoration: none; color: white; font-size: 16px; padding: 12px; display: block; border-radius: 6px; transition: 0.3s; }}
    .sidebar-menu a:hover, .sidebar-menu a.active {{ background: #3d47d6; }}
    .main-content {{ flex: 1; padding: 20px; display: flex; flex-direction: column; align-items: center; }}
    .topbar {{ display: flex; align-items: center; gap: 10px; width: 100%; }}
    .menu-btn {{ background: #5f6FFF; color: #fff; padding: 10px; border: none; border-radius: 5px; cursor: pointer; display: none; }}
    .mobile-heading {{ display: none; font-size: 18px; font-weight: bold; color: #333; }}
    .desktop-heading {{ font-size: 24px; font-weight: bold; color: #333; }}
    .form-wrapper {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1); width: 100%; max-width: 1000px; margin-top: 20px; }}
    h2 {{ text-align: center; margin-bottom: 20px; font-size: 22px; color: #333; }}
    form {{ display: grid; gap: 20px; grid-template-columns: repeat(2, 1fr); }}
    label {{ font-weight: 600; font-size: 14px; margin-bottom: 6px; display: block; }}
    input, select {{ width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 8px; font-size: 14px; }}
    .form-buttons {{ grid-column: span 2; display: flex; justify-content: flex-end; gap: 12px; margin-top: 20px; }}
    .btn {{ padding: 12px 20px; font-size: 1rem; font-weight: 600; border: none; border-radius: 8px; cursor: pointer; width:100% }}
    .btn-submit {{ background: #5f6FFF; color: white; }}
    .btn-submit:hover {{ background: #3d47d6; }}
    .btn-cancel {{ background: red; color: white; }}
    .btn-cancel:hover {{ background: darkred; }}
    .full-width {{ grid-column: span 2; }}
    @media (max-width: 575px) {{ form {{ grid-template-columns: 1fr; }} .full-width, .form-buttons {{ grid-column: span 1; width: 100%; }} .form-buttons {{ flex-direction: column-reverse; align-items: stretch; }} .btn {{ width: 100%; }} }}
    @media (min-width: 576px) and (max-width: 767px) {{ form {{ grid-template-columns: 1fr; }} .full-width, .form-buttons {{ grid-column: span 1; width: 100%; }} .form-buttons {{ flex-direction: column-reverse; align-items: stretch; }} .btn {{ width: 100%; }} }}
    @media (min-width: 768px) and (max-width: 991px) {{ form {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (min-width: 992px) and (max-width: 1199px) {{ form {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (min-width: 1200px) {{ form {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (max-width: 767px) {{ .sidebar {{ position: fixed; left: 0; top: 0; height: 100%; transform: translateX(-100%); z-index: 1000; }} .sidebar.open {{ transform: translateX(0); }} .close-sidebar {{ display: block; }} .menu-btn {{ display: inline-block; }} .mobile-heading {{ display: inline-block; }} .desktop-heading {{ display: none; }} .form-wrapper {{ width: 95%; }} }}
  </style>
</head>
<body>
<div class="dashboard-container">
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <h2>Admin Panel</h2>
      <button class="close-sidebar" onclick="toggleSidebar()">&times;</button>
    </div>
    <ul class="sidebar-menu">
      <li><a href="admin-dashboard.py">📊 Control Center</a></li>
      <li><a href="doctors.py">👨‍⚕️ Doctor Directory</a></li>
      <li><a href="patients.py">🧑‍🤝‍🧑 Patient Hub</a></li>
      <li><a href="appointments-history.py">📅 Appointment History</a></li>
      <li><a href="upcoming-appointments.py">⏳ Upcoming Appointments</a></li>
      <li><a href="cancelled-appointments.py">❌ Cancelled Appointments</a></li>
      <li><a href="add-doctor.py">➕ Add Healer</a></li>
      <li><a href="add-patient.py" class="active">➕ Add Patient</a></li>
      <li><a href="index.py">🚪 Sign Out</a></li>
    </ul>
  </aside>

  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <span class="mobile-heading">Add Patient</span>
      <h1 class="desktop-heading">Add Patient</h1>
    </header>

    <section class="form-wrapper">
      <h2>Patient Registration Form</h2>
      {msg}
      <form method="post" enctype="multipart/form-data">
        <div><label>Full Name</label><input type="text" name="fullname" required></div>
        <div><label>Date of Birth</label><input type="date" name="dob" required></div>
        <div><label>Gender</label><select name="gender" required><option value="">Select</option><option>Male</option><option>Female</option><option>Other</option></select></div>
        <div><label>Marital Status</label><select name="marital" required><option value="">Select</option><option>Single</option><option>Married</option><option>Divorced</option><option>Widowed</option></select></div>
        <div><label>Phone</label><input type="tel" name="phone" required></div>
        <div><label>Email</label><input type="email" name="email" required></div>
        <div><label>Password</label><input type="password" name="password" required></div>
        <div><label>Confirm Password</label><input type="password" name="cpassword" required></div>
        <div><label>Address Line 1</label><input type="text" name="address1" required></div>
        <div><label>Address Line 2</label><input type="text" name="address2"></div>
        <div class="full-width"><label>Profile Picture</label><input type="file" name="profile" accept="image/*"></div>
        <div class="form-buttons">
          <input type="submit" name="submit" class="btn btn-submit" value="Add Patient">
          <button type="button" class="btn btn-cancel" onclick="window.location.href='patients.py'">Cancel</button>
        </div>
      </form>
    </section>
  </main>
</div>
<script>
  function toggleSidebar() {{
    document.getElementById("sidebar").classList.toggle("open");
  }}
</script>
</body>
</html>
""")
