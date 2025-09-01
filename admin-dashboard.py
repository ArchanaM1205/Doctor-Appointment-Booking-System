#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys, os
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

# ---------------- Fetch counts ----------------
# Doctors count
cur.execute("SELECT COUNT(*) FROM doctor_register")
doctor_count = cur.fetchone()[0]

# Patients count
cur.execute("SELECT COUNT(*) FROM patient_register")
patient_count = cur.fetchone()[0]

# Today's Appointments
cur.execute("SELECT COUNT(*) FROM appointments WHERE DATE(appointment_date) = CURDATE()")
today_appointments = cur.fetchone()[0]

# Weekly appointments (for chart)
cur.execute("""
    SELECT DAYNAME(appointment_date) as day, COUNT(*) 
    FROM appointments 
    WHERE YEARWEEK(appointment_date) = YEARWEEK(CURDATE())
    GROUP BY DAYOFWEEK(appointment_date)
    ORDER BY DAYOFWEEK(appointment_date)
""")
weekly_data = cur.fetchall()

# Convert weekly data into JS-friendly arrays
days = [row[0] for row in weekly_data]
counts = [row[1] for row in weekly_data]

# ---------------- HTML Output ----------------
print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Admin Dashboard</title>
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
      font-size: 20px;
    }}

    .close-sidebar {{
      background: none;
      border: none;
      font-size: 22px;
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
      padding: 12px;
      display: block;
      border-radius: 6px;
      transition: all 0.3s ease;
    }}

    .sidebar-menu a:hover {{
      background: #3d47d6;
      transform: translateX(5px);
    }}

    .sidebar-menu a.active {{
      background: #2a35c4;
    }}

    /* Main Content */
    .main-content {{
      flex: 1;
      padding: 20px;
    }}

    .topbar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
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

    .content {{
      margin-top: 20px;
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}

    .cards {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }}

    .card {{
      background: #eef1ff;
      padding: 20px;
      border-radius: 10px;
      text-align: center;
    }}

    .card h3 {{
      margin-bottom: 10px;
      color: #333;
    }}

    .card p {{
      font-size: 24px;
      font-weight: bold;
      color: #5f6FFF;
    }}

    .section-title {{
      margin-top: 40px;
      margin-bottom: 10px;
      font-size: 20px;
      font-weight: bold;
      color: #333;
    }}

    .activity-log {{
      list-style: none;
      padding-left: 20px;
    }}

    .activity-log li {{
      margin-bottom: 10px;
      color: #555;
    }}

    .chart-placeholder {{
      margin-top: 20px;
      height: 300px;
      background: #e4e7ff;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #666;
      font-style: italic;
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
    }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
      <li><a href="admin-dashboard.py" class="active">📊 Control Center</a></li>
      <li><a href="doctors.py">👨‍⚕️ Doctor Directory</a></li>
      <li><a href="patients.py">🧑‍🤝‍🧑 Patient Hub</a></li>
      <li><a href="appointments-history.py">📅 Appointment History</a></li>
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
      <h1>Admin Dashboard</h1>
    </header>

    <section class="content">
      <h2>Welcome, Admin</h2>
      <p>Select a menu item from the sidebar to manage doctors, patients, and more.</p>

      <div class="cards">
        <div class="card">
          <h3>Total Doctors</h3>
          <p>{doctor_count}</p>
        </div>
        <div class="card">
          <h3>Total Patients</h3>
          <p>{patient_count}</p>
        </div>
        <div class="card">
          <h3>Appointments Today</h3>
          <p>{today_appointments}</p>
        </div>
      </div>

      <div class="section-title">System Activity (Today)</div>
      <ul class="activity-log">
        <li>🧑‍⚕️ Doctor database updated</li>
        <li>🧑‍🤝‍🧑 Patient records refreshed</li>
        <li>📅 {today_appointments} appointments scheduled today</li>
      </ul>

      <div class="section-title">Weekly Overview</div>
      <canvas id="weeklyChart" class="chart-placeholder"></canvas>
    </section>
  </main>
</div>

<script>
  function toggleSidebar() {{
    document.getElementById("sidebar").classList.toggle("open");
  }}

  // Weekly Chart Data
  const ctx = document.getElementById('weeklyChart').getContext('2d');
  new Chart(ctx, {{
    type: 'bar',
    data: {{
      labels: {days},
      datasets: [{{
        label: 'Appointments',
        data: {counts},
        backgroundColor: '#5f6FFF'
      }}]
    }},
    options: {{
      responsive: true,
      plugins: {{
        legend: {{ display: false }}
      }}
    }}
  }});
</script>

</body>
</html>
""")
