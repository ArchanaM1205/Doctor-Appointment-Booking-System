#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql,cgi,cgitb,sys,os
cgitb.enable()

# --- Connect to database ---
form=cgi.FieldStorage()
con=pymysql.connect(host="localhost",user="root",password="",database="appointment_booking_system")
cur=con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

# --- Get doctor ID safely ---
user_id=form.getvalue("id")
if isinstance(user_id, list):
    user_id=user_id[0]
user_id=int(user_id)

# --- Fetch doctor name ---
cur.execute("SELECT Doctor_name FROM doctor_register WHERE id=%s", (user_id,))
doctor = cur.fetchone()
doctor_name = doctor[0] if doctor else "Unknown"

# --- Fetch cancelled appointments for this doctor ---
cur.execute("""
    SELECT patient_name, age, dob, gender, appointment_date, appointment_time,
           reason_for_booking, reason_for_cancelling
    FROM cancelled_appointments
    WHERE doctor_id=%s
    ORDER BY appointment_date DESC
""", (user_id,))
cancelled_appointments = cur.fetchall()

# --- Start HTML output ---
print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Cancelled Appointments</title>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
    }}

    .dashboard-container {{
      display: flex;
      height: 100vh;
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

    /* Main content */
    .main-content {{
      flex: 1;
      background: #f8f9ff;
      padding: 20px;
      overflow-x: auto;
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
      overflow-x: auto;
    }}

    /* Table Styling */
    table {{
      width: 100%;
      border-collapse: collapse;
      min-width: 850px;
    }}

    table th, table td {{
      border: 1px solid #ddd;
      padding: 10px;
      text-align: left;
      font-size: 14px;
    }}

    table th {{
      background: #5f6FFF;
      color: #fff;
      position: sticky;
      top: 0;
    }}

    table tr:nth-child(even) {{
      background: #f2f2f2;
    }}

    table tr:hover {{
      background: #e6e6e6;
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

      table {{
        font-size: 12px;
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
      <li><a href="doctor-dashboard.py?id={user_id}">📊 Dashboard</a></li>
      <li><a href="doctor-appointment-history.py?id={user_id}">📅 Appointment History</a></li>
      <li><a href="doctor-upcoming-appointments.py?id={user_id}">⏳ Upcoming Appointments</a></li>
      <li><a href="doctor-cancelled-appointments.py?id={user_id}" class="active">❌ Cancelled Appointments</a></li>
      <li><a href="doctor-profile.py?id={user_id}">👤 Profile</a></li>
      <li><a href="index.py">🚪 Logout</a></li>
    </ul>
  </aside>

  <!-- Main Content -->
  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <h1>Cancelled Appointments</h1>
    </header>

    <section class="content">
      <h2>Rejected Appointments List</h2>
      <div style="overflow-x:auto;">
        <table>
          <thead>
            <tr>
              <th>Patient Name</th>
              <th>Age</th>
              <th>DOB</th>
              <th>Gender</th>
              <th>Date</th>
              <th>Time</th>
              <th>Reason for Booking</th>
              <th>Reason for Rejection</th>
            </tr>
          </thead>
          <tbody>
""")

# --- Populate table dynamically from database ---
if cancelled_appointments:
    for row in cancelled_appointments:
        patient_name, age, dob, gender, date, time, reason_booking, reason_cancelling = row
        print(f"""
            <tr>
              <td>{patient_name}</td>
              <td>{age}</td>
              <td>{dob}</td>
              <td>{gender}</td>
              <td>{date}</td>
              <td>{time}</td>
              <td>{reason_booking}</td>
              <td>{reason_cancelling}</td>
            </tr>
        """)
else:
    print('<tr><td colspan="8" style="text-align:center;">No cancelled appointments found.</td></tr>')

# --- Close HTML ---
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
