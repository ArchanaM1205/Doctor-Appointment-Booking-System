#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys
import datetime
cgitb.enable()

form = cgi.FieldStorage()

con = pymysql.connect(host="localhost", user="root", password="", database="appointment_booking_system")
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

user_id = form.getvalue("id")

# Fetch patient name from patient_register
cur.execute("SELECT Patient_name FROM patient_register WHERE id=%s", (user_id,))
patient = cur.fetchone()
patient_name = patient[0] if patient else "Unknown"

# Fetch upcoming appointments for this patient
today = datetime.date.today()
cur.execute("""
    SELECT patient_name, doctor_name, Age, Gender, Specialization, Dob, Hospital_name, Hospital_address, 
           amount, reason, medical_records, appointment_time, appointment_date
    FROM appointments
    WHERE patient_name=%s AND appointment_date >= %s
    ORDER BY appointment_date ASC
""", (patient_name, today))
appointments = cur.fetchall()

# Start HTML output
print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Upcoming Appointments</title>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f8f9ff;
    }}

    .dashboard-container {{
      display: flex;
      height: 100vh;
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

    .content {{
      margin-top: 20px;
      background: white;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}

    h2 {{
      margin-top: 0;
    }}

    /* Table Styles */
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 15px;
      border-radius: 8px;
      overflow: hidden;
    }}

    table th, table td {{
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }}

    table th {{
      background-color: #5f6FFF;
      color: white;
      font-weight: bold;
    }}

    table tbody tr:nth-child(even) {{
      background-color: #f2f2f2;
    }}

    table tbody tr:hover {{
      background-color: #e8ebff;
      transition: 0.2s;
    }}

    /* Responsive Table */
    @media (max-width: 1024px) {{
      table, thead, tbody, th, td, tr {{
        display: block;
      }}
      thead tr {{
        display: none;
      }}
      tr {{
        background: white;
        margin-bottom: 15px;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
      }}
      td {{
        display: flex;
        justify-content: space-between;
        padding: 10px;
        border: none;
        border-bottom: 1px solid #eee;
      }}
      td:last-child {{
        border-bottom: none;
      }}
      td:before {{
        content: attr(data-label);
        font-weight: bold;
        color: #333;
      }}
    }}

    /* Sidebar Responsive */
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
      <li><a href="patient-dashboard.py?id={user_id}">🏠 Dashboard</a></li>
      <li><a href="patient-upcoming-appointments.py?id={user_id}" class="active">⏳ Upcoming Appointments</a></li>
      <li><a href="patient-book-appointments.py?id={user_id}">📅 Book Appointments</a></li>
      <li><a href="patient-past-appointments.py?id={user_id}">🗓 Past Appointments</a></li>
      <li><a href="patient-profile.py?id={user_id}">👤 Profile</a></li>
      <li><a href="patient-medical-records.py?id={user_id}">📄 Medical Records</a></li>
      <li><a href="index.py">🚪 Logout</a></li>
    </ul>
  </aside>

  <!-- Main Content -->
  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <h1>Upcoming Appointments</h1>
    </header>

    <section class="content">
      <h2>Your Upcoming Appointments</h2>
      <table>
        <thead>
          <tr>
            <th>Patient Name</th>
            <th>Doctor Name</th>
            <th>Age</th>
            <th>Gender</th>
            <th>Specialization</th>
            <th>DOB</th>
            <th>Hospital</th>
            <th>Hospital Address</th>
            <th>Fees (₹)</th>
            <th>Reason</th>
            <th>Appointment Time</th>
            <th>Appointment Date</th>
          </tr>
        </thead>
        <tbody>
""")

# Populate table rows
if appointments:
    for appt in appointments:
        (patient_name, doctor_name, age, gender, specialization, dob, hospital, hospital_address,
         amount, reason, medical_records, appt_time, appt_date) = appt
        print(f"""
          <tr>
            <td data-label="Patient Name">{patient_name}</td>
            <td data-label="Doctor Name">{doctor_name}</td>
            <td data-label="Age">{age}</td>
            <td data-label="Gender">{gender}</td>
            <td data-label="Specialization">{specialization}</td>
            <td data-label="DOB">{dob}</td>
            <td data-label="Hospital">{hospital}</td>
            <td data-label="Hospital Address">{hospital_address}</td>
            <td data-label="Fees (₹)">₹{amount}</td>
            <td data-label="Reason">{reason}</td>
            <td data-label="Appointment Time">{appt_time}</td>
            <td data-label="Appointment Date">{appt_date}</td>
          </tr>
        """)
else:
    print("""
          <tr>
            <td colspan="12" style="text-align:center;">No upcoming appointments found.</td>
          </tr>
    """)

# Close table and HTML
print("""
        </tbody>
      </table>
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
