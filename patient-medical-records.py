#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys, os, datetime
cgitb.enable()

form = cgi.FieldStorage()
patient_id = form.getvalue("id")  # Get patient ID from URL

con = pymysql.connect(host="localhost", user="root", password="", database="appointment_booking_system")
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

UPLOAD_DIR = "uploads/patient_records/"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# ✅ Handle file upload
if "fileUpload" in form:
    file_item = form["fileUpload"]
    if file_item.filename:
        filename = os.path.basename(file_item.filename)
        filepath = os.path.join(UPLOAD_DIR, filename)

        # Save file
        with open(filepath, "wb") as f:
            f.write(file_item.file.read())

        # Insert into new table patient_medical_records
        cur.execute("""
            INSERT INTO patient_medical_records(patient_id, record_name, record_path, uploaded_date)
            VALUES (%s, %s, %s, %s)
        """, (patient_id, filename, filepath.replace("\\", "/"), datetime.date.today()))
        con.commit()

# ✅ Fetch old records from appointment_history
cur.execute("""
    SELECT id, doctor_name, appointment_date, prescription, medical_record
    FROM appointment_history
    WHERE patient_name = (SELECT patient_name FROM patient_register WHERE id=%s)
    ORDER BY appointment_date DESC
""", (patient_id,))
records = cur.fetchall()

# ✅ Fetch uploaded records from patient_medical_records
cur.execute("""
    SELECT id, record_name, record_path, uploaded_date
    FROM patient_medical_records
    WHERE patient_id=%s
    ORDER BY uploaded_date DESC
""", (patient_id,))
uploaded_records = cur.fetchall()

