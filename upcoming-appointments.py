#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-Type: text/html\r\n\r\n")
import pymysql, cgi, cgitb, sys
from datetime import datetime, time

cgitb.enable()
form = cgi.FieldStorage()

# Database connection
con = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="appointment_booking_system"
)
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

# Fetch all upcoming appointments
cur.execute("""
    SELECT d.Doctor_name, d.Specialization, p.Patient_name, a.appointment_date, 
           a.appointment_time, a.reason, a.status, CONCAT(p.Email, ' | ', p.Phone)
    FROM appointments a
    JOIN doctor_register d ON a.doctor_id = d.id
    JOIN patient_register p ON a.patient_id = p.id
    WHERE a.appointment_date >= CURDATE()
    ORDER BY a.appointment_date, a.appointment_time
""")
appointments = cur.fetchall()

print("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Upcoming Appointments</title>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; background: #f8f9ff; }
    .dashboard-container { display: flex; min-height: 100vh; }
    .sidebar { background: #5f6FFF; color: #fff; width: 250px; padding: 20px; display: flex; flex-direction: column; transition: transform 0.3s ease; }
    .sidebar-header { display: flex; justify-content: space-between; align-items: center; }
    .sidebar-header h2 { margin: 0; font-size: 20px; }
    .close-sidebar { background: none; border: none; font-size: 22px; color: white; cursor: pointer; display: none; }
    .sidebar-menu { list-style: none; padding: 0; margin-top: 20px; }
    .sidebar-menu li { margin-bottom: 15px; }
    .sidebar-menu a { text-decoration: none; color: white; font-size: 16px; padding: 12px; display: block; border-radius: 6px; transition: all 0.3s ease; }
    .sidebar-menu a:hover { background: #3d47d6; transform: translateX(5px); }
    .sidebar-menu a.active { background: #2a35c4; }
    .main-content { flex: 1; padding: 20px; }
    .topbar { display: flex; align-items: center; justify-content: flex-start; flex-wrap: wrap; gap: 10px; }
    .menu-btn { background: #5f6FFF; color: #fff; padding: 10px; border: none; border-radius: 5px; cursor: pointer; display: none; }
    .mobile-heading { display: none; font-size: 18px; font-weight: bold; color: #333; }
    .desktop-heading { font-size: 24px; font-weight: bold; color: #333; }
    .content { margin-top: 20px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
    h2 { margin-bottom: 20px; font-size: 22px; }
    .table-container { overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; min-width: 1100px; }
    th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; font-size: 14px; }
    th { background: #5f6FFF; color: white; }
    tr:hover { background: #f1f1f1; }
    @media (max-width: 768px) {
      .sidebar { position: fixed; left: 0; top: 0; height: 100%; transform: translateX(-100%); z-index: 1000; }
      .sidebar.open { transform: translateX(0); }
      .close-sidebar { display: block; }
      .menu-btn { display: inline-block; }
      .mobile-heading { display: inline-block; }
      .desktop-heading { display: none; }
    }
  </style>
</head>
<body>
<div class="dashboard-container">
  <!-- Sidebar -->
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <h2>Admin Panel</h2>
      <button class="close-sidebar" onclick="toggleSidebar()">×</button>
    </div>
    <ul class="sidebar-menu">
      <li><a href="admin-dashboard.py">📊 Control Center</a></li>
      <li><a href="doctors.py">👨‍⚕️ Doctor Directory</a></li>
      <li><a href="patients.py">🧑‍🤝‍🧑 Patient Hub</a></li>
      <li><a href="appointments-history.py">📅 Appointment History</a></li>
      <li><a href="upcoming-appointments.py" class="active">⏳ Upcoming Appointments</a></li>
      <li><a href="cancelled-appointments.py">❌ Cancelled Appointments</a></li>
      <li><a href="add-doctor.py">➕ Add a Healer</a></li>
      <li><a href="add-patient.py">➕ Register Patient</a></li>
      <li><a href="index.py">🚪 Sign Out</a></li>
    </ul>
  </aside>

  <!-- Main Content -->
  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <span class="mobile-heading">Upcoming Appointments</span>
      <h1 class="desktop-heading">Upcoming Appointments</h1>
    </header>

    <section class="content">
      <h2>All Scheduled Appointments</h2>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Doctor Name</th>
              <th>Specialization</th>
              <th>Patient Name</th>
              <th>Date</th>
              <th>Time</th>
              <th>Reason</th>
              <th>Status</th>
              <th>Contact</th>
            </tr>
          </thead>
          <tbody>
""")

# Populate table rows dynamically with timedelta conversion
for appt in appointments:
    doctor_name = appt[0]
    specialization = appt[1]
    patient_name = appt[2]
    appt_date = appt[3].strftime("%Y-%m-%d")

    # Handle timedelta for appointment_time
    appt_time_td = appt[4]
    total_seconds = appt_time_td.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    appt_time = f"{(hours % 12) or 12}:{minutes:02d} {'AM' if hours < 12 else 'PM'}"

    reason = appt[5] if appt[5] else "General Checkup"
    status = appt[6]
    contact = appt[7]
    status_color = "green" if status.lower() == "confirmed" else "orange"

    print(f"""
            <tr>
              <td>{doctor_name}</td>
              <td>{specialization}</td>
              <td>{patient_name}</td>
              <td>{appt_date}</td>
              <td>{appt_time}</td>
              <td>{reason}</td>
              <td><span style="color: {status_color};">{status}</span></td>
              <td>{contact}</td>
            </tr>
    """)

print("""
          </tbody>
        </table>
      </div>
    </section>
  </main>
</div>

<script>
  function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("open");
  }
</script>

</body>
</html>
""")
