#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
import pymysql, cgi, cgitb, sys, os, json, datetime
cgitb.enable()

form = cgi.FieldStorage()
con = pymysql.connect(host="localhost", user="root", password="", database="appointment_booking_system")
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

# Handle AJAX doctor fetch
if form.getvalue("ajax") == "1":
    specialization = form.getvalue("specialization")
    cur.execute("SELECT id, Doctor_name FROM doctor_register WHERE specialization=%s", (specialization,))
    rows = cur.fetchall()
    doctors = [{"id": row[0], "name": row[1]} for row in rows]
    print("content-type: application/json\n")
    print(json.dumps(doctors))
    sys.exit()

# Normal page render
print("content-type: text/html\n\n")

patient_id = form.getvalue("id")
if isinstance(patient_id, list): patient_id = patient_id[0]
if not patient_id:
    print("""<!DOCTYPE html>
<html><body>
<p>Please login first!</p>
<a href="index.py">Go to Login</a>
</body></html>""")
    sys.exit()

# Fetch specializations & doctors
cur.execute("SELECT DISTINCT specialization FROM doctor_register")
specializations = [row[0] for row in cur.fetchall()]
cur.execute("SELECT id, Doctor_name FROM doctor_register")
all_doctors = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]

today = datetime.date.today().strftime("%Y-%m-%d")

