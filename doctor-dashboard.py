#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys
from datetime import datetime, time
cgitb.enable()
form = cgi.FieldStorage()

# ---------------- DB ----------------
con = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="appointment_booking_system"
)
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

user_id = form.getvalue("id")

# ---------------- Doctor Details ----------------
q = """SELECT id, Doctor_name, Specialization, Hospital_name, Hospital_address, Profile_picture
       FROM doctor_register WHERE id=%s"""
cur.execute(q, (user_id,))
det = cur.fetchall()

for i in det:
    doc_id = i[0]
    doc_name = i[1] if i[1] else "Dr. Unknown"
    specialization = i[2] if i[2] else "Specialization Not Updated"
    hospital = i[3] if i[3] else "Hospital/Clinic Not Updated"
    hospital_address = i[4] if i[4] else "Hospital Address"
    profile_image = i[5] if i[5] else "doc1.png"
    image_path = f"Doctor-register-images/{profile_image}"

# ---------------- Stats Counts ----------------
cur.execute("""SELECT COUNT(*) FROM appointments 
               WHERE doctor_id=%s AND appointment_date >= CURDATE() 
               AND appointment_date <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)""", (user_id,))
upcoming_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM appointment_history WHERE doctor_id=%s", (user_id,))
completed_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM cancelled_appointments WHERE doctor_id=%s", (user_id,))
cancelled_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(DISTINCT patient_id) FROM appointment_history WHERE doctor_id=%s", (user_id,))
patients_count = cur.fetchone()[0]

# ---------------- Upcoming Appointments ----------------
cur.execute("""SELECT p.Patient_name, a.reason, a.appointment_date, a.appointment_time
               FROM appointments a 
               JOIN patient_register p ON a.patient_id = p.id
               WHERE a.doctor_id=%s 
               AND a.appointment_date >= CURDATE() 
               AND a.appointment_date <= DATE_ADD(CURDATE(), INTERVAL 7 DAY)
               ORDER BY a.appointment_date, a.appointment_time""", (user_id,))
upcoming_appts = cur.fetchall()

# ---------------- HTML ----------------
print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Doctor Dashboard</title>
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
      color: #fff;
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
    }}
    .topbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 20px;
    }}
    .menu-btn {{
      display: none;
      background: #5f6FFF;
      color: #fff;
      padding: 10px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }}
    .profile-card {{
      display: flex;
      align-items: center;
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
      margin-bottom: 20px;
    }}
    .profile-card img {{
      width: 80px;
      height: 80px;
      border-radius: 50%;
      margin-right: 20px;
      object-fit: cover;
    }}
    .profile-info h2 {{
      margin: 0;
      font-size: 20px;
      color: #333;
    }}
    .profile-info p {{
      margin: 4px 0;
      font-size: 14px;
      color: #666;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin-bottom: 20px;
    }}
    .stat-card {{
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
      text-align: center;
    }}
    .stat-card h3 {{
      margin: 0;
      font-size: 18px;
      color: #333;
    }}
    .stat-card p {{
      font-size: 24px;
      font-weight: bold;
      margin: 10px 0 0;
      color: #5f6FFF;
    }}
    .appointments {{
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    }}
    .appointments h3 {{
      margin: 0 0 15px;
      font-size: 18px;
      color: #333;
    }}
    .appointment-card {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px;
      border-bottom: 1px solid #eee;
    }}
    .appointment-left {{
      display: flex;
      align-items: center;
    }}
    .avatar {{
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: #5f6FFF;
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      margin-right: 12px;
    }}
    .appointment-info {{
      display: flex;
      flex-direction: column;
    }}
    .appointment-info strong {{
      font-size: 16px;
      color: #333;
    }}
    .appointment-info span {{
      font-size: 13px;
      color: #666;
    }}
    .appointment-time {{
      font-size: 14px;
      color: #5f6FFF;
      font-weight: bold;
      margin-bottom: 5px;
    }}
    .view-btn {{
      background: #5f6FFF;
      color: white;
      padding: 6px 12px;
      border: none;
      border-radius: 4px;
      font-size: 14px;
      cursor: pointer;
    }}
    .view-btn:hover {{
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
      .profile-card {{
        flex-direction: column;
        text-align: center;
      }}
      .profile-card img {{
        margin-bottom: 10px;
      }}
      .appointment-card {{
        flex-direction: column;
        align-items: flex-start;
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
      <li><a href="doctor-dashboard.py?id={user_id}" class="active">📊 Dashboard</a></li>
      <li><a href="doctor-appointment-history.py?id={user_id}">📅 Appointment History</a></li>
      <li><a href="doctor-upcoming-appointments.py?id={user_id}">⏳ Upcoming Appointments</a></li>
      <li><a href="doctor-cancelled-appointments.py?id={user_id}">❌ Cancelled Appointments</a></li>
      <li><a href="doctor-profile.py?id={user_id}">👤 Profile</a></li>
      <li><a href="index.py">🚪 Logout</a></li>
    </ul>
  </aside>

  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <h1>Doctor Dashboard</h1>
    </header>

    <!-- Profile -->
    <div class="profile-card">
      <img src="{image_path}" alt="Doctor">
      <div class="profile-info">
        <h2>{doc_name}</h2>
        <p>{specialization} | {hospital}</p>
        <p>{hospital_address}</p>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats">
      <div class="stat-card">
        <h3>Upcoming Appointments</h3>
        <p>{upcoming_count}</p>
      </div>
      <div class="stat-card">
        <h3>Completed Appointments</h3>
        <p>{completed_count}</p>
      </div>
      <div class="stat-card">
        <h3>Cancelled Appointments</h3>
        <p>{cancelled_count}</p>
      </div>
      <div class="stat-card">
        <h3>Total Patients</h3>
        <p>{patients_count}</p>
      </div>
    </div>

    <!-- Upcoming Appointments (within 7 days) -->
    <div class="appointments">
      <h3>Upcoming Appointments (Next 7 Days)</h3>
""")

if upcoming_appts:
    for appt in upcoming_appts:
        pname = appt[0]
        reason = appt[1] if appt[1] else "General Checkup"
        appt_date = appt[2].strftime("%d-%b-%Y")

        # ---- FIX: Convert timedelta to 12-hour format ----
        appt_time_obj = appt[3]
        hours, remainder = divmod(appt_time_obj.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        appt_time = datetime.combine(datetime.today(), time(hours, minutes)).strftime("%I:%M %p")

        initial = pname[0].upper()

        print(f"""
        <div class="appointment-card">
          <div class="appointment-left">
            <div class="avatar">{initial}</div>
            <div class="appointment-info">
              <strong>{pname}</strong>
              <span>{reason}</span>
            </div>
          </div>
          <div>
            <div class="appointment-time">{appt_date} {appt_time}</div>
            <button class="view-btn">View</button>
          </div>
        </div>
        """)
else:
    print("<p>No upcoming appointments in the next 7 days.</p>")

print(f"""
    </div>
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
