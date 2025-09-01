#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("Content-Type: text/html\n")
import pymysql, cgi, cgitb, sys, os, datetime, shutil
cgitb.enable()

# ---------------- DB ----------------
con = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="appointment_booking_system",
    charset="utf8mb4"
)
cur = con.cursor()
sys.stdout.reconfigure(encoding='utf-8')

form = cgi.FieldStorage()
user_id = form.getvalue("id")  # Doctor ID from login redirect
if not user_id:
    user_id = "0"

# ---------- Helpers ----------
def col_exists(table, col):
    try:
        cur.execute(f"SHOW COLUMNS FROM `{table}` LIKE %s", (col,))
        return cur.fetchone() is not None
    except:
        return False

def first_existing_col(table, candidates):
    for c in candidates:
        if col_exists(table, c):
            return c
    return None

# ensure upload folders exist
upload_base = "uploads"
pres_dir = os.path.join(upload_base, "prescriptions")
med_dir = os.path.join(upload_base, "medical_records")
for d in [upload_base, pres_dir, med_dir]:
    if not os.path.exists(d):
        os.makedirs(d)

def safe_save(field, subdir):
    """Save file to uploads/subdir with unique name and return relative path"""
    if field is not None and getattr(field, "filename", None):
        base = os.path.basename(field.filename)
        name, ext = os.path.splitext(base)
        stamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        final_name = f"{name}_{stamp}{ext}"
        folder = os.path.join(upload_base, subdir)
        if not os.path.exists(folder):
            os.makedirs(folder)
        path = os.path.join(folder, final_name)
        with open(path, "wb") as f:
            shutil.copyfileobj(field.file, f)
        return path.replace("\\", "/")
    return ""

# ---------- STEP 1: Move past appointments ----------
def get_appointments():
    date_col = first_existing_col("appointments", ["appointment_date", "date"])
    time_col = first_existing_col("appointments", ["appointment_time", "time"])
    amount_col = first_existing_col("appointments", ["amount", "fees", "fee"])
    reason_col = first_existing_col("appointments", ["reason", "reason_for_booking"])
    pname_col = first_existing_col("appointments", ["patient_name"])
    dname_col = first_existing_col("appointments", ["doctor_name"])
    dob_col   = first_existing_col("appointments", ["dob"])
    age_col   = first_existing_col("appointments", ["age"])
    spec_col  = first_existing_col("appointments", ["specialization"])
    gender_col= first_existing_col("appointments", ["gender"])

    cur.execute(f"""
        SELECT id, patient_id, doctor_id,
               {reason_col if reason_col else "NULL"} as reason,
               {date_col} as appt_date,
               {time_col} as appt_time,
               {amount_col if amount_col else "0"} as amt,
               {pname_col if pname_col else "NULL"} as patient_name,
               {dname_col if dname_col else "NULL"} as doctor_name,
               {dob_col if dob_col else "NULL"} as dob,
               {age_col if age_col else "NULL"} as age,
               {spec_col if spec_col else "NULL"} as specialization,
               {gender_col if gender_col else "NULL"} as gender
        FROM appointments
        WHERE doctor_id=%s
    """, (user_id,))
    return cur.fetchall(), date_col, time_col

def parse_dt(date_val, time_val):
    s_date = str(date_val)
    s_time = str(time_val)
    fmt_try = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"]
    for f in fmt_try:
        try:
            return datetime.datetime.strptime(s_date + " " + s_time, f)
        except:
            continue
    try:
        s_time2 = s_time[:5]
        return datetime.datetime.strptime(s_date + " " + s_time2, "%Y-%m-%d %H:%M")
    except:
        return None

now = datetime.datetime.now()
ah_cols = {}
for col in ["doctor_id","patient_id","patient_name","doctor_name","age","dob","specialization",
            "gender","amount","consultation","appointment_time","appointment_date","prescription","medical_record",
            "status","satus","reason","reason_for_booking"]:
    ah_cols[col] = col_exists("appointment_history", col)

appointments, date_col, time_col = get_appointments()

