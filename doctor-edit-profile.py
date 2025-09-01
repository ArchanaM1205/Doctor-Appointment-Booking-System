#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql, cgi, cgitb, sys, os
from datetime import datetime
cgitb.enable()

UPLOAD_DIR = "Doctor-register-images"

form = cgi.FieldStorage()
con = pymysql.connect(host="localhost", user="root", password="", database="appointment_booking_system")
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

doctor_id = form.getvalue("id")

# ---------- UPDATE DOCTOR PROFILE ----------
if form.getvalue("sub"):
    name = form.getvalue("name")
    dob = form.getvalue("dob")
    gender = form.getvalue("gender")
    specialization = form.getvalue("specialization")
    experience = form.getvalue("experience")
    address1 = form.getvalue("address1")
    address2 = form.getvalue("address2")
    hospitalName = form.getvalue("hospitalName")
    hospitalAddress = form.getvalue("hospitalAddress")

    # Handle image upload
    fileitem = form['profilePic'] if "profilePic" in form else None
    filename_db = None
    if fileitem is not None and fileitem.filename:
        filename = os.path.basename(fileitem.filename)
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(fileitem.file.read())
        filename_db = filename

    # Update query
    if filename_db:
        update_q = """UPDATE doctor_register 
                      SET Doctor_name=%s, Dob=%s, Gender=%s, Specialization=%s, Experience=%s, 
                          Address_line1=%s, Address_line2=%s, Hospital_name=%s, Hospital_address=%s, Profile_picture=%s 
                      WHERE id=%s"""
        cur.execute(update_q, (name, dob, gender, specialization, experience,
                               address1, address2, hospitalName, hospitalAddress, filename_db, doctor_id))
    else:
        update_q = """UPDATE doctor_register 
                      SET Doctor_name=%s, Dob=%s, Gender=%s, Specialization=%s, Experience=%s, 
                          Address_line1=%s, Address_line2=%s, Hospital_name=%s, Hospital_address=%s
                      WHERE id=%s"""
        cur.execute(update_q, (name, dob, gender, specialization, experience,
                               address1, address2, hospitalName, hospitalAddress, doctor_id))

    con.commit()
    print(f"<script>alert('Profile Updated Successfully!');window.location.href='doctor-profile.py?id={doctor_id}';</script>")
    sys.exit()

# ---------- FETCH EXISTING DATA ----------
query = """
    SELECT id, Doctor_name, Dob, Gender, Specialization, Experience, 
           Address_line1, Address_line2, Hospital_name, Hospital_address, Profile_picture
    FROM doctor_register
    WHERE id = %s
"""
cur.execute(query, (doctor_id,))
data = cur.fetchone()

if data:
    (did, name, dob, gender, specialization, experience,
     addr1, addr2, hospitalName, hospitalAddr, image) = data

    # Fix date format for input type="date" (yyyy-MM-dd)
    if dob and isinstance(dob, (str, bytes)):
        try:
            dob = datetime.strptime(str(dob), "%Y-%m-%d").strftime("%Y-%m-%d")
        except:
            dob = ""
    else:
        dob = ""

    profile_image = f"{UPLOAD_DIR}/{image}" if image else f"{UPLOAD_DIR}/profile_pic.png"
else:
    did = 0
    name = dob = gender = specialization = experience = addr1 = addr2 = hospitalName = hospitalAddr = ""
    profile_image = f"{UPLOAD_DIR}/profile_pic.png"

