#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys, datetime
cgitb.enable()

form = cgi.FieldStorage()
con = pymysql.connect(host="localhost", user="root", password="", database="appointment_booking_system")
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

# Get user_id safely
user_id = form.getvalue("id")
if isinstance(user_id, list):
    user_id = user_id[0]
user_id = int(user_id)

# --- Handle Accept (Update fees) ---
update_appointment_id = form.getvalue("appointment_id")
new_fee = form.getvalue("fee")
if update_appointment_id and new_fee:
    cur.execute("UPDATE appointments SET amount=%s WHERE id=%s", (new_fee, update_appointment_id))
    con.commit()

# --- Handle Reject (Move to cancelled_appointments) ---
reject_appointment_id = form.getvalue("reject_id")
reject_reason = form.getvalue("reject_reason")
if reject_appointment_id and reject_reason:
    # Get full appointment details
    cur.execute("""
        SELECT id, patient_id, doctor_id, patient_name, doctor_name, Age, specialization,
               reason, Dob, appointment_date, appointment_time, Gender, amount
        FROM appointments
        WHERE id=%s
    """, (reject_appointment_id,))
    appt = cur.fetchone()
    if appt:
        (appt_id, patient_id, doctor_id, patient_name, doctor_name, age, specialization,
         reason_for_booking, dob, appointment_date, appointment_time, gender, amount) = appt

        # Insert into cancelled_appointments with status='Cancelled'
        cur.execute("""
            INSERT INTO cancelled_appointments
            (patient_id, doctor_id, patient_name, doctor_name, age, specialization,
             reason_for_booking, reason_for_cancelling, dob, appointment_date, appointment_time, gender, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (patient_id, doctor_id, patient_name, doctor_name, age, specialization,
              reason_for_booking, reject_reason, dob, appointment_date, appointment_time, gender, "Cancelled"))
        con.commit()

        # Delete from appointments
        cur.execute("DELETE FROM appointments WHERE id=%s", (reject_appointment_id,))
        con.commit()

# --- Fetch doctor name ---
cur.execute("SELECT Doctor_name FROM doctor_register WHERE id=%s", (user_id,))
doctor = cur.fetchone()
doctor_name = doctor[0] if doctor else "Unknown"

# --- Fetch all upcoming appointments ---
today = datetime.date.today()
cur.execute("""
    SELECT id, patient_name, appointment_date, appointment_time, Dob, Gender, Age, reason, amount, status
    FROM appointments
    WHERE doctor_name=%s AND appointment_date >= %s
    ORDER BY appointment_date ASC
""", (doctor_name, today))
appointments = cur.fetchall()

# --- Start HTML ---
print("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Upcoming Appointments</title>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; }
    .dashboard-container { display: flex; height: 100vh; }
    .sidebar { background: #5f6FFF; color: #fff; width: 250px; padding: 20px; display: flex; flex-direction: column; transition: transform 0.3s ease; }
    .sidebar-header { display: flex; justify-content: space-between; align-items: center; }
    .sidebar-header h2 { margin: 0; }
    .close-sidebar { background: none; border: none; font-size: 20px; color: white; cursor: pointer; display: none; }
    .sidebar-menu { list-style: none; padding: 0; margin-top: 20px; }
    .sidebar-menu li { margin-bottom: 15px; }
    .sidebar-menu a { text-decoration: none; color: white; font-size: 16px; padding: 10px; display: block; border-radius: 6px; transition: background 0.3s ease; }
    .sidebar-menu a:hover, .sidebar-menu a.active { background: #3d47d6; }
    .main-content { flex: 1; background: #f8f9ff; padding: 20px; overflow-x: auto; }
    .topbar { display: flex; align-items: center; justify-content: space-between; }
    .menu-btn { display: none; background: #5f6FFF; color: #fff; padding: 10px; border: none; border-radius: 5px; cursor: pointer; }
    .content { margin-top: 20px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; min-width: 900px; }
    table th, table td { border: 1px solid #ddd; padding: 10px; text-align: left; font-size: 14px; }
    table th { background: #5f6FFF; color: #fff; position: sticky; top: 0; }
    table tr:nth-child(even) { background: #f2f2f2; }
    table tr:hover { background: #e6e6e6; }
    button.action-btn { padding: 5px 10px; margin: 2px; border: none; border-radius: 5px; cursor: pointer; font-size: 12px; }
    button.accept { background: #28a745; color: #fff; }
    button.reject { background: #dc3545; color: #fff; }
    .modal { display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); justify-content: center; align-items: center; }
    .modal-content { background: #fff; padding: 20px; border-radius: 8px; width: 300px; text-align: center; }
    .modal-content input, .modal-content textarea { width: 100%; padding: 8px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; }
    .modal-buttons { display: flex; justify-content: space-between; }
    .modal-buttons button { flex: 1; margin: 5px; padding: 8px; border: none; border-radius: 5px; cursor: pointer; }
    .save-btn { background: #28a745; color: #fff; }
    .cancel-btn { background: #6c757d; color: #fff; }
    .reject-btn { background: #dc3545; color: #fff; }
    @media (max-width: 768px) { .sidebar { position: fixed; left: 0; top: 0; height: 100%; transform: translateX(-100%); z-index: 1000; } .sidebar.open { transform: translateX(0); } .close-sidebar { display: block; } .menu-btn { display: block; } table { font-size: 12px; } }
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
      <li><a href="doctor-dashboard.py?id="""+str(user_id)+"""">📊 Dashboard</a></li>
      <li><a href="doctor-appointment-history.py?id="""+str(user_id)+"""">📅 Appointment History</a></li>
      <li><a href="doctor-upcoming-appointments.py?id="""+str(user_id)+"""" class="active">⏳ Upcoming Appointments</a></li>
      <li><a href="doctor-cancelled-appointments.py?id="""+str(user_id)+"""">❌ Cancelled Appointments</a></li>
      <li><a href="doctor-profile.py?id="""+str(user_id)+"""">👤 Profile</a></li>
      <li><a href="index.py">🚪 Logout</a></li>
    </ul>
  </aside>
  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <h1>Upcoming Appointments</h1>
    </header>
    <section class="content">
      <h2>Booked Appointments</h2>
      <div style="overflow-x:auto;">
        <table id="appointmentsTable">
          <thead>
            <tr>
              <th>Patient Name</th>
              <th>Date</th>
              <th>Time</th>
              <th>DOB</th>
              <th>Gender</th>
              <th>Age</th>
              <th>Reason</th>
              <th>Actions</th>
              <th id="feesHeader">Fees</th>
            </tr>
          </thead>
          <tbody>
""")

