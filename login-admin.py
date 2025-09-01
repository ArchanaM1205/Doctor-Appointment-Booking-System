#!C:/Users/archa/AppData/Local/Programs/Python/Python311/python.exe
print("content-type:text/html \r\n\r\n")
import pymysql,cgi,cgitb,sys
cgitb.enable()
form=cgi.FieldStorage()
con=pymysql.connect(host="localhost",user="root",password="",database="appointment_booking_system")
cur=con.cursor()
sys.stdout.reconfigure(encoding='utf-8')
print("""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Admin Login</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      background: #f5f7ff;
    }

    .modal-overlay {
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      background: rgba(0,0,0,0.5);
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 999;
    }

    .modal {
      background: #fff;
      width: 90%;
      max-width: 400px;
      padding: 20px 25px;
      border-radius: 10px;
      box-shadow: 0 5px 20px rgba(0,0,0,0.2);
      animation: slideDown 0.3s ease;
    }

    @keyframes slideDown {
      from { transform: translateY(-50px); opacity: 0; }
      to   { transform: translateY(0); opacity: 1; }
    }

    .modal h2 {
      text-align: center;
      color: #5f6FFF;
      margin-bottom: 20px;
    }

    .close-btn {
      float: right;
      font-size: 20px;
      border: none;
      background: none;
      cursor: pointer;
    }

    .form-group {
      margin-bottom: 15px;
    }

    .form-group label {
      display: block;
      font-size: 14px;
      margin-bottom: 5px;
    }

    .form-group input {
      width: 100%;
      padding: 10px;
      border: 1px solid #ccc;
      border-radius: 6px;
      font-size: 14px;
      outline: none;
    }

    .form-group input:focus {
      border-color: #5f6FFF;
    }

    .submit-btn {
      width: 100%;
      background: #5f6FFF;
      color: white;
      padding: 12px;
      font-size: 16px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.3s ease;
      margin-top: 10px;
    }

    .submit-btn:hover {
      background: #3d47d6;
    }

    .cancel-btn{
      width: 100%;
      background:red;
      color: white;
      padding: 12px;
      font-size: 16px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.3s ease;
      margin-top: 10px;
    }

    .cancel-btn:hover{
      background-color: darkred;
    }

    .login-footer {
      text-align: center;
      margin-top: 10px;
      font-size: 14px;
    }

    .login-footer a {
      color: #5f6FFF;
      text-decoration: none;
      font-weight: bold;
    }

    .login-footer a:hover {
      text-decoration: underline;
    }

    .forgot-password {
      text-align: right;
      font-size: 14px;
      margin-top: -10px;
      margin-bottom: 15px;
    }

    .forgot-password a {
      color: #5f6FFF;
      text-decoration: none;
    }

    .forgot-password a:hover {
      text-decoration: underline;
    }

    @media (max-width: 500px) {
      .modal {
        padding: 15px;
      }
      .modal h2 {
        font-size: 20px;
      }
    }
  </style>
</head>
<body>

  <!-- Modal -->
  <div class="modal-overlay" id="adminModal">
    <div class="modal">
      <button class="close-btn" onclick="closeModal()">×</button>
      <h2>Admin Login</h2>
      <form id="adminLoginForm">
        <div class="form-group">
          <label>Username</label>
          <input type="email" id="email" required>
        </div>
        <div class="form-group">
          <label>Password</label>
          <input type="password" id="password" required>
        </div>
        <button type="submit" class="submit-btn">Login</button>
      </form>
      <div class="login-footer">
        <button class="cancel-btn" onclick="window.location.href='index.py'">Cancel</button>
      </div>
    </div>
  </div>

  <script>
    function closeModal() {
      document.getElementById("adminModal").style.display = "none";
    }

    document.getElementById("adminLoginForm").addEventListener("submit", function(e) {
      e.preventDefault();

      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value.trim();

      const defaultUsername = "admin@prescripto.com";
      const defaultPassword = "admin123";

      if (email === defaultUsername && password === defaultPassword) {
        // Redirect to admin dashboard
        window.location.href = "admin-dashboard.py";
      } else {
        alert("Invalid username or password.");
      }
    });
  </script>

</body>
</html>

""")