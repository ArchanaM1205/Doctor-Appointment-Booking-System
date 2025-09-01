#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys, os
cgitb.enable()

# DB connection
con = pymysql.connect(host="localhost", user="root", password="", database="appointment_booking_system")
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')
UPLOAD_DIR = "Patient-register-images"

form = cgi.FieldStorage()
patient_id = form.getvalue("id")

# If multiple values are passed, pick the first one
if isinstance(patient_id, list):
    patient_id = patient_id[0]

# Convert to int safely
try:
    patient_id = int(patient_id)
except (TypeError, ValueError):
    print("<h3 style='color:red;'>Error: Invalid patient ID.</h3>")
    sys.exit()


# Handle form submission
if form.getvalue("sub"):
    name = form.getvalue("patientname")
    gender = form.getvalue("gender")
    dob = form.getvalue("dob")
    marital = form.getvalue("maritalstatus")
    addr1 = form.getvalue("address1")
    addr2 = form.getvalue("address2")

    # File upload handling
    fileitem = form["profile_pic"] if "profile_pic" in form else None
    filename_db = None

    if fileitem is not None and fileitem.filename:
        filename = os.path.basename(fileitem.filename)
        filepath = os.path.join(UPLOAD_DIR, filename)

        # Save file to Patient-register-images folder
        with open(filepath, "wb") as f:
            f.write(fileitem.file.read())
        filename_db = filename

        # Update all fields including image
        q = """UPDATE patient_register 
               SET Patient_name=%s, Gender=%s, Dob=%s, Marital_Status=%s,
                   Address_line1=%s, Address_line2=%s, Profile_image=%s
               WHERE id=%s"""
        cur.execute(q, (name, gender, dob, marital, addr1, addr2, filename_db, patient_id))
    else:
        # Update all fields except image
        q = """UPDATE patient_register 
               SET Patient_name=%s, Gender=%s, Dob=%s, Marital_Status=%s,
                   Address_line1=%s, Address_line2=%s
               WHERE id=%s"""
        cur.execute(q, (name, gender, dob, marital, addr1, addr2, patient_id))

    con.commit()

    # Redirect back to profile page
    print(f"""
        <script>
            alert("Profile updated successfully!");
            window.location.href = "patient-profile.py?id={patient_id}";
        </script>
    """)
    con.close()
    sys.exit()

# Fetch patient details
q = """SELECT id, Patient_name, Gender, Dob, Email, Phone, 
              Address_line1, Address_line2, Profile_image, Marital_Status 
       FROM patient_register WHERE id=%s"""
cur.execute(q, (patient_id,))
data = cur.fetchone()

if data:
    pid, name, gender, dob, email_db, phone, addr1, addr2, profile_image_db, marital = data
    profile_image = f"{UPLOAD_DIR}/{profile_image_db}" if profile_image_db else f"{UPLOAD_DIR}/default.png"
else:
    pid = 0
    name = gender = dob = email_db = phone = addr1 = addr2 = marital = "N/A"
    profile_image = f"{UPLOAD_DIR}/default.png"