# --- Populate appointments table ---
for appt in appointments:
    appt_id, patient_name, date, time, dob, gender, age, reason, amount, status = appt
    fees_display = f"₹{amount}" if amount else ""
    accept_btn_display = "none" if amount or status=="Rejected" else "inline-block"
    reject_btn_display = "none" if status=="Rejected" else "inline-block"
    print(f"""
        <tr>
          <td>{patient_name}</td>
          <td>{date}</td>
          <td>{time}</td>
          <td>{dob}</td>
          <td>{gender}</td>
          <td>{age}</td>
          <td>{reason}</td>
          <td>
            <button class="action-btn accept" style="display:{accept_btn_display}" onclick="openFeesModal(this, {appt_id})">Accept</button>
            <button class="action-btn reject" style="display:{reject_btn_display}" onclick="openRejectModal(this, {appt_id})">Reject</button>
          </td>
          <td class="feesCell">{fees_display if status != 'Rejected' else 'Rejected'}</td>
        </tr>
    """)

if not appointments:
    print('<tr><td colspan="9" style="text-align:center;">No upcoming appointments found.</td></tr>')

# --- Closing HTML + JS ---
print("""
          </tbody>
        </table>
      </div>
    </section>
  </main>
</div>

<div class="modal" id="feesModal">
  <div class="modal-content">
    <h3>Set Appointment Fees</h3>
    <input type="number" id="feesInput" placeholder="Enter fees" />
    <div class="modal-buttons">
      <input type="submit" class="save-btn" onclick="saveFees()" value="Save">
      <input type="button" class="cancel-btn" onclick="closeModal('feesModal')" value="Cancel">
    </div>
  </div>
</div>

<div class="modal" id="rejectModal">
  <div class="modal-content">
    <h3>Reason for Rejection</h3>
    <textarea id="rejectReason" placeholder="Enter reason"></textarea>
    <div class="modal-buttons">
      <button class="reject-btn" onclick="rejectAppointment()">Reject</button>
      <button class="cancel-btn" onclick="closeModal('rejectModal')">Cancel</button>
    </div>
  </div>
</div>

<script>
let currentRow;
let currentAppointmentId;

function toggleSidebar() { document.getElementById("sidebar").classList.toggle("open"); }

function openFeesModal(button, apptId) {
  currentRow = button.closest("tr");
  currentAppointmentId = apptId;
  document.getElementById("feesModal").style.display = "flex";
}

function saveFees() {
  const fees = document.getElementById("feesInput").value;
  if (fees.trim() === "") return alert("Please enter fees.");
  const feesCell = currentRow.querySelector(".feesCell");
  feesCell.innerText = "₹" + fees;
  currentRow.querySelector(".accept").style.display = "none";

  const form = document.createElement("form");
  form.method = "post";
  form.style.display = "none";
  form.innerHTML = `
    <input type="hidden" name="id" value="${currentAppointmentId}">
    <input type="hidden" name="appointment_id" value="${currentAppointmentId}">
    <input type="hidden" name="fee" value="${fees}">
  `;
  document.body.appendChild(form);
  form.submit();
  closeModal('feesModal');
}

function openRejectModal(button, apptId) {
  currentRow = button.closest("tr");
  currentAppointmentId = apptId;
  document.getElementById("rejectModal").style.display = "flex";
}

function rejectAppointment() {
  const reason = document.getElementById("rejectReason").value;
  if (reason.trim() === "") return alert("Please enter a reason.");
  currentRow.style.backgroundColor = "#f8d7da";
  currentRow.querySelector(".accept").style.display = "none";
  currentRow.querySelector(".reject").style.display = "none";
  currentRow.querySelector(".feesCell").innerText = "Rejected";

  const form = document.createElement("form");
  form.method = "post";
  form.style.display = "none";
  form.innerHTML = `
    <input type="hidden" name="id" value="${currentAppointmentId}">
    <input type="hidden" name="reject_id" value="${currentAppointmentId}">
    <input type="hidden" name="reject_reason" value="${reason}">
  `;
  document.body.appendChild(form);
  form.submit();
  closeModal('rejectModal');
}

function closeModal(id) {
  document.getElementById(id).style.display = "none";
  document.getElementById("feesInput").value = "";
  document.getElementById("rejectReason").value = "";
}
</script>

</body>
</html>
""")