for appt in appointments:
    appt_id, patient_id, doctor_id, reason, date_val, time_val, amt, pname, dname, dob, age, spec, gender = appt
    appt_dt = parse_dt(date_val, time_val)
    if appt_dt and appt_dt < now:
        insert_cols = []
        insert_vals = []

        if ah_cols.get("patient_id"):
            insert_cols.append("patient_id"); insert_vals.append(patient_id)
        if ah_cols.get("doctor_id"):
            insert_cols.append("doctor_id"); insert_vals.append(doctor_id)
        if ah_cols.get("patient_name"):
            insert_cols.append("patient_name"); insert_vals.append(pname or "")
        if ah_cols.get("doctor_name"):
            insert_cols.append("doctor_name"); insert_vals.append(dname or "")
        if ah_cols.get("dob"):
            insert_cols.append("dob"); insert_vals.append(dob or "")
        if ah_cols.get("age"):
            insert_cols.append("age"); insert_vals.append(age or "")
        if ah_cols.get("specialization"):
            insert_cols.append("specialization"); insert_vals.append(spec or "")
        if ah_cols.get("gender"):
            insert_cols.append("gender"); insert_vals.append(gender or "")

        if ah_cols.get("reason"):
            insert_cols.append("reason"); insert_vals.append(reason or "")
        elif ah_cols.get("reason_for_booking"):
            insert_cols.append("reason_for_booking"); insert_vals.append(reason or "")

        if ah_cols.get("amount"):
            insert_cols.append("amount"); insert_vals.append(amt or 0)
        if ah_cols.get("appointment_date"):
            insert_cols.append("appointment_date"); insert_vals.append(str(date_val))
        if ah_cols.get("appointment_time"):
            insert_cols.append("appointment_time"); insert_vals.append(str(time_val))

        if ah_cols.get("consultation"):
            insert_cols.append("consultation"); insert_vals.append("")
        if ah_cols.get("prescription"):
            insert_cols.append("prescription"); insert_vals.append("")
        if ah_cols.get("medical_record"):
            insert_cols.append("medical_record"); insert_vals.append("")

        if ah_cols.get("status"):
            insert_cols.append("status"); insert_vals.append("completed")
        elif ah_cols.get("satus"):
            insert_cols.append("satus"); insert_vals.append("completed")

        if insert_cols:
            placeholders = ",".join(["%s"] * len(insert_vals))
            cols_sql = ",".join(f"`{c}`" for c in insert_cols)
            cur.execute(f"INSERT INTO `appointment_history` ({cols_sql}) VALUES ({placeholders})", tuple(insert_vals))
            cur.execute("DELETE FROM `appointments` WHERE id=%s", (appt_id,))
            con.commit()

# ---------- STEP 2: Uploads ----------
action = form.getvalue("action") or ""

if action == "upload":
    history_id = form.getvalue("history_id")
    prescription = form["prescription"] if "prescription" in form else None
    medical = form["medical"] if "medical" in form else None

    pres_path = safe_save(prescription, "prescriptions")
    med_path = safe_save(medical, "medical_records")

    pres_col = "prescription" if ah_cols.get("prescription") else first_existing_col("appointment_history", ["prescription_file"])
    med_col  = "medical_record" if ah_cols.get("medical_record") else first_existing_col("appointment_history", ["medical_record_file"])

    sets = []
    vals = []
    if pres_path and pres_col:
        sets.append(f"`{pres_col}`=%s"); vals.append(pres_path)
    if med_path and med_col:
        sets.append(f"`{med_col}`=%s"); vals.append(med_path)

    if sets:
        sets_sql = ", ".join(sets)
        cur.execute(f"UPDATE `appointment_history` SET {sets_sql} WHERE id=%s AND doctor_id=%s", (*vals, history_id, user_id))
        con.commit()

elif action == "save_consultation":
    history_id = form.getvalue("history_id")
    text = form.getvalue("consultation_text") or ""
    if ah_cols.get("consultation"):
        cur.execute("UPDATE `appointment_history` SET `consultation`=%s WHERE id=%s AND doctor_id=%s",
                    (text, history_id, user_id))
        con.commit()

