#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-Type: text/html\r\n\r\n")
import pymysql, cgi, cgitb, sys

cgitb.enable()
form = cgi.FieldStorage()
doctor_id = form.getvalue('delete_id')  # For deletion
reason = form.getvalue('reason')        # Reason for deletion

# Database connection
con = pymysql.connect(host="localhost", user="root", password="", database="appointment_booking_system")
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

def safe(v):
    return "" if v is None else v

# --- Handle deletion if delete_id is provided ---
if doctor_id and reason:
    doctor_id = int(doctor_id)

    # Fetch doctor's current record
    cur.execute("SELECT * FROM doctor_register WHERE id=%s", (doctor_id,))
    doctor = cur.fetchone()

    if doctor:
        # Count appointments
        cur.execute("SELECT COUNT(*) FROM appointments WHERE doctor_id=%s", (doctor_id,))
        approved_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM cancelled_appointments WHERE doctor_id=%s", (doctor_id,))
        cancelled_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM appointment_history WHERE doctor_id=%s", (doctor_id,))
        completed_count = cur.fetchone()[0]

        # Insert into deleted_doctors with deleted_reason included
        cur.execute("""
            INSERT INTO deleted_doctors
            (Doctor_name, DOB, Gender, Specialization, Experience,
             Address_line1, Address_line2, Email, Phone,
             Hospital_name, Hospital_address, deletion_reason)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            safe(doctor[1]),   # Doctor_name
            safe(doctor[7]),   # DOB
            safe(doctor[8]),   # Gender
            safe(doctor[5]),   # Specialization
            safe(doctor[6]),   # Experience
            safe(doctor[9]),   # Address_line1
            safe(doctor[10]),  # Address_line2
            safe(doctor[2]),   # Email
            safe(doctor[11]),  # Phone
            safe(doctor[12]),  # Hospital_name
            safe(doctor[13]),  # Hospital_address
            reason.strip()     # deleted_reason (from modal textarea)
        ))

        # Delete doctor from active table
        cur.execute("DELETE FROM doctor_register WHERE id=%s", (doctor_id,))
        con.commit()

    # Redirect after deletion
    print("<script>window.location.href='doctors.py';</script>")
    sys.exit()

# --- Fetch all doctors ---
cur.execute("SELECT * FROM doctor_register")
doctors = cur.fetchall()

# --- HTML Output ---
print("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Doctor List</title>
  <style>
    body { margin:0; font-family:Arial,sans-serif; background:#f8f9ff; }
    .dashboard-container { display:flex; min-height:100vh; }
    .sidebar { background:#5f6FFF; color:#fff; width:250px; padding:20px; display:flex; flex-direction:column; transition: transform 0.3s ease; }
    .sidebar-header { display:flex; justify-content:space-between; align-items:center; }
    .sidebar-header h2 { margin:0; font-size:20px; }
    .close-sidebar { background:none; border:none; font-size:22px; color:white; cursor:pointer; display:none; }
    .sidebar-menu { list-style:none; padding:0; margin-top:20px; }
    .sidebar-menu li { margin-bottom:15px; }
    .sidebar-menu a { text-decoration:none; color:white; font-size:16px; padding:12px; display:block; border-radius:6px; transition: all 0.3s ease; }
    .sidebar-menu a:hover { background:#3d47d6; transform:translateX(5px); }
    .sidebar-menu a.active { background:#2a35c4; }
    .main-content { flex:1; padding:20px; }
    .topbar { display:flex; align-items:center; justify-content:flex-start; flex-wrap:wrap; gap:10px; }
    .menu-btn { background:#5f6FFF; color:#fff; padding:10px; border:none; border-radius:5px; cursor:pointer; display:none; }
    .mobile-heading { display:none; font-size:18px; font-weight:bold; color:#333; }
    .desktop-heading { font-size:24px; font-weight:bold; color:#333; }
    .content { margin-top:20px; background:white; padding:20px; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,0.1); }
    h2 { margin-bottom:20px; font-size:22px; }
    .table-container { overflow-x:auto; }
    table { width:100%; border-collapse:collapse; min-width:900px; }
    th, td { padding:12px; text-align:left; border-bottom:1px solid #ddd; font-size:14px; }
    th { background:#5f6FFF; color:white; }
    tr:hover { background:#f1f1f1; }
    .delete-btn { background-color:#ff4c4c; color:white; border:none; padding:6px 12px; border-radius:5px; cursor:pointer; font-size:13px; }
    .delete-btn:hover { background-color:#d93636; }
    .modal { display:none; position:fixed; z-index:2000; left:0; top:0; width:100%; height:100%; overflow:auto; background-color:rgba(0,0,0,0.5); }
    .modal-content { background-color:#fff; margin:10% auto; padding:20px; border-radius:8px; width:90%; max-width:400px; position:relative; box-shadow:0 4px 12px rgba(0,0,0,0.2); }
    .modal-content h3 { margin-top:0; color:#333; }
    .modal-content textarea { width:100%; padding:10px; margin-top:8px; border-radius:4px; border:1px solid #ccc; }
    .confirm-delete { background-color:#5f6FFF; color:#fff; padding:10px; border:none; border-radius:5px; margin-top:12px; cursor:pointer; width:100%; }
    .close-modal { position:absolute; right:12px; top:10px; font-size:22px; cursor:pointer; color:#666; }
    .profile-pic { width:50px; height:50px; border-radius:50%; object-fit:cover; }
    @media (max-width:768px) {
      .sidebar { position:fixed; left:0; top:0; height:100%; transform:translateX(-100%); z-index:1000; }
      .sidebar.open { transform:translateX(0); }
      .close-sidebar { display:block; }
      .menu-btn { display:inline-block; }
      .mobile-heading { display:inline-block; }
      .desktop-heading { display:none; }
    }
  </style>
</head>
<body>
<div class="dashboard-container">
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <h2>Admin Panel</h2>
      <button class="close-sidebar" onclick="toggleSidebar()">×</button>
    </div>
    <ul class="sidebar-menu">
      <li><a href="admin-dashboard.py">📊 Control Center</a></li>
      <li><a href="doctors.py" class="active">👨‍⚕️ Doctor Directory</a></li>
      <li><a href="patients.py">🧑‍🤝‍🧑 Patient Hub</a></li>
      <li><a href="appointments-history.py">📅 Appointment History</a></li>
      <li><a href="upcoming-appointments.py">⏳ Upcoming Appointments</a></li>
      <li><a href="cancelled-appointments.py">❌ Cancelled Appointments</a></li>
      <li><a href="add-doctor.py">➕ Add a Healer</a></li>
      <li><a href="add-patient.py">➕ Register Patient</a></li>
      <li><a href="index.py">🚪 Sign Out</a></li>
    </ul>
  </aside>
  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <span class="mobile-heading">Doctor List</span>
      <h1 class="desktop-heading">Doctor List</h1>
    </header>
    <section class="content">
      <h2>All Registered Doctors</h2>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Profile</th>
              <th>Name</th><th>DOB</th><th>Gender</th><th>Specialization</th><th>Experience</th>
              <th>Address Line 1</th><th>Address Line 2</th><th>Email</th><th>Phone Number</th>
              <th>Hospital Name</th><th>Hospital Address</th>
              <th>Appointments</th><th>Action</th>
            </tr>
          </thead>
          <tbody>
""")

