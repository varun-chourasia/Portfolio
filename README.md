# 🌐 Personal Portfolio Website

Welcome to my **personal portfolio website** — a dynamic and responsive web application designed to showcase my professional profile, technical skills, and contact information.  
Built with **Python (Flask)**, integrated with **Brevo API** for email automation, and deployed on **Render Cloud**.

---

## 🧭 Overview

This project serves as my digital identity — presenting my background, skills, and featured work in an elegant, structured way.  
It includes a functional contact form powered by the **Brevo API**, allowing direct communication via automated emails.

---

## 🛠️ Tech Stack

| Category | Technologies |
|-----------|--------------|
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python (Flask Framework) |
| **Database** | PostgreSQL |
| **Email Service** | Brevo API (formerly Sendinblue) |
| **Deployment** | Render Cloud Platform |
| **Version Control** | Git & GitHub |

---

## ✨ Features

- 🎨 **Responsive UI** — clean, modern, and mobile-friendly design  
- ⚙️ **Flask Backend** — structured routes and modular logic  
- 📨 **Brevo API Integration** — handles contact form email automation  
- 🗄️ **SQLite Database** — stores and manages form data efficiently  
- 🚀 **Render Deployment** — continuous deployment from GitHub  
- 🧩 **Scalable Architecture** — maintainable, well-organized file structure  

---

## 📁 Project Structure

Portfolio/
│
├── static/ # CSS, JS, images, and static assets
├── templates/ # HTML templates
├── routes/ # Flask route files
├── utils/ # Utility functions and modules
├── models.py # Database models
├── app.py # Main Flask application
├── requirements.txt # Project dependencies
└── README.md # Project documentation

yaml
Copy code

---

## ⚙️ Installation & Setup

Follow these steps to set up the project locally:

---

# Clone the repository
git clone https://github.com/varun-chourasia/Portfolio.git

# Navigate to the project directory
cd Portfolio

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate     # On Mac/Linux
venv\Scripts\activate        # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
Now visit → http://127.0.0.1:5000/ to view your local build.

📧 Email Configuration (Brevo API)
This project integrates the Brevo API for automated contact form responses.

Create a Brevo account.

Generate your API Key from the dashboard.

Create a .env file in your project directory and add:

env
Copy code
BREVO_API_KEY=your_api_key_here
Restart your Flask app. Now all form submissions will trigger an automatic email response!

🌍 Deployment
The portfolio is deployed on Render Cloud Platform, providing:

Continuous integration with GitHub

Automatic build & deployment

SSL-secured live hosting

🔗 Live Website: https://portfolio-1l5t.onrender.com/

🧩 Future Enhancements
Add a project showcase dashboard with filters

Implement a blog or experience section

Integrate Google Analytics for visitor tracking

Add dark mode support

👤 Author
Varun Chourasia
💼 LinkedIn
🌐 Portfolio
📂 GitHub

⭐ Show Your Support
If you like this project, please star the repository — it motivates me to keep improving and building more projects!

"Turning ideas into interactive web experiences through code." 💻