# ---------- STEP 3: Fetch appointment history ----------
pname_col = first_existing_col("appointment_history", ["patient_name"])
dname_col = first_existing_col("appointment_history", ["doctor_name"])
age_col   = first_existing_col("appointment_history", ["age"])
dob_col   = first_existing_col("appointment_history", ["dob"])
gender_col= first_existing_col("appointment_history", ["gender"])
spec_col  = first_existing_col("appointment_history", ["specialization"])
reason_col_ah = first_existing_col("appointment_history", ["reason","reason_for_booking"])
date_col_ah = first_existing_col("appointment_history", ["appointment_date", "date"])
time_col_ah = first_existing_col("appointment_history", ["appointment_time", "time"])
amount_col_ah = first_existing_col("appointment_history", ["amount","fees","fee"])
consult_col = first_existing_col("appointment_history", ["consultation","consultation_summary"])
pres_col = first_existing_col("appointment_history", ["prescription","prescription_file"])
med_col = first_existing_col("appointment_history", ["medical_record","medical_record_file"])

cols_select = ["id"]
for c in [pname_col, dname_col, age_col, dob_col, gender_col, spec_col, reason_col_ah, date_col_ah, time_col_ah, amount_col_ah, consult_col, pres_col, med_col]:
    cols_select.append(c if c else "NULL")

select_sql = ", ".join([f"`{c}`" if c not in (None,"NULL") else "NULL" for c in cols_select])

cur.execute(f"""
    SELECT {select_sql}
    FROM `appointment_history`
    WHERE `doctor_id`=%s
    ORDER BY {f'`{date_col_ah}`' if date_col_ah else 'id'} DESC
""", (user_id,))
history = cur.fetchall()

# ---------- HTML OUTPUT ----------
# (keep your existing HTML output code below unchanged)