# --- Generate table rows dynamically ---
for doctor in doctors:
    did = doctor[0]
    profile_pic = doctor[15] if len(doctor) > 15 else ""

    # appointment counts
    cur.execute("SELECT COUNT(*) FROM appointments WHERE doctor_id=%s", (did,))
    approved = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM cancelled_appointments WHERE doctor_id=%s", (did,))
    cancelled = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM appointment_history WHERE doctor_id=%s", (did,))
    completed = cur.fetchone()[0]

    img_tag = f"<img src='Doctor-register-images/{safe(profile_pic)}' class='profile-pic' alt='Profile'>" if profile_pic else "No Image"

    print(f"""
    <tr>
        <td>{img_tag}</td>
        <td>{safe(doctor[1])}</td>
        <td>{safe(doctor[7])}</td>
        <td>{safe(doctor[8])}</td>
        <td>{safe(doctor[5])}</td>
        <td>{safe(doctor[6])}</td>
        <td>{safe(doctor[9])}</td>
        <td>{safe(doctor[10])}</td>
        <td>{safe(doctor[2])}</td>
        <td>{safe(doctor[11])}</td>
        <td>{safe(doctor[12])}</td>
        <td>{safe(doctor[13])}</td>
        <td>Approved: {approved}, Cancelled: {cancelled}, Completed: {completed}</td>
        <td><button class="delete-btn" onclick="openDeleteModal('{did}','{safe(doctor[1])}')">Delete</button></td>
    </tr>
    """)

print("""
          </tbody>
        </table>
      </div>
    </section>
  </main>
</div>

<!-- Modal -->
<div id="deleteModal" class="modal">
  <div class="modal-content">
    <span class="close-modal" onclick="closeModal()">&times;</span>
    <h3>Delete Doctor Account</h3>
    <p id="delete-doctor-name"></p>
    <form method="get" id="deleteForm">
      <input type="hidden" name="delete_id" id="delete_id" />
      <label for="reason">Reason for deletion:</label><br />
      <textarea id="reason" name="reason" rows="4" placeholder="Enter reason..." required></textarea><br />
      <button class="confirm-delete" type="submit">Confirm Delete</button>
    </form>
  </div>
</div>

<script>
function toggleSidebar() { document.getElementById("sidebar").classList.toggle("open"); }
function openDeleteModal(id, name) {
    document.getElementById("delete-doctor-name").textContent = 'Doctor: ' + name;
    document.getElementById("delete_id").value = id;
    document.getElementById("deleteModal").style.display = 'block';
}
function closeModal() {
    document.getElementById("deleteModal").style.display = 'none';
    document.getElementById("reason").value = '';
}
</script>
</body>
</html>
""")