# HTML Content (unchanged)
print(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Book Appointment</title>
<style>
/* ... original CSS ... */
body {{ margin:0; font-family: Arial, sans-serif; background:#f8f9ff; }}
.dashboard-container {{ display:flex; min-height:100vh; }}
.sidebar {{ background:#5f6FFF; color:white; width:250px; padding:20px; display:flex; flex-direction:column; transition: transform 0.3s ease; }}
.sidebar-header {{ display:flex; justify-content:space-between; align-items:center; }}
.sidebar-header h2 {{ margin:0; font-size:20px; }}
.close-sidebar {{ background:none; border:none; font-size:20px; color:white; cursor:pointer; display:none; }}
.sidebar-menu {{ list-style:none; padding:0; margin-top:20px; }}
.sidebar-menu li {{ margin-bottom:15px; }}
.sidebar-menu a {{ text-decoration:none; color:white; font-size:16px; padding:10px; display:block; border-radius:6px; transition: background 0.3s ease; }}
.sidebar-menu a:hover, .sidebar-menu a.active {{ background:#3d47d6; }}
.main-content {{ flex:1; padding:20px; }}
.topbar {{ display:flex; align-items:center; justify-content:space-between; margin-bottom:20px; }}
.menu-btn {{ display:none; background:#5f6FFF; color:white; padding:10px; border:none; border-radius:5px; cursor:pointer; }}
.content {{ background:white; padding:20px; border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,0.1); max-width:900px; margin:auto; }}
h1.page-title {{ font-size:28px; text-align:center; color:#333; }}
form {{ display:grid; grid-template-columns:1fr; gap:20px; margin-top:20px; }}
.form-group {{ display:flex; flex-direction:column; }}
label {{ font-weight:bold; margin-bottom:5px; }}
input, select, textarea {{ padding:12px; border:1px solid #ccc; border-radius:6px; font-size:15px; width:100%; box-sizing:border-box; }}
textarea {{ resize:vertical; min-height:100px; }}
.full-width {{ grid-column: span 2; }}
.half-width {{ width:100%; }}
.upload-area {{ text-align:center; padding:20px; border-radius:8px; background:#f8f9ff; border:2px dashed #ccc; cursor:pointer; }}
.upload-area img {{ width:70px; margin-bottom:10px; opacity:0.7; }}
.upload-area p {{ font-size:14px; color:#555; }}
.form-buttons {{ display:flex; flex-direction:column; gap:12px; }}
.form-buttons button, .form-buttons input {{ padding:14px; font-size:16px; font-weight:bold; border:none; border-radius:6px; cursor:pointer; }}
.submit-btn {{ background:#5f6FFF; color:white; }}
.submit-btn:hover {{ background:#3d47d6; }}
.cancel-btn {{ background:#f50606; color:white; }}
.cancel-btn:hover {{ background:#999; }}
@media(max-width:768px){{
  form {{ grid-template-columns:1fr; }}
  .full-width, .half-width {{ grid-column: span 1; }}
  .form-buttons {{ flex-direction:column; gap:12px; }}
  .form-buttons button,.form-buttons input {{ width:100%; }}
  .sidebar {{ position:fixed; left:0; top:0; height:100%; transform:translateX(-100%); z-index:1000; }}
  .sidebar.open {{ transform:translateX(0); }}
  .close-sidebar {{ display:block; }}
  .menu-btn {{ display:block; }}
}}
@media(min-width:769px){{
  form {{ grid-template-columns:repeat(2,1fr); }}
  .full-width {{ grid-column: span 2; }}
  .half-width {{ grid-column: span 1; }}
  .form-buttons {{ flex-direction:row; justify-content:space-between; }}
  .form-buttons button,.form-buttons input {{ width:48%; }}
}}
</style>
</head>
<body>
<div class="dashboard-container">
<aside class="sidebar" id="sidebar">
<div class="sidebar-header">
<h2>Prescripto</h2>
<button class="close-sidebar">×</button>
</div>
<ul class="sidebar-menu">
<li><a href="patient-dashboard.py?id={patient_id}">🏠 Dashboard</a></li>
<li><a href="patient-upcoming-appointments.py?id={patient_id}">⏳ Upcoming Appointments</a></li>
<li><a href="patient-book-appointments.py?id={patient_id}" class="active">📅 Book Appointments</a></li>
<li><a href="patient-past-appointments.py?id={patient_id}">🗓 Past Appointments</a></li>
<li><a href="patient-profile.py?id={patient_id}">👤 Profile</a></li>
<li><a href="patient-medical-records.py?id={patient_id}">📄 Medical Records</a></li>
<li><a href="index.py">🚪 Logout</a></li>
</ul>
</aside>
<main class="main-content">
<header class="topbar">
<button class="menu-btn">☰</button>
<h1 class="page-title">Appointment Booking</h1>
</header>
<section class="content">
<div id="msg" style="display:none;"></div>
<form id="bookAppointmentForm" method="post" enctype="multipart/form-data">
<input type="hidden" name="id" value="{patient_id}">
<input type="hidden" name="doctorId" id="doctorId">
<div class="form-group"><label>Patient Name</label><input type="text" name="patientName" required></div>
<div class="form-group"><label>Date of Birth</label><input type="date" name="dob" required></div>
<div class="form-group"><label>Gender</label><select name="gender" required>
<option value="">Select</option><option>Male</option><option>Female</option><option>Other</option></select></div>
<div class="form-group"><label>Age</label><input type="number" name="age" min="1" max="120" required></div>
<div class="form-group"><label>Specialization</label><select name="specialist" id="specialist" required><option value="">Select</option>""")

for sp in specializations:
    print(f"<option value='{sp}'>{sp}</option>")

print("</select></div><div class='form-group'><label>Select Doctor</label><select name='doctor' id='doctor' required><option value=''>Select</option>")

for doc in all_doctors:
    print(f"<option value='{doc['name']}' data-id='{doc['id']}'>{doc['name']}</option>")

print(f"""</select></div>
<div class="form-group half-width"><label>Appointment Date</label><input type="date" name="date" min="{today}" required></div>
<div class="form-group half-width"><label>Appointment Time</label><input type="time" name="time" min="09:00" max="20:00" required></div>
<div class="form-group full-width"><label>Reason</label><textarea name="reason" required></textarea></div>
<div class="upload-area full-width" onclick="document.getElementById('medicalRecords').click()">
<img src="upload_area.png" alt="Upload Icon"/>
<p>Upload Medical Records (Optional)</p>
<input type="file" name="medicalRecords" id="medicalRecords" accept=".pdf,.jpg,.png" hidden>
</div>
<div class="form-buttons full-width">
<input type="submit" class="submit-btn" value="Book Appointment" name="sub">
<input type="button" class="cancel-btn" value="Cancel" id="cancelBtn">
</div></form></section></main></div>
<script>
document.querySelector(".menu-btn").addEventListener("click",function(){{document.getElementById("sidebar").classList.toggle("open");}});
document.querySelector(".close-sidebar").addEventListener("click",function(){{document.getElementById("sidebar").classList.toggle("open");}});
document.getElementById("cancelBtn").addEventListener("click",function(){{window.location.href="patient-dashboard.py?id={patient_id}";}});
document.getElementById("specialist").addEventListener("change",function(){{
var xhr=new XMLHttpRequest();xhr.open("GET","patient-book-appointments.py?ajax=1&specialization="+this.value,true);
xhr.onreadystatechange=function(){{if(xhr.readyState===4 && xhr.status===200){{
var doctorSelect=document.getElementById("doctor"); doctorSelect.innerHTML='<option value="">Select</option>';
JSON.parse(xhr.responseText).forEach(function(doc){{
var opt=document.createElement("option"); opt.value=doc.name; opt.text=doc.name; opt.setAttribute("data-id", doc.id); doctorSelect.appendChild(opt);
}});
}}}};xhr.send();}});
document.getElementById("doctor").addEventListener("change",function(){{
var selected=this.options[this.selectedIndex];document.getElementById("doctorId").value=selected.getAttribute("data-id");}});
</script>
</body></html>""")

# Backend processing
Submit = form.getvalue("sub")
if Submit:
    try:
        Patient_name = form.getvalue("patientName")
        Doctor_name = form.getvalue("doctor")
        Doctor_id = form.getvalue("doctorId")
        Dob = form.getvalue("dob")
        Gender = form.getvalue("gender")
        Age = int(form.getvalue("age"))
        Specialist = form.getvalue("specialist")
        Appointment_date = form.getvalue("date")
        Appointment_time = form.getvalue("time")
        Reason = form.getvalue("reason")

        # Validate appointment date/time
        appt_date_obj = datetime.datetime.strptime(Appointment_date, "%Y-%m-%d").date()
        today_date = datetime.date.today()
        now_time = datetime.datetime.now().time()
        appt_time_obj = datetime.datetime.strptime(Appointment_time, "%H:%M").time()
        if appt_date_obj < today_date:
            print("content-type: text/html\n")
            print("<div>Appointments can only be booked for today or future dates</div>")
            sys.exit()
        if not(datetime.time(9,0) <= appt_time_obj <= datetime.time(20,0)):
            print("content-type: text/html\n")
            print("<div>Appointments can only be booked between 9 AM and 8 PM</div>")
            sys.exit()
        if appt_date_obj == today_date and appt_time_obj <= now_time:
            print("content-type: text/html\n")
            print("<div>For today, appointment time must be after current time</div>")
            sys.exit()

        # Handle optional medical record upload
        medical_record_path = ""
        if "medicalRecords" in form:
            fileitem = form["medicalRecords"]
            if getattr(fileitem,"filename",None):
                upload_dir = "uploads/medical_records"
                os.makedirs(upload_dir,exist_ok=True)
                filename = os.path.basename(fileitem.filename)
                filepath = os.path.join(upload_dir, filename)
                with open(filepath,"wb") as f:
                    f.write(fileitem.file.read())
                medical_record_path = filepath

        # Fetch hospital name and address from doctor_register
        cur.execute("SELECT Hospital_name, Hospital_address FROM doctor_register WHERE id=%s", (Doctor_id,))
        result = cur.fetchone()
        hospital_name, hospital_address = (result if result else ("",""))

        # Insert appointment
        q = """INSERT INTO appointments 
        (patient_id, patient_name, doctor_id, doctor_name, Dob, Gender, Age, Specialization, 
        appointment_date, appointment_time, reason, medical_records, Hospital_name, Hospital_address, status) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'Pending')"""
        cur.execute(q, (patient_id, Patient_name, Doctor_id, Doctor_name, Dob, Gender, Age, Specialist,
                        Appointment_date, Appointment_time, Reason, medical_record_path, hospital_name, hospital_address))

        con.commit()
        print("content-type:text/html \r\n\r\n")
        print(f"<div>Appointment booked successfully! <a href='patient-upcoming-appointments.py?id={patient_id}'>Go to Upcoming</a></div>")

    except Exception as e:
        print("content-type: text/html\n")
        print(f"<div>Error: {str(e)}</div>")
