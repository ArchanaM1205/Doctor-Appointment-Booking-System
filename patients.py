#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys, datetime
cgitb.enable()

form = cgi.FieldStorage()
con = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="appointment_booking_system"
)
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

# -------- Handle Deletion if form submitted --------
if form.getvalue("delete_id") and form.getvalue("delete_reason"):
    pid = int(form.getvalue("delete_id"))
    reason = form.getvalue("delete_reason")

    # Fetch patient details
    cur.execute("SELECT * FROM patient_register WHERE id=%s", (pid,))
    patient = cur.fetchone()

    if patient:
        # patient_register column order assumption:
        # (id, Patient_name, Dob, Gender, Marital_Status, Email, Phone, Address_line1, Address_line2, Profile_image, Password,...)
        patient_id = patient[0]
        patient_name = patient[1]
        dob = patient[2]
        gender = patient[3]
        marital_status = patient[4]
        email = patient[5]
        phone = patient[6]
        addr1 = patient[7]
        addr2 = patient[8]
        # profile_img = patient[9]  # Removed as requested

        # ✅ Insert into deleted_patients WITHOUT profile image
        cur.execute("""
            INSERT INTO deleted_patients
            (Id, Patient_name, Dob, Gender, Marital_Status, Email, Phone, Address_line1, Address_line2, Deletion_reason, Deleted_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            patient_id,
            patient_name,
            dob,
            gender,
            marital_status,
            email,
            phone,
            addr1,
            addr2,
            reason,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        # Delete from patient_register
        cur.execute("DELETE FROM patient_register WHERE id=%s", (pid,))
        con.commit()

        print(f"<script>alert('Patient deleted successfully'); window.location.href='patients.py';</script>")

# -------- HTML Page Starts --------
print("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Patient List</title>
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
    img.profile-pic { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; }
    .delete-btn { background: #ff4d4d; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; }
    .modal { display: none; position: fixed; z-index: 2000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.4); }
    .modal-content { background-color: #fff; margin: 10% auto; padding: 20px; border-radius: 8px; width: 90%; max-width: 400px; box-shadow: 0 2px 10px rgba(0,0,0,0.2); }
    .modal-content h3 { margin-top: 0; }
    .modal-content textarea { width: 100%; height: 80px; margin: 10px 0; padding: 8px; font-size: 14px; border-radius: 4px; border: 1px solid #ccc; resize: vertical; }
    .modal-actions { display: flex; justify-content: flex-end; gap: 10px; }
    .modal-actions button { padding: 8px 14px; border: none; border-radius: 4px; cursor: pointer; }
    .cancel-btn { background-color: #ccc; }
    .confirm-btn { background-color: #ff4d4d; color: white; }
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
      <li><a href="patients.py" class="active">🧑‍🤝‍🧑 Patient Hub</a></li>
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
      <span class="mobile-heading">Patient List</span>
      <h1 class="desktop-heading">Patient List</h1>
    </header>

    <section class="content">
      <h2>All Registered Patients</h2>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Profile Pic</th>
              <th>Name</th>
              <th>DOB</th>
              <th>Gender</th>
              <th>Marital Status</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Address Line 1</th>
              <th>Address Line 2</th>
              <th>Appointments</th>
              <th>Delete Account</th>
            </tr>
          </thead>
          <tbody>
""")

# --- Fetch patients dynamically ---
cur.execute("SELECT id, Patient_name, Dob, Gender, Marital_Status, Email, Phone, Address_line1, Address_line2, Profile_image FROM patient_register")
patients = cur.fetchall()

for patient in patients:
    pid, name, dob, gender, marital_status, email, phone, addr1, addr2, pic = patient

    # Appointment counts (use `id` instead of patient_id)
    cur.execute("SELECT COUNT(*) FROM appointments WHERE id=%s", (pid,))
    approved = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM cancelled_appointments WHERE id=%s", (pid,))
    cancelled = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM appointment_history WHERE id=%s", (pid,))
    completed = cur.fetchone()[0]

    profile_pic = f"Patient-register-images/{pic}" if pic else "default-patient.png"

    print(f"""
            <tr>
              <td><img src="{profile_pic}" alt="Patient Pic" class="profile-pic"></td>
              <td>{name}</td>
              <td>{dob}</td>
              <td>{gender}</td>
              <td>{marital_status}</td>
              <td>{email}</td>
              <td>{phone}</td>
              <td>{addr1}</td>
              <td>{addr2}</td>
              <td>Approved: {approved}, Cancelled: {cancelled}, Completed: {completed}</td>
              <td>
                <button class="delete-btn" onclick="openModal({pid}, '{name}')">Delete</button>
              </td>
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
<div class="modal" id="deleteModal">
  <div class="modal-content">
    <h3>Reason for deleting <span id="deleteTargetName"></span>'s account</h3>
    <form method="post" id="deleteForm">
      <input type="hidden" name="delete_id" id="deleteTargetId">
      <textarea name="delete_reason" placeholder="Enter reason..."></textarea>
      <div class="modal-actions">
        <button type="button" class="cancel-btn" onclick="closeModal()">Cancel</button>
        <button type="submit" class="confirm-btn">Confirm</button>
      </div>
    </form>
  </div>
</div>

<script>
  function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("open");
  }

  function openModal(id, name) {
    document.getElementById("deleteTargetId").value = id;
    document.getElementById("deleteTargetName").textContent = name;
    document.getElementById("deleteModal").style.display = "block";
  }

  function closeModal() {
    document.getElementById("deleteModal").style.display = "none";
  }
</script>

</body>
</html>
""")
