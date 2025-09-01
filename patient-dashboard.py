#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-Type: text/html\r\n\r\n")
import pymysql, cgi, cgitb, sys
from datetime import datetime, time

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

# Get ID from query string
form = cgi.FieldStorage()
user_id = form.getvalue("id")

# Fetch patient details
q = """SELECT id, Patient_name, Gender, Email, Phone, Address_line1, Address_line2, Profile_image 
       FROM patient_register WHERE id=%s"""
cur.execute(q, (user_id,))
det = cur.fetchall()

for i in det:
    patient_id = i[0]
    patient_name = i[1] if i[1] else "Unknown"
    gender = i[2] if i[2] else "Not Updated"
    email = i[3] if i[3] else "Not Updated"
    phone = i[4] if i[4] else "Not Updated"
    address1 = i[5] if i[5] else "Not Updated"
    address2 = i[6] if i[6] else ""
    profile_image = i[7] if i[7] else "patient.png"
    image_path = f"Patient-register-images/{profile_image}"

    # Fetch counts for stats
    cur.execute("SELECT COUNT(*) FROM appointments WHERE patient_id=%s AND appointment_date >= CURDATE()", (patient_id,))
    upcoming_count = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM appointment_history WHERE patient_id=%s", (patient_id,))
    past_count = cur.fetchone()[0]

    print(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Patient Dashboard</title>
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
          justify-content: center;
          position: relative;
        }}
        .topbar h1 {{
          margin: 0;
          font-size: 24px;
          font-weight: bold;
          text-align: center;
          flex: 1;
        }}
        .menu-btn {{
          position: absolute;
          left: 0;
          background: #5f6FFF;
          color: white;
          padding: 10px 15px;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          display: none;
        }}
        .content {{
          margin-top: 20px;
        }}
        .cards {{
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 20px;
          margin-bottom: 30px;
        }}
        .card {{
          background: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 6px rgba(0,0,0,0.1);
          text-align: center;
        }}
        .card h3 {{
          margin: 0 0 10px;
          font-size: 20px;
          color: #333;
        }}
        .card p {{
          font-size: 24px;
          font-weight: bold;
          color: #5f6FFF;
          margin: 0;
        }}
        .appointments {{
          background: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 6px rgba(0,0,0,0.1);
          margin-bottom: 20px;
        }}
        .appointments h2 {{
          font-size: 20px;
          margin-bottom: 15px;
          color: #333;
        }}
        .appointment-item {{
          padding: 10px;
          border-bottom: 1px solid #eee;
        }}
        .appointment-item:last-child {{
          border-bottom: none;
        }}
        .appointment-item strong {{
          display: block;
          font-size: 16px;
          color: #333;
        }}
        .appointment-item span {{
          font-size: 14px;
          color: #666;
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
          .topbar h1 {{
            font-size: 20px;
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
          <li><a href="patient-dashboard.py?id={patient_id}" class="active">🏠 Dashboard</a></li>
          <li><a href="patient-upcoming-appointments.py?id={patient_id}">⏳ Upcoming Appointments</a></li>
          <li><a href="patient-book-appointments.py?id={patient_id}">📅 Book Appointments</a></li>
          <li><a href="patient-past-appointments.py?id={patient_id}">🗓 Past Appointments</a></li>
          <li><a href="patient-profile.py?id={patient_id}">👤 Profile</a></li>
          <li><a href="patient-medical-records.py?id={patient_id}">📄 Medical Records</a></li>
          <li><a href="index.py">🚪 Logout</a></li>
        </ul>
      </aside>
      <main class="main-content">
        <header class="topbar">
          <button class="menu-btn" onclick="toggleSidebar()">☰</button>
          <h1>Patient Dashboard</h1>
        </header>
        <section class="content">
          <div class="cards">
            <div class="card">
              <h3>Upcoming Appointments</h3>
              <p>{upcoming_count}</p>
            </div>
            <div class="card">
              <h3>Past Appointments</h3>
              <p>{past_count}</p>
            </div>
          </div>
          <div class="appointments">
            <h2>Next Appointments</h2>
    """)

    # Fetch actual upcoming appointments for this patient
    cur.execute("""SELECT d.Doctor_name, a.reason, a.appointment_date, a.appointment_time
                   FROM appointments a
                   JOIN doctor_register d ON a.doctor_id = d.id
                   WHERE a.patient_id=%s AND a.appointment_date >= CURDATE()
                   ORDER BY a.appointment_date, a.appointment_time""", (patient_id,))
    upcoming_appts = cur.fetchall()

    if upcoming_appts:
        for appt in upcoming_appts:
            doctor_name = appt[0]
            reason = appt[1] if appt[1] else "General Checkup"
            appt_date = appt[2].strftime("%Y-%m-%d")
            appt_time_obj = appt[3]
            hours, remainder = divmod(appt_time_obj.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            appt_time = datetime.combine(datetime.today(), time(hours, minutes)).strftime("%I:%M %p")

            print(f"""
            <div class="appointment-item">
              <strong>{doctor_name}</strong>
              <span>{reason} - {appt_date} at {appt_time}</span>
            </div>
            """)
    else:
        print("<p>No upcoming appointments.</p>")

    print("""
          </div>
          <div class="tips">
            <h2>Health Tips</h2>
            <ul>
              <li>Stay hydrated and drink at least 8 glasses of water daily.</li>
              <li>Get at least 7 hours of sleep every night.</li>
              <li>Exercise for at least 30 minutes daily.</li>
              <li>Eat a balanced diet rich in fruits and vegetables.</li>
            </ul>
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