# ---------- HTML OUTPUT ----------
print("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Doctor Appointment History</title>
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
    table { width: 100%; border-collapse: collapse; min-width: 1200px; }
    table th, table td { border: 1px solid #ddd; padding: 10px; text-align: left; font-size: 14px; }
    table th { background: #5f6FFF; color: #fff; position: sticky; top: 0; }
    table tr:nth-child(even) { background: #f2f2f2; }
    table tr:hover { background: #e6e6e6; }
    .upload-btn { background: #5f6FFF; color: white; padding: 6px 12px; border: none; border-radius: 5px; cursor: pointer; }
    /* Modal */
    .modal { display: none; position: fixed; z-index: 1001; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background: rgba(0,0,0,0.5); }
    .modal-content { background: #fff; margin: 10% auto; padding: 20px; border-radius: 8px; width: 400px; }
    .modal textarea { width: 100%; height: 100px; }
    .modal-buttons { margin-top: 10px; text-align: right; }
    .modal-buttons button { margin-left: 10px; padding: 6px 12px; }
    @media (max-width: 768px) {
      .sidebar { position: fixed; left: 0; top: 0; height: 100%; transform: translateX(-100%); z-index: 1000; }
      .sidebar.open { transform: translateX(0); }
      .close-sidebar { display: block; }
      .menu-btn { display: block; }
      table { font-size: 12px; }
    }
  </style>
  <script>
    function toggleSidebar() {
      document.getElementById("sidebar").classList.toggle("open");
    }
    function openConsultModal(id, existingText) {
      document.getElementById("consultModal").style.display = "block";
      document.getElementById("history_id_input").value = id;
      document.getElementById("consultation_text").value = existingText || "";
    }
    function closeConsultModal() {
      document.getElementById("consultModal").style.display = "none";
    }
    function openUploadModal(id) {
      document.getElementById("uploadModal").style.display = "block";
      document.getElementById("upload_history_id").value = id;
    }
    function closeUploadModal() {
      document.getElementById("uploadModal").style.display = "none";
    }
    function openViewModal(pres, med) {
      document.getElementById("viewModal").style.display = "block";
      let html = "<p><strong>Prescription:</strong> <a href='" + pres + "' target='_blank'>View</a></p>";
      if(med) html += "<p><strong>Medical Record:</strong> <a href='" + med + "' target='_blank'>View</a></p>";
      document.getElementById("viewContent").innerHTML = html;
    }
    function closeViewModal() {
      document.getElementById("viewModal").style.display = "none";
    }
  </script>
</head>
<body>
""")

print(f"""
<div class="dashboard-container">
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <h2>Prescripto</h2>
      <button class="close-sidebar" onclick="toggleSidebar()">×</button>
    </div>
    <ul class="sidebar-menu">
      <li><a href="doctor-dashboard.py?id={user_id}">📊 Dashboard</a></li>
      <li><a href="doctor-appointment-history.py?id={user_id}" class="active">📅 Appointment History</a></li>
      <li><a href="doctor-upcoming-appointments.py?id={user_id}">⏳ Upcoming Appointments</a></li>
      <li><a href="doctor-cancelled-appointments.py?id={user_id}">❌ Cancelled Appointments</a></li>
      <li><a href="doctor-profile.py?id={user_id}">👤 Profile</a></li>
      <li><a href="index.py">🚪 Logout</a></li>
    </ul>
  </aside>

  <main class="main-content">
    <header class="topbar">
      <button class="menu-btn" onclick="toggleSidebar()">☰</button>
      <h1>Appointment History</h1>
    </header>

    <section class="content">
      <h2>Past Consultations</h2>
      <div style="overflow-x:auto;">
        <table>
          <thead>
            <tr>
              <th>Patient Name</th>
              <th>Doctor Name</th>
              <th>Age</th>
              <th>DOB</th>
              <th>Gender</th>
              <th>Specialization</th>
              <th>Reason</th>
              <th>Date</th>
              <th>Time</th>
              <th>Fees</th>
              <th>Consultation/Summary</th>
              <th>Upload Records</th>
            </tr>
          </thead>
          <tbody>
""")

for row in history:
    (
        hid, pname, dname, age, dob, gender, spec, reason,
        date_val, time_val, amt, consult, pres, med
    ) = row

    print(f"""
    <tr>
      <td>{pname or ''}</td>
      <td>{dname or ''}</td>
      <td>{age or ''}</td>
      <td>{dob or ''}</td>
      <td>{gender or ''}</td>
      <td>{spec or ''}</td>
      <td>{reason or ''}</td>
      <td>{date_val or ''}</td>
      <td>{time_val or ''}</td>
      <td>{amt or ''}</td>
      <td>
        <button class="upload-btn" onclick="openConsultModal('{hid}', `{consult or ''}`)">Edit</button>
        <br/>
        {consult or ''}
      </td>
      <td>
        <button class="upload-btn" onclick="openUploadModal('{hid}')">Upload</button>
        <br/>
        <button class="upload-btn" onclick="openViewModal('{pres or ''}', '{med or ''}')">View</button>
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

<!-- Consultation Modal -->
<div id="consultModal" class="modal">
  <div class="modal-content">
    <h3>Consultation Summary</h3>
    <form method="post">
      <input type="hidden" name="action" value="save_consultation">
      <input type="hidden" id="history_id_input" name="history_id">
      <textarea id="consultation_text" name="consultation_text"></textarea>
      <div class="modal-buttons">
        <button type="button" onclick="closeConsultModal()">Cancel</button>
        <button type="submit">Save</button>
      </div>
    </form>
  </div>
</div>

<!-- Upload Modal -->
<div id="uploadModal" class="modal">
  <div class="modal-content">
    <h3>Upload Records</h3>
    <form method="post" enctype="multipart/form-data">
      <input type="hidden" name="action" value="upload">
      <input type="hidden" id="upload_history_id" name="history_id">
      <p><label>Prescription: <input type="file" name="prescription"></label></p>
      <p><label>Medical Record: <input type="file" name="medical"></label></p>
      <div class="modal-buttons">
        <button type="button" onclick="closeUploadModal()">Cancel</button>
        <button type="submit">Upload</button>
      </div>
    </form>
  </div>
</div>

<!-- View Modal -->
<div id="viewModal" class="modal">
  <div class="modal-content">
    <h3>View Records</h3>
    <div id="viewContent"></div>
    <div class="modal-buttons">
      <button type="button" onclick="closeViewModal()">Close</button>
    </div>
  </div>
</div>

</body>
</html>
""")
