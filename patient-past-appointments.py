#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")

import pymysql
import cgi
import cgitb
import sys
import os

cgitb.enable()
sys.stdout.reconfigure(encoding='utf-8')

# Get patient id from query string after login
form = cgi.FieldStorage()
user_id = form.getvalue("id")

# Connect to database
con = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="appointment_booking_system"
)
cur = con.cursor()

# =========================
# Fetch Finished Appointments from appointment_history
# =========================
finished_rows = []
if user_id:
    cur.execute("""
        SELECT doctor_name, specialization, appointment_date, appointment_time,
               reason_for_booking, consultation, prescription,
               medical_record
        FROM appointment_history
        WHERE patient_id = %s
        ORDER BY appointment_date DESC
    """, (user_id,))
    finished_rows = cur.fetchall()

# =========================
# Fetch Cancelled Appointments
# =========================
cancelled_rows = []
if user_id:
    cur.execute("""
        SELECT doctor_name, specialization, appointment_date, appointment_time,
               reason_for_booking, status, reason_for_cancelling
        FROM cancelled_appointments
        WHERE patient_id = %s
        ORDER BY appointment_date DESC
    """, (user_id,))
    cancelled_rows = cur.fetchall()

print(""" 
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Past Appointments</title>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; background: #f8f9ff; }
    .dashboard-container { display: flex; min-height: 100vh; }
    .sidebar { background: #5f6FFF; color: white; width: 250px; padding: 20px; display: flex; flex-direction: column; transition: transform 0.3s ease; }
    .sidebar-header { display: flex; justify-content: space-between; align-items: center; }
    .sidebar-header h2 { margin: 0; font-size: 20px; }
    .close-sidebar { background: none; border: none; font-size: 20px; color: white; cursor: pointer; display: none; }
    .sidebar-menu { list-style: none; padding: 0; margin-top: 20px; }
    .sidebar-menu li { margin-bottom: 15px; }
    .sidebar-menu a { text-decoration: none; color: white; font-size: 16px; padding: 10px; display: block; border-radius: 6px; transition: background 0.3s ease; }
    .sidebar-menu a:hover, .sidebar-menu a.active { background: #3d47d6; }
    .main-content { flex: 1; padding: 20px; overflow-y: auto; }
    .topbar { display: flex; align-items: center; justify-content: space-between; }
    .menu-btn { display: none; background: #5f6FFF; color: white; padding: 10px; border: none; border-radius: 5px; cursor: pointer; }
    h1.page-title { font-size: 28px; margin: 10px 0 20px; color: #333; text-align: center; }
    .content { margin-top: 20px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); max-width: 1200px; margin-left: auto; margin-right: auto; }
    h2.section-title { margin-top: 0; font-size: 22px; color: #5f6FFF; margin-bottom: 15px; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 30px; border-radius: 8px; overflow: hidden; }
    table th, table td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; font-size: 14px; }
    table th { background-color: #5f6FFF; color: white; font-weight: bold; }
    table tbody tr:nth-child(even) { background-color: #f2f2f2; }
    table tbody tr:hover { background-color: #e8ebff; transition: 0.2s; }
    .view-more-btn { background-color: #5f6FFF; color: white; padding: 6px 12px; border: none; border-radius: 4px; cursor: pointer; }
    .view-more-btn:hover { background-color: #3d47d6; }
    .modal { display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); }
    .modal-content { background: white; margin: 10% auto; padding: 20px; width: 90%; max-width: 500px; border-radius: 8px; position: relative; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }
    .modal-content h3 { margin-top: 0; color: #333; }
    .close-modal { position: absolute; top: 10px; right: 15px; font-size: 22px; cursor: pointer; color: #999; }
    .modal-content p { margin: 10px 0; }
    .modal-content a { color: #5f6FFF; text-decoration: underline; }
    @media (max-width: 1200px) {
      table, thead, tbody, th, td, tr { display: block; }
      thead { display: none; }
      tr { background: white; margin-bottom: 15px; border: 1px solid #ddd; padding: 10px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
      td { display: flex; justify-content: space-between; padding: 10px; border: none; border-bottom: 1px solid #eee; }
      td:last-child { border-bottom: none; }
      td:before { content: attr(data-label); font-weight: bold; color: #333; flex: 1; }
    }
    @media (max-width: 768px) {
      .sidebar { position: fixed; left: 0; top: 0; height: 100%; transform: translateX(-100%); z-index: 1000; }
      .sidebar.open { transform: translateX(0); }
      .close-sidebar { display: block; }
      .menu-btn { display: block; }
    }
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
      <li><a href="patient-dashboard.py?id=""" + str(user_id) + """">🏠 Dashboard</a></li>
      <li><a href="patient-upcoming-appointments.py?id=""" + str(user_id) + """">⏳ Upcoming Appointments</a></li>
      <li><a href="patient-book-appointments.py?id=""" + str(user_id) + """">📅 Book Appointments</a></li>
      <li><a href="patient-past-appointments.py?id=""" + str(user_id) + """" class="active">🗓 Past Appointments</a></li>
      <li><a href="patient-profile.py?id=""" + str(user_id) + """">👤 Profile</a></li>
      <li><a href="patient-medical-records.py?id=""" + str(user_id) + """">📄 Medical Records</a></li>
      <li><a href="index.py">🚪 Logout</a></li>
    </ul>
  </aside>

  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <h1 class="page-title">Past Appointments</h1>
    </header>

    <section class="content">
      <h2 class="section-title">✔ Finished Appointments</h2>
      <table>
        <thead>
          <tr>
            <th>Doctor Name</th>
            <th>Specialization</th>
            <th>Date</th>
            <th>Time</th>
            <th>Reason</th>
            <th>Consultation</th>
            <th>Finished</th>
            <th>Details</th>
          </tr>
        </thead>
        <tbody>
""")

