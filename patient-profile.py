#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")

import pymysql, cgi, cgitb, sys
cgitb.enable()

form = cgi.FieldStorage()

# Get patient ID from query string
patient_id = form.getvalue("id")

if not patient_id:
    print("<h3 style='color:red;'>Error: Patient ID not provided.</h3>")
    sys.exit()

# Connect to MySQL
con = pymysql.connect(host="localhost", user="root", password="", database="appointment_booking_system")
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

# Fetch patient data by ID
query = """
    SELECT id, Patient_name, Gender, Dob, Email, Phone, Address_line1, Address_line2, Profile_image, Marital_Status
    FROM patient_register
    WHERE id = %s
"""
cur.execute(query, (patient_id,))
data = cur.fetchone()

# Default values if no record found
if data:
    pid, name, gender, dob, email_db, phone, addr1, addr2, image, marital = data
    profile_image = f"Patient-register-images/{image}" if image else "Patient-register-images/profile_pic.png"
else:
    pid = 0
    name = gender = dob = email_db = phone = addr1 = addr2 = marital = "N/A"
    profile_image = "Patient-register-images/profile_pic.png"

# HTML and CSS
print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Patient Profile</title>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f8f9ff;
    }}
    .dashboard-container {{
      display: flex;
      min-height: 100vh;
    }}
    .sidebar {{
      background: #5f6FFF;
      color: white;
      width: 250px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      transition: transform 0.3s ease;
    }}
    .sidebar-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .sidebar-header h2 {{
      margin: 0;
      font-size: 20px;
    }}
    .close-sidebar {{
      background: none;
      border: none;
      font-size: 20px;
      color: white;
      cursor: pointer;
      display: none;
    }}
    .sidebar-menu {{
      list-style: none;
      padding: 0;
      margin-top: 20px;
    }}
    .sidebar-menu li {{
      margin-bottom: 15px;
    }}
    .sidebar-menu a {{
      text-decoration: none;
      color: white;
      font-size: 16px;
      padding: 10px;
      display: block;
      border-radius: 6px;
      transition: background 0.3s ease;
    }}
    .sidebar-menu a:hover,
    .sidebar-menu a.active {{
      background: #3d47d6;
    }}
    .main-content {{
      flex: 1;
      padding: 20px;
      overflow-y: auto;
    }}
    .topbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .menu-btn {{
      display: none;
      background: #5f6FFF;
      color: white;
      padding: 10px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }}
    .content {{
      margin-top: 20px;
      background: white;
      padding: 30px 20px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      max-width: 600px;
      margin-left: auto;
      margin-right: auto;
      text-align: center;
    }}
    .profile-pic {{
      width: 140px;
      height: 140px;
      border-radius: 50%;
      object-fit: cover;
      border: 4px solid #5f6FFF;
      margin-bottom: 15px;
    }}
    .profile-name {{
      font-size: 22px;
      font-weight: bold;
      color: #333;
      margin-bottom: 20px;
    }}
    .profile-details {{
      text-align: left;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 15px;
      margin-bottom: 30px;
    }}
    .profile-item {{
      background: #f4f5ff;
      padding: 12px;
      border-radius: 8px;
      font-size: 16px;
      color: #333;
    }}
    .profile-item strong {{
      display: block;
      font-size: 14px;
      color: #666;
      margin-bottom: 3px;
    }}
    .edit-btn {{
      background: #5f6FFF;
      color: white;
      padding: 12px 20px;
      border: none;
      border-radius: 6px;
      font-size: 16px;
      cursor: pointer;
      transition: background 0.3s ease;
    }}
    .edit-btn:hover {{
      background: #3d47d6;
    }}
    @media (max-width: 768px) {{
      .sidebar {{
        position: fixed;
        left: 0;
        top: 0;
        height: 100%;
        transform: translateX(-100%);
        z-index: 1000;
      }}
      .sidebar.open {{
        transform: translateX(0);
      }}
      .close-sidebar {{
        display: block;
      }}
      .menu-btn {{
        display: block;
      }}
      .profile-details {{
        grid-template-columns: 1fr;
      }}
    }}
    @media (max-width: 480px) {{
      .profile-name {{
        font-size: 18px;
      }}
      .profile-item {{
        font-size: 14px;
      }}
      .edit-btn {{
        font-size: 14px;
        padding: 10px;
      }}
    }}
  </style>
</head>
<body>

<div class="dashboard-container">
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <h2>Prescripto</h2>
      <button class="close-sidebar" onclick="toggleSidebar()">×</button>
    </div>
    <ul class="sidebar-menu">
      <li><a href="patient-dashboard.py?id={pid}">🏠 Dashboard</a></li>
      <li><a href="patient-upcoming-appointments.py?id={pid}">⏳ Upcoming Appointments</a></li>
      <li><a href="patient-book-appointments.py?id={pid}">📅 Book Appointments</a></li>
      <li><a href="patient-past-appointments.py?id={pid}">🗓 Past Appointments</a></li>
      <li><a href="patient-profile.py?id={pid}" class="active">👤 Profile</a></li>
      <li><a href="patient-medical-records.py?id={pid}">📄 Medical Records</a></li>
      <li><a href="index.py">🚪 Logout</a></li>
    </ul>
  </aside>

  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <h1>Patient Profile</h1>
    </header>

    <section class="content">
      <img src="{profile_image}" alt="Profile Picture" class="profile-pic">
      <div class="profile-name">{name}</div>
      <div class="profile-details">
        <div class="profile-item"><strong>Email:</strong> {email_db}</div>
        <div class="profile-item"><strong>Phone:</strong> {phone}</div>
        <div class="profile-item"><strong>Address Line 1:</strong> {addr1}</div>
        <div class="profile-item"><strong>Address Line 2:</strong> {addr2}</div>
        <div class="profile-item"><strong>Gender:</strong> {gender}</div>
        <div class="profile-item"><strong>Date of Birth:</strong> {dob}</div>
        <div class="profile-item"><strong>Marital Status:</strong> {marital}</div>
      </div>
      <button class="edit-btn" onclick="window.location.href='patient-edit-profile.py?id={pid}'">Edit Profile</button>
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
