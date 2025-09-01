#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys, os, shutil
cgitb.enable()

form = cgi.FieldStorage()
con = pymysql.connect(host="localhost", user="root", password="", database="appointment_booking_system")
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

# Create folder for doctor images if not exists
upload_dir = "Doctor-register-images"
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

# Handle form submission
if "name" in form:
    name = form.getvalue("name")
    dob = form.getvalue("dob")
    gender = form.getvalue("gender")
    specialization = form.getvalue("specialization")
    experience = form.getvalue("experience")
    phone = form.getvalue("phone")
    email = form.getvalue("email")
    password = form.getvalue("password")
    address1 = form.getvalue("address1")
    address2 = form.getvalue("address2")
    hospital = form.getvalue("hospital")
    hospitalAddress = form.getvalue("hospitalAddress")
    about = form.getvalue("about")

    # Handle file upload
    profilePic = form["profilePic"] if "profilePic" in form else None
    profile_filename = None
    if profilePic is not None and profilePic.filename:
        profile_filename = os.path.basename(profilePic.filename)
        save_path = os.path.join(upload_dir, profile_filename)
        with open(save_path, "wb") as f:
            shutil.copyfileobj(profilePic.file, f)

    # Insert into doctor_register
    cur.execute("""
        INSERT INTO doctor_register 
        (Doctor_name, DOB, Gender, Specialization, Experience, Phone, Email, Password, Address_line1, Address_line2, Hospital_name, Hospital_address, About, Profile_picture)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (name, dob, gender, specialization, experience, phone, email, password, address1, address2, hospital, hospitalAddress, about, profile_filename))
    con.commit()

    print("<script>alert('Doctor added successfully!');window.location.href='doctors.py';</script>")
    sys.exit()

# ---------------- HTML CONTENT (Unchanged) ----------------
print("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Add Doctor</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Outfit', sans-serif; background: #f8f9ff; }
    .dashboard-container { display: flex; min-height: 100vh; }
    .sidebar { background: #5f6FFF; color: #fff; width: 250px; padding: 20px; flex-shrink: 0; transition: transform 0.3s ease; }
    .sidebar-header { display: flex; justify-content: space-between; align-items: center; }
    .sidebar-header h2 { margin: 0; font-size: 20px; }
    .close-sidebar { background: none; border: none; font-size: 22px; color: white; cursor: pointer; display: none; }
    .sidebar-menu { list-style: none; padding: 0; margin-top: 20px; }
    .sidebar-menu li { margin-bottom: 15px; }
    .sidebar-menu a { text-decoration: none; color: white; font-size: 16px; padding: 12px; display: block; border-radius: 6px; transition: all 0.3s ease; }
    .sidebar-menu a:hover { background: #3d47d6; transform: translateX(5px); }
    .sidebar-menu a.active { background: #2a35c4; }
    .main-content { flex: 1; padding: 20px; display: flex; flex-direction: column; align-items: center; }
    .topbar { display: flex; align-items: center; gap: 10px; width: 100%; }
    .menu-btn { background: #5f6FFF; color: #fff; padding: 10px; border: none; border-radius: 5px; cursor: pointer; display: none; }
    .mobile-heading { display: none; font-size: 18px; font-weight: bold; color: #333; }
    .desktop-heading { font-size: 24px; font-weight: bold; color: #333; }
    .form-wrapper { background: white; padding: 30px; border-radius: 12px; box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.1); width: 100%; max-width: 1000px; margin-top: 20px; }
    h2 { text-align: center; margin-bottom: 20px; font-size: 22px; color: #333; }
    form { display: grid; gap: 20px; grid-template-columns: repeat(2, 1fr); }
    label { font-weight: 600; font-size: 14px; margin-bottom: 6px; display: block; }
    input, select, textarea { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 8px; font-size: 14px; transition: all 0.3s ease; }
    input:focus, select:focus, textarea:focus { border-color: #5f6FFF; outline: none; box-shadow: 0 0 5px rgba(95, 111, 255, 0.3); }
    .form-buttons { grid-column: span 2; display: flex; justify-content: flex-end; gap: 12px; margin-top: 20px; width: 60%; }
    .btn { padding: 12px 20px; font-size: 1rem; font-weight: 600; border: none; border-radius: 8px; cursor: pointer; transition: background 0.3s ease; }
    .btn-submit { background: #5f6FFF; color: white; }
    .btn-submit:hover { background: #3d47d6; }
    .btn-cancel { background: red; color: white; }
    .btn-cancel:hover { background: darkred; }
    .full-width { grid-column: span 2; }
    @media (max-width: 575px) { form { grid-template-columns: 1fr; } .full-width, .form-buttons { grid-column: span 1; width: 100%; } .form-buttons { flex-direction: column-reverse; align-items: stretch; } .btn { width: 100%; } }
    @media (min-width: 576px) and (max-width: 767px) { form { grid-template-columns: 1fr; } .full-width, .form-buttons { grid-column: span 1; width: 100%; } .form-buttons { flex-direction: column-reverse; align-items: stretch; } .btn { width: 100%; } }
    @media (min-width: 768px) and (max-width: 991px) { form { grid-template-columns: repeat(2, 1fr); } }
    @media (min-width: 992px) and (max-width: 1199px) { form { grid-template-columns: repeat(2, 1fr); } }
    @media (min-width: 1200px) { form { grid-template-columns: repeat(2, 1fr); } }
    @media (max-width: 767px) { .sidebar { position: fixed; left: 0; top: 0; height: 100%; transform: translateX(-100%); z-index: 1000; } .sidebar.open { transform: translateX(0); } .close-sidebar { display: block; } .menu-btn { display: inline-block; } .mobile-heading { display: inline-block; } .desktop-heading { display: none; } .form-wrapper { width: 95%; } }
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
      <li><a href="add-doctor.py" class="active">➕ Add Healer</a></li>
      <li><a href="add-patient.py">➕ Add Patient</a></li>
      <li><a href="index.py">🚪 Sign Out</a></li>
    </ul>
  </aside>

  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <span class="mobile-heading">Add Doctor</span>
      <h1 class="desktop-heading">Add Doctor</h1>
    </header>

    <section class="form-wrapper">
      <h2>Doctor Registration Form</h2>
      <form id="addDoctorForm" method="post" enctype="multipart/form-data">
        <div><label for="name">Full Name</label><input type="text" name="name" id="name" required /></div>
        <div><label for="dob">Date of Birth</label><input type="date" name="dob" id="dob" required /></div>
        <div><label for="gender">Gender</label><select name="gender" id="gender" required><option value="">Select</option><option>Male</option><option>Female</option><option>Other</option></select></div>
        <div><label for="specialization">Specialization</label><input type="text" name="specialization" id="specialization" required /></div>
        <div><label for="experience">Experience (Years)</label><input type="number" name="experience" id="experience" required /></div>
        <div><label for="phone">Phone</label><input type="tel" name="phone" id="phone" pattern="[0-9]{10}" max_length="10" required /></div>
        <div><label for="email">Email</label><input type="email" name="email" id="email" required /></div>
        <div><label for="password">Password</label><input type="password" name="password" id="password" required /></div>
        <div><label for="confirmPassword">Confirm Password</label><input type="password" id="confirmPassword" required /></div>
        <div><label for="address1">Address Line 1</label><input type="text" name="address1" id="address1" required /></div>
        <div><label for="address2">Address Line 2</label><input type="text" name="address2" id="address2" /></div>
        <div><label for="hospital">Hospital Name</label><input type="text" name="hospital" id="hospital" /></div>
        <div><label for="hospitalAddress">Hospital Address</label><input type="text" name="hospitalAddress" id="hospitalAddress" /></div>
        <div class="full-width"><label for="about">About</label><textarea name="about" id="about" rows="3"></textarea></div>
        <div class="full-width"><label for="profilePic">Profile Picture</label><input type="file" name="profilePic" id="profilePic" accept="image/*" /></div>
        <div class="form-buttons">
          <button type="submit" class="btn btn-submit">Submit</button>
          <button type="button" class="btn btn-cancel" onclick="goBack()">Cancel</button>
        </div>
      </form>
    </section>
  </main>
</div>

<script>
  function toggleSidebar() { document.getElementById("sidebar").classList.toggle("open"); }
  function goBack() { window.location.href = "admin-dashboard.py"; }
  document.getElementById("addDoctorForm").addEventListener("submit", function (e) {
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirmPassword").value;
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      e.preventDefault();
      return false;
    }
  });
</script>
</body>
</html>
""")