# Finished appointments dynamic rows
if finished_rows:
    for row in finished_rows:
        doctor_name, specialization, date, time, reason, consultation, prescription, medical = row
        print(f"""
          <tr>
            <td data-label="Doctor Name">{doctor_name}</td>
            <td data-label="Specialization">{specialization}</td>
            <td data-label="Date">{date}</td>
            <td data-label="Time">{time}</td>
            <td data-label="Reason">{reason}</td>
            <td data-label="Consultation">{consultation or '—'}</td>
            <td data-label="Finished">Yes</td>
            <td data-label="Details">
              <button class="view-more-btn" onclick="openModal(
                '{doctor_name}',
                '{reason}',
                '{prescription or ''}',
                '{medical or ''}'
              )">View More</button>
            </td>
          </tr>
        """)
else:
    print("""
          <tr>
            <td colspan="8" style="text-align:center; color:#777;">No finished appointments found.</td>
          </tr>
    """)

print("""
        </tbody>
      </table>

      <h2 class="section-title">❌ Cancelled / Rejected Appointments</h2>
      <table>
        <thead>
          <tr>
            <th>Doctor Name</th>
            <th>Specialization</th>
            <th>Date</th>
            <th>Time</th>
            <th>Reason</th>
            <th>Status</th>
            <th>Remarks</th>
          </tr>
        </thead>
        <tbody>
""")

# Cancelled appointments dynamic rows
if cancelled_rows:
    for row in cancelled_rows:
        doctor_name, specialization, date, time, reason, status, remarks = row
        print(f"""
          <tr>
            <td data-label="Doctor Name">{doctor_name}</td>
            <td data-label="Specialization">{specialization}</td>
            <td data-label="Date">{date}</td>
            <td data-label="Time">{time}</td>
            <td data-label="Reason">{reason}</td>
            <td data-label="Status">{status}</td>
            <td data-label="Remarks">{remarks}</td>
          </tr>
        """)
else:
    print("""
          <tr>
            <td colspan="7" style="text-align:center; color:#777;">No cancelled/rejected appointments found.</td>
          </tr>
    """)

print("""
        </tbody>
      </table>
    </section>
  </main>
</div>

<div id="detailsModal" class="modal">
  <div class="modal-content">
    <span class="close-modal" onclick="closeModal()">&times;</span>
    <h3>Appointment Details</h3>
    <p id="modalDoctorName"><strong>Doctor:</strong></p>
    <p id="modalReason"><strong>Reason:</strong></p>
    <p id="modalPrescription" style="display:none;"><strong>Prescription:</strong> <a href="" target="_blank" id="prescriptionLink">View File</a></p>
    <p id="modalMedicalRecord" style="display:none;"><strong>Medical Record:</strong> <a href="" target="_blank" id="recordLink">View File</a></p>
  </div>
</div>

<script>
  function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("open");
  }

  function openModal(doctor, reason, prescriptionUrl, recordUrl) {
    document.getElementById("modalDoctorName").innerHTML = `<strong>Doctor:</strong> ${doctor}`;
    document.getElementById("modalReason").innerHTML = `<strong>Reason:</strong> ${reason}`;

    const presEl = document.getElementById("modalPrescription");
    const recEl = document.getElementById("modalMedicalRecord");

    if (prescriptionUrl && prescriptionUrl.trim()) {
      presEl.style.display = "block";
      document.getElementById("prescriptionLink").href = prescriptionUrl;
    } else {
      presEl.style.display = "none";
    }

    if (recordUrl && recordUrl.trim()) {
      recEl.style.display = "block";
      document.getElementById("recordLink").href = recordUrl;
    } else {
      recEl.style.display = "none";
    }

    document.getElementById("detailsModal").style.display = "block";
  }

  function closeModal() {
    document.getElementById("detailsModal").style.display = "none";
  }

  window.onclick = function(event) {
    const modal = document.getElementById("detailsModal");
    if (event.target === modal) {
      closeModal();
    }
  };
</script>

</body>
</html>
""")