# ---------- PRINT HTML ----------
print(f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Edit Doctor Profile</title>
  <style>
    /* Your original CSS — unchanged */
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
      max-width: 800px;
      margin-left: auto;
      margin-right: auto;
    }}

    .content h2 {{
      text-align: center;
      margin-bottom: 20px;
      font-size: 24px;
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

    .form-group label {{
      font-size: 14px;
      margin-bottom: 6px;
      color: #555;
    }}

    .form-group input,
    .form-group select {{
      padding: 10px;
      font-size: 14px;
      border: 1px solid #ccc;
      border-radius: 6px;
      outline: none;
      width: 100%;
      box-sizing: border-box;
    }}

    .upload-area {{
      grid-column: span 1;
      border: 2px dashed #ccc;
      padding: 20px;
      text-align: center;
      border-radius: 8px;
      cursor: pointer;
      background: #fafafa;
    }}

    .upload-area img {{
      width: 120px;
      height: 120px;
      border-radius: 50%;
      object-fit: cover;
      margin-bottom: 10px;
    }}

    .upload-area span {{
      display: block;
      font-size: 14px;
      color: #666;
    }}

    .upload-area input {{
      display: none;
    }}

    .form-actions {{
      grid-column: span 1;
      display: flex;
      justify-content: center;
      gap: 20px;
      margin-top: 20px;
      flex-wrap: wrap;
    }}

    .save-btn {{
      background: #5f6FFF;
      color: white;
      padding: 12px 20px;
      border: none;
      border-radius: 6px;
      font-size: 16px;
      cursor: pointer;
      width: 160px;
    }}

    .save-btn:hover {{
      background: #3d47d6;
    }}

    .cancel-btn {{
      background: #ff4d4d;
      color: white;
      padding: 12px 20px;
      border: none;
      border-radius: 6px;
      font-size: 16px;
      cursor: pointer;
      width: 160px;
    }}

    .cancel-btn:hover {{
      background: #d93636;
    }}

    /* Responsive: One column on small screens */
    @media (max-width: 899px) {{
      form {{
        grid-template-columns: 1fr;
      }}

      .upload-area,
      .form-actions {{
        grid-column: span 1;
      }}

      .form-actions {{
        flex-direction: column;
        align-items: center;
      }}

      .save-btn,
      .cancel-btn {{
        width: 100%;
        max-width: 300px;
      }}
    }}

    /* Two columns on medium and larger screens */
    @media (min-width: 900px) {{
      form {{
        grid-template-columns: repeat(2, 1fr);
      }}

      .upload-area,
      .form-actions {{
        grid-column: span 2;
      }}
    }}

    /* Sidebar toggle for small screens */
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
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <h2>Prescripto</h2>
      <button class="close-sidebar" onclick="toggleSidebar()">×</button>
    </div>
    <ul class="sidebar-menu">
      <li><a href="doctor-dashboard.py?id={doctor_id}">📊 Dashboard</a></li>
      <li><a href="doctor-appointment-history.py?id={doctor_id}">📅 Appointment History</a></li>
      <li><a href="doctor-upcoming-appointments.py?id={doctor_id}">⏳ Upcoming Appointments</a></li>
      <li><a href="doctor-cancelled-appointments.py?id={doctor_id}">❌ Cancelled Appointments</a></li>
      <li><a href="doctor-profile.py?id={doctor_id}" class="active">👤 Profile</a></li>
      <li><a href="index.py">🚪 Logout</a></li>
    </ul>
  </aside>

  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <h1>Edit Doctor Profile</h1>
    </header>

    <section class="content">
      <h2>Edit Profile</h2>
      <form id="doctorEditForm" method="post" enctype="multipart/form-data">
        <div class="form-group">
          <label for="name">Doctor Name</label>
          <input type="text" id="name" name="name" value="{name}">
        </div>
        <div class="form-group">
          <label for="dob">Date of Birth</label>
          <input type="date" id="dob" name="dob" value="{dob}">
        </div>
        <div class="form-group">
          <label for="gender">Gender</label>
          <select id="gender" name="gender">
            <option {"selected" if gender=="Male" else ""}>Male</option>
            <option {"selected" if gender=="Female" else ""}>Female</option>
            <option {"selected" if gender=="Other" else ""}>Other</option>
          </select>
        </div>
        <div class="form-group">
          <label for="specialization">Specialization</label>
          <input type="text" id="specialization" name="specialization" value="{specialization}">
        </div>
        <div class="form-group">
          <label for="experience">Experience (years)</label>
          <input type="number" id="experience" name="experience" value="{experience}">
        </div>
        <div class="form-group">
          <label for="address1">Address Line 1</label>
          <input type="text" id="address1" name="address1" value="{addr1}">
        </div>
        <div class="form-group">
          <label for="address2">Address Line 2</label>
          <input type="text" id="address2" name="address2" value="{addr2}">
        </div>
        <div class="form-group">
          <label for="hospitalName">Hospital Name</label>
          <input type="text" id="hospitalName" name="hospitalName" value="{hospitalName}">
        </div>
        <div class="form-group">
          <label for="hospitalAddress">Hospital Address</label>
          <input type="text" id="hospitalAddress" name="hospitalAddress" value="{hospitalAddr}">
        </div>

        <div class="upload-area" onclick="document.getElementById('profilePic').click()">
          <img id="previewImg" src="{profile_image}" alt="Profile Preview">
          <span>Click to upload profile picture</span>
          <input type="file" id="profilePic" name="profilePic" accept="image/*" onchange="previewImage(event)">
        </div>

        <div class="form-actions">
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

  function previewImage(event) {{
    const reader = new FileReader();
    reader.onload = function () {{
      document.getElementById("previewImg").src = reader.result;
    }};
    reader.readAsDataURL(event.target.files[0]);
  }}

  function cancelEdit() {{
    window.location.href = "doctor-profile.py?id={doctor_id}";
  }}
</script>

</body>
</html>
""")
