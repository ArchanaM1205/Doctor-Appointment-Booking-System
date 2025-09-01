#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys
cgitb.enable()

form = cgi.FieldStorage()
sys.stdout.reconfigure(encoding='utf-8')

# Get doctor id from query string
doctor_id = form.getvalue("id")

if not doctor_id:
    print("<h3 style='color:red;'>Error: Doctor ID not provided.</h3>")
    sys.exit()

# Connect to MySQL
con = pymysql.connect(host="localhost", user="root", password="", database="appointment_booking_system")
cur = con.cursor()

# Fetch doctor data
query = """
    SELECT id, Doctor_name, Specialization, Experience, Email, Phone, 
           Address_line1, Address_line2, Hospital_name, Hospital_address, 
           About, Profile_picture 
    FROM doctor_register
    WHERE id = %s
"""
cur.execute(query, (doctor_id,))
data = cur.fetchone()

# Default values if no record found
if data:
    (did, name, specialization, experience, email, phone,
     addr1, addr2, hospital_name, hospital_addr, about, image) = data
    profile_image = f"Doctor-register-images/{image}" if image else "Doctor-register-images/profile_pic.png"
else:
    did = 0
    name = specialization = experience = email = phone = addr1 = addr2 = hospital_name = hospital_addr = about = "N/A"
    profile_image = "Doctor-register-images/profile_pic.png"


print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Doctor Profile</title>
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

    /* Sidebar */
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

    /* Main Content */
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

    /* Profile Section */
    .content {{
      margin-top: 20px;
      background: white;
      padding: 30px 20px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      max-width: 650px;
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

    /* Responsive */
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
  <!-- Sidebar -->
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <h2>Prescripto</h2>
      <button class="close-sidebar" onclick="toggleSidebar()">×</button>
    </div>
    <ul class="sidebar-menu">
      <li><a href="doctor-dashboard.py?id={doctor_id}">📊 Dashboard</a></li>
      <li><a href="doctor-appointment-history.py?id={doctor_id}">📅 Appointment History</a></li>
      <li><a href="doctor-upcoming-appointments.py?id={doctor_id}">⏳ Upcoming Appointments</a></li>
      <li><a href="doctor-cancelled-appointments.py?id={doctor_id}">❌ Cancelled Appointments</a></li>
      <li><a href="doctor-profile.py?id={doctor_id}" class="active">👤 Profile</a></li>
      <li><a href="index.py">🚪 Logout</a></li>
    </ul>
  </aside>

  <!-- Main Content -->
  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <h1>Doctor Profile</h1>
    </header>

    <section class="content">
      <img src="{profile_image}" alt="Doctor Picture" class="profile-pic">
      <div class="profile-name">{name}</div>
      <div class="profile-details">
        <div class="profile-item"><strong>Specialization:</strong> {specialization}</div>
        <div class="profile-item"><strong>Experience:</strong> {experience} years</div>
        <div class="profile-item"><strong>Email:</strong> {email}</div>
        <div class="profile-item"><strong>Phone:</strong> {phone}</div>
        <div class="profile-item"><strong>Address Line 1:</strong> {addr1}</div>
        <div class="profile-item"><strong>Address Line 2:</strong> {addr2}</div>
        <div class="profile-item"><strong>Hospital Name:</strong> {hospital_name}</div>
        <div class="profile-item"><strong>Hospital Address:</strong> {hospital_addr}</div>
        <div class="profile-item" style="grid-column: span 2;"><strong>About:</strong> {about}</div>
      </div>
      <button class="edit-btn" onclick="window.location.href='doctor-edit-profile.py?id={doctor_id}'">Edit Profile</button>
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