# Output HTML
print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Edit Patient Profile</title>
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
      padding: 30px 20px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
      max-width: 900px;
      margin-left: auto;
      margin-right: auto;
    }}

    .content h2 {{
      text-align: center;
      margin-bottom: 30px;
      color: #333;
    }}

    form {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 20px;
    }}

    .form-group {{
      display: flex;
      flex-direction: column;
    }}

    label {{
      font-weight: bold;
      font-size: 14px;
      margin-bottom: 5px;
    }}

    input, select {{
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 6px;
      font-size: 15px;
    }}

    .form-group.col-span-6 {{
      grid-column: span 1;
    }}

    .form-group.col-span-12 {{
      grid-column: span 1;
    }}

    .upload-area {{
      grid-column: span 1;
      text-align: center;
      padding: 20px;
      border-radius: 8px;
      background: #f8f9ff;
      border: 2px dashed #ccc;
      cursor: pointer;
      transition: background 0.3s ease;
    }}

    .upload-area:hover {{
      background: #eef0ff;
    }}

    .upload-area img {{
      width: 50px;
      margin-bottom: 10px;
      opacity: 0.7;
    }}

    .form-buttons {{
      grid-column: span 1;
      display: flex;
      justify-content: space-between;
      gap: 10px;
    }}

    .save-btn {{
      background: #5f6FFF;
      color: white;
      padding: 12px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 16px;
      width: 48%;
    }}

    .save-btn:hover {{
      background: #3d47d6;
    }}

    .cancel-btn {{
      background: #f50606;
      color: white;
      padding: 12px;
      border: none;
      border-radius: 6px;
      cursor: pointer;
      font-size: 16px;
      width: 48%;
    }}

    .cancel-btn:hover {{
      background: #b00000;
    }}

    /* Responsive Layout for Form */
    @media (min-width: 900px) {{
      form {{
        grid-template-columns: repeat(2, 1fr);
      }}

      .form-group.col-span-6 {{
        grid-column: span 1;
      }}

      .form-group.col-span-12,
      .upload-area,
      .form-buttons {{
        grid-column: span 2;
      }}

      .form-buttons {{
        flex-direction: row;
        justify-content: space-between;
      }}

      .form-buttons button {{
        width: 48%;
      }}
    }}

    @media (max-width: 899px) {{
      .form-group.col-span-6,
      .form-group.col-span-12,
      .upload-area,
      .form-buttons {{
        grid-column: span 1;
      }}

      .form-buttons {{
        flex-direction: column;
        align-items: center;
      }}

      .form-buttons button {{
        width: 100%;
      }}
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
    }}

    @media (max-width: 480px) {{
      input, select {{
        font-size: 14px;
      }}

      .save-btn, .cancel-btn {{
        font-size: 14px;
        padding: 10px;
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
      <li><a href="patient-dashboard.py?id={patient_id}">🏠 Dashboard</a></li>
      <li><a href="patient-upcoming-appointments.py?id={patient_id}">⏳ Upcoming Appointments</a></li>
      <li><a href="patient-book-appointments.py?id={patient_id}">📅 Book Appointments</a></li>
      <li><a href="patient-past-appointments.py?id={patient_id}">🗓 Past Appointments</a></li>
      <li><a href="patient-profile.py?id={patient_id}" class="active">👤 Profile</a></li>
      <li><a href="patient-medical-records.py?id={patient_id}">📄 Medical Records</a></li>
      <li><a href="index.py">🚪 Logout</a></li>
    </ul>
  </aside>

  <!-- Main Content -->
  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <h1>Edit Profile</h1>
    </header>

    <section class="content">
      <h2>Edit Patient Profile</h2>
      <form id="editForm" method="post" enctype="multipart/form-data">
      <input type="hidden" name="id" value="{pid}">
        <div class="form-group col-span-6">
          <label>Full Name</label>
          <input type="text" value="{name}" name="patientname"required>
        </div>
        <div class="form-group col-span-6">
          <label>Gender</label>
          <select name="gender" required>
            <option selected>Female</option>
            <option>Male</option>
            <option>Other</option>
          </select>
        </div>
        <div class="form-group col-span-6">
          <label>Date of Birth</label>
          <input type="date" value="{dob}" name="dob" required>
        </div>
        <div class="form-group col-span-6">
          <label>Marital Status</label>
          <select name="maritalstatus" required>
            <option selected>Single</option>
            <option>Married</option>
            <option>Other</option>
          </select>
        </div>
        <div class="form-group col-span-12">
          <label>Address Line 1</label>
          <input type="text" value="{addr1}" name="address1"required>
        </div>
        <div class="form-group col-span-12">
          <label>Address Line 2</label>
          <input type="text" value="{addr2}" name="address2">
        </div>

        <div class="upload-area" onclick="document.getElementById('uploadImage').click()">
          <img src="upload_area.png" alt="Upload Icon">
          <p>Upload Profile Picture</p>
          <input type="file" id="uploadImage"name="profile_pic" value="{profile_image}" hidden>
        </div>

        <div class="form-buttons">
          <input type="submit" class="save-btn" value="Save Changes" name="sub">
          <button type="button" class="cancel-btn" onclick="cancelEdit()">Cancel</button>
        </div>
      </form>
    </section>
  </main>
</div>

<script>
  function toggleSidebar() {{
    document.getElementById("sidebar").classList.toggle("open");
  }}

  function cancelEdit() {{
    window.location.href = "patient-profile.py?id={patient_id}";
  }}

  document.getElementById("editForm").addEventListener("submit", function(e) {{
    alert("Profile updated successfully!");
    window.location.href = "patient-profile.py?id={patient_id}";
  }});
</script>

</body>
</html>
""")