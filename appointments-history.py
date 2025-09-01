#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys, os, datetime
cgitb.enable()

# Database connection
con = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="appointment_booking_system"
)
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

print("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Appointment History</title>
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f8f9ff;
    }

    .dashboard-container {
      display: flex;
      min-height: 100vh;
    }

    /* Sidebar */
    .sidebar {
      background: #5f6FFF;
      color: #fff;
      width: 250px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      transition: transform 0.3s ease;
    }

    .sidebar-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .sidebar-header h2 {
      margin: 0;
      font-size: 20px;
    }

    .close-sidebar {
      background: none;
      border: none;
      font-size: 22px;
      color: white;
      cursor: pointer;
      display: none;
    }

    .sidebar-menu {
      list-style: none;
      padding: 0;
      margin-top: 20px;
    }

    .sidebar-menu li {
      margin-bottom: 15px;
    }

    .sidebar-menu a {
      text-decoration: none;
      color: white;
      font-size: 16px;
      padding: 12px;
      display: block;
      border-radius: 6px;
      transition: all 0.3s ease;
    }

    .sidebar-menu a:hover {
      background: #3d47d6;
      transform: translateX(5px);
    }

    .sidebar-menu a.active {
      background: #2a35c4;
    }

    /* Main Content */
    .main-content {
      flex: 1;
      padding: 20px;
    }

    .topbar {
      display: flex;
      align-items: center;
      justify-content: flex-start;
      flex-wrap: wrap;
      gap: 10px;
    }

    .menu-btn {
      background: #5f6FFF;
      color: #fff;
      padding: 10px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      display: none;
    }

    .mobile-heading {
      display: none;
      font-size: 18px;
      font-weight: bold;
      color: #333;
    }

    .desktop-heading {
      font-size: 24px;
      font-weight: bold;
      color: #333;
    }

    .content {
      margin-top: 20px;
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    h2 {
      margin-bottom: 20px;
      font-size: 22px;
    }

    /* Table Styling */
    .table-container {
      overflow-x: auto;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 1200px;
    }

    th, td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #ddd;
      font-size: 14px;
    }

    th {
      background: #5f6FFF;
      color: white;
    }

    tr:hover {
      background: #f1f1f1;
    }

    /* Responsive */
    @media (max-width: 768px) {
      .sidebar {
        position: fixed;
        left: 0;
        top: 0;
        height: 100%;
        transform: translateX(-100%);
        z-index: 1000;
      }

      .sidebar.open {
        transform: translateX(0);
      }

      .close-sidebar {
        display: block;
      }

      .menu-btn {
        display: inline-block;
      }

      .mobile-heading {
        display: inline-block;
      }

      .desktop-heading {
        display: none;
      }
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
      <li><a href="appointments-history.py" class="active">📅 Appointment History</a></li>
      <li><a href="upcoming-appointments.py">⏳ Upcoming Appointments</a></li>
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
      <span class="mobile-heading">Appointment History</span>
      <h1 class="desktop-heading">Appointment History</h1>
    </header>

    <section class="content">
      <h2>Completed Appointments</h2>
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
              <th>Consultation Given</th>
              <th>Fees (₹)</th>
            </tr>
          </thead>
          <tbody>
""")

# Fetch data from appointment_history table
query = """
SELECT d.Doctor_name, d.Specialization, p.Patient_name, 
       a.appointment_date, a.appointment_time, a.reason_for_booking, 
       a.consultation, a.amount
FROM appointment_history a
JOIN doctor_register d ON a.doctor_id = d.id
JOIN patient_register p ON a.patient_id = p.id
ORDER BY a.appointment_date DESC, a.appointment_time DESC
"""
cur.execute(query)
rows = cur.fetchall()

if rows:
    for row in rows:
        doctor_name = row[0]
        specialization = row[1]
        patient_name = row[2]
        appt_date = row[3].strftime("%Y-%m-%d") if isinstance(row[3], datetime.date) else str(row[3])

        # Handle TIME stored as timedelta
        appt_time = row[4]
        if isinstance(appt_time, datetime.timedelta):
            total_seconds = appt_time.seconds
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            period = "AM"
            if hours >= 12:
                period = "PM"
                if hours > 12:
                    hours -= 12
            if hours == 0:
                hours = 12
            appt_time_str = f"{hours:02}:{minutes:02} {period}"
        else:
            appt_time_str = str(appt_time)

        reason = row[5] if row[5] else "N/A"
        consultation = row[6] if row[6] else "N/A"
        fees = row[7] if row[7] else "0"

        print(f"""
            <tr>
              <td>{doctor_name}</td>
              <td>{specialization}</td>
              <td>{patient_name}</td>
              <td>{appt_date}</td>
              <td>{appt_time_str}</td>
              <td>{reason}</td>
              <td>{consultation}</td>
              <td>{fees}</td>
            </tr>
        """)
else:
    print("""
        <tr>
          <td colspan="8" style="text-align:center;">No appointment history found.</td>
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