print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Patient Medical Records</title>
  <style>
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      background: #f8f9ff;
    }}
    .dashboard-container {{ display: flex; min-height: 100vh; }}
    .sidebar {{ background: #5f6FFF; color: white; width: 250px; padding: 20px; display: flex; flex-direction: column; transition: transform 0.3s ease; }}
    .sidebar-header {{ display: flex; justify-content: space-between; align-items: center; }}
    .sidebar-header h2 {{ margin: 0; font-size: 20px; }}
    .close-sidebar {{ background: none; border: none; font-size: 20px; color: white; cursor: pointer; display: none; }}
    .sidebar-menu {{ list-style: none; padding: 0; margin-top: 20px; }}
    .sidebar-menu li {{ margin-bottom: 15px; }}
    .sidebar-menu a {{ text-decoration: none; color: white; font-size: 16px; padding: 10px; display: block; border-radius: 6px; transition: background 0.3s ease; }}
    .sidebar-menu a:hover, .sidebar-menu a.active {{ background: #3d47d6; }}
    .main-content {{ flex: 1; padding: 20px; overflow-y: auto; }}
    .topbar {{ display: flex; align-items: center; justify-content: center; position: relative; }}
    .topbar h1 {{ margin: 0; font-size: 24px; font-weight: bold; text-align: center; flex: 1; }}
    .menu-btn {{ position: absolute; left: 0; background: #5f6FFF; color: white; padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer; display: none; }}
    .content {{ margin-top: 20px; background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
    .content h2 {{ margin-bottom: 20px; color: #333; text-align: center; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
    table thead {{ background: #5f6FFF; color: white; }}
    table th, table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; font-size: 15px; }}
    table tr:hover {{ background: #f1f1f1; }}
    .action-btn {{ padding: 6px 12px; border: none; border-radius: 4px; font-size: 14px; cursor: pointer; margin: 3px 5px 3px 0; }}
    .view-btn {{ background: #5f6FFF; color: white; }}
    .download-btn {{ background: #28a745; color: white; }}
    .upload-section {{ border: 2px dashed #ccc; padding: 20px; text-align: center; border-radius: 8px; background: #f8f9ff; cursor: pointer; transition: background 0.3s ease; }}
    .upload-section:hover {{ background: #eef0ff; }}
    .upload-section input {{ display: none; }}
    @media (max-width: 768px) {{
      table, thead, tbody, th, td, tr {{ display: block; }}
      thead {{ display: none; }}
      tr {{ background: white; margin-bottom: 12px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); padding: 10px; }}
      td {{ border: none; padding: 8px 10px; display: flex; justify-content: space-between; align-items: center; }}
      td::before {{ content: attr(data-label); font-weight: bold; color: #333; }}
      .action-btn {{ width: 100%; margin: 5px 0; display: block; }}
      .sidebar {{ position: fixed; left: 0; top: 0; height: 100%; transform: translateX(-100%); z-index: 1000; }}
      .sidebar.open {{ transform: translateX(0); }}
      .close-sidebar {{ display: block; }}
      .menu-btn {{ display: block; }}
    }}
    @media (max-width: 480px) {{
      .topbar h1 {{ font-size: 20px; }}
      .action-btn {{ font-size: 12px; padding: 6px; }}
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
      <li><a href="patient-dashboard.py?id={patient_id}">🏠 Dashboard</a></li>
      <li><a href="patient-upcoming-appointments.py?id={patient_id}">⏳ Upcoming Appointments</a></li>
      <li><a href="patient-book-appointments.py?id={patient_id}">📅 Book Appointments</a></li>
      <li><a href="patient-past-appointments.py?id={patient_id}">🗓 Past Appointments</a></li>
      <li><a href="patient-profile.py?id={patient_id}">👤 Profile</a></li>
      <li><a href="patient-medical-records.py?id={patient_id}" class="active">📄 Medical Records</a></li>
      <li><a href="index.py">🚪 Logout</a></li>
    </ul>
  </aside>

  <!-- Main Content -->
  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <h1>Medical Records</h1>
    </header>

    <section class="content">
      <h2>Your Medical Records</h2>

      <!-- Records Table -->
      <table>
        <thead>
          <tr>
            <th>Record Name</th>
            <th>Date</th>
            <th>Doctor</th>
            <th>Type</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
""")

# ✅ Old records
for rid, doctor_name, date_val, prescription, medical_record in records:
    if prescription:
        pres_name = os.path.basename(prescription)
        print(f"""
          <tr>
            <td data-label="Record Name">{pres_name}</td>
            <td data-label="Date">{date_val}</td>
            <td data-label="Doctor">{doctor_name}</td>
            <td data-label="Type">Prescription</td>
            <td data-label="Actions">
              <a href="{prescription}" target="_blank"><button class="action-btn view-btn">View</button></a>
              <a href="{prescription}" download><button class="action-btn download-btn">Download</button></a>
            </td>
          </tr>
        """)
    if medical_record:
        med_name = os.path.basename(medical_record)
        print(f"""
          <tr>
            <td data-label="Record Name">{med_name}</td>
            <td data-label="Date">{date_val}</td>
            <td data-label="Doctor">{doctor_name}</td>
            <td data-label="Type">Medical Record</td>
            <td data-label="Actions">
              <a href="{medical_record}" target="_blank"><button class="action-btn view-btn">View</button></a>
              <a href="{medical_record}" download><button class="action-btn download-btn">Download</button></a>
            </td>
          </tr>
        """)

print("""
        </tbody>
      </table>

      <!-- Upload New Record -->
      <form method="post" enctype="multipart/form-data">
        <div class="upload-section" onclick="document.getElementById('fileUpload').click()">
          <p>📤 Click here to upload a new medical record</p>
          <input type="file" name="fileUpload" id="fileUpload" onchange="this.form.submit()" />
        </div>
      </form>
    </section>

    <section class="content">
      <h2>Uploaded Records</h2>
      <table>
        <thead>
          <tr>
            <th>Record Name</th>
            <th>Uploaded Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
""")

# ✅ Uploaded patient records
for rid, record_name, record_path, uploaded_date in uploaded_records:
    print(f"""
      <tr>
        <td data-label="Record Name">{record_name}</td>
        <td data-label="Uploaded Date">{uploaded_date}</td>
        <td data-label="Actions">
          <a href="{record_path}" target="_blank"><button class="action-btn view-btn">View</button></a>
          <a href="{record_path}" download><button class="action-btn download-btn">Download</button></a>
        </td>
      </tr>
    """)

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
