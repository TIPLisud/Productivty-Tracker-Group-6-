<div align="center">

# Productivity Management System
<h3 align="center" style="color:gray;">A High-Performance Python GUI for Tracking Workflows</h3>

<img src="https://i.pinimg.com/originals/39/7b/c2/397bc20ad2da1a5920c1347052aea03d.gif" width="100%" height="150px" style="object-fit: cover; border-radius: 10px;"/>

<pre>
 ██████   ██████  ██████      ███████ ██ ███    ██  █████  ██          ██████  ██████   ██████       ██ ███████  ██████ ████████
██    ██ ██    ██ ██   ██     ██      ██ ████   ██ ██   ██ ██          ██   ██ ██   ██ ██    ██      ██ ██      ██         ██   
██    ██ ██    ██ ██████      █████   ██ ██ ██  ██ ███████ ██          ██████  ██████  ██    ██      ██ █████   ██         ██   
██    ██ ██    ██ ██          ██      ██ ██  ██ ██ ██   ██ ██          ██      ██   ██ ██    ██ ██   ██ ██      ██         ██   
 ██████   ██████  ██          ██      ██ ██   ████ ██   ██ ███████     ██      ██   ██  ██████   █████  ███████  ██████    ██   
                                                                                                                                
                                                                                                                                
                 ██████ ▄▄   ▄▄ ▄▄▄▄  ▄▄     ▄▄▄  ▄▄ ▄▄ ▄▄▄▄▄ ▄▄▄▄▄   █████▄ ▄▄▄▄   ▄▄▄    ▄▄ ▄▄▄▄▄  ▄▄▄▄ ▄▄▄▄▄▄                
                 ██▄▄   ██▀▄▀██ ██▄█▀ ██    ██▀██ ▀███▀ ██▄▄  ██▄▄    ██▄▄█▀ ██▄█▄ ██▀██   ██ ██▄▄  ██▀▀▀   ██                  
                 ██▄▄▄▄ ██   ██ ██    ██▄▄▄ ▀███▀   █   ██▄▄▄ ██▄▄▄   ██     ██ ██ ▀███▀ ▄▄█▀ ██▄▄▄ ▀████   ██                  
                                                                                                                                
          ██▄  ▄██  ▄▄▄  ▄▄  ▄▄  ▄▄▄   ▄▄▄▄ ▄▄▄▄▄ ▄▄   ▄▄ ▄▄▄▄▄ ▄▄  ▄▄ ▄▄▄▄▄▄   ▄█████ ▄▄ ▄▄  ▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄ ▄▄   ▄▄         
          ██ ▀▀ ██ ██▀██ ███▄██ ██▀██ ██ ▄▄ ██▄▄  ██▀▄▀██ ██▄▄  ███▄██   ██     ▀▀▀▄▄▄ ▀███▀ ███▄▄   ██   ██▄▄  ██▀▄▀██         
          ██    ██ ██▀██ ██ ▀██ ██▀██ ▀███▀ ██▄▄▄ ██   ██ ██▄▄▄ ██ ▀██   ██     █████▀   █   ▄▄██▀   ██   ██▄▄▄ ██   ██         
</pre>



<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Tkinter-GUI-blue?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Data-JSON-lightgray?style=for-the-badge&logo=json&logoColor=white"/>
</p>

</div>

---

## 👥 The Development Team
<p align="center">
  <b>Ian Paulo Lisud</b> • <b>Jesse Matthew Esteta</b> • <b>Jiro Luis Katindig</b><br>
  <b>Francis Elijah Formalejo</b> • <b>Marqui Cenar</b>
</p>

---

**📌 Overview**   
The Productivity Management System is a command-line based application designed to help users efficiently manage their tasks, projects, and overall productivity. It allows users to create accounts, track personal and group projects, monitor progress, and log distractions to improve focus and performance.  
  
The system supports both solo and collaborative workflows, enabling users to work independently or as part of a team. With built-in features such as deadlines, task assignment, and project tracking, the application helps users stay organized and meet their goals effectively.  
  

---

## ⚙️ Core Modules
<table align="center">
  <tr>
    <td align="center"><b>🔐 Authentication.py</b><br>Secure login logic & session handling</td>
    <td align="center"><b>🖥️ Dashboard.py</b><br>Main GUI window & user interface</td>
  </tr>
  <tr>
    <td align="center"><b>💾 Database.py</b><br>Local JSON storage & data CRUD</td>
    <td align="center"><b>🛠️ Config.py</b><br>System constants & global settings</td>
  </tr>
</table>

---

## ✨ Key Features
- 🚀 **Tkinter Interface:** A native desktop experience with responsive `ttk` widgets.
- 🆔 **UUID Integrity:** Every task and project is tracked with unique universal identifiers.
- 📊 **Progress Monitoring:** Real-time completion updates for both solo and group projects.
- 📅 **Deadline Tracking:** Integrated `datetime` calculations for urgent task prioritization.
- 📂 **Persistent Storage:** Data remains intact across sessions via local file-handling.

---

## 🛠️ Built With
<p align="center">
  <img src="https://skillicons.dev/icons?i=py,vscode,github,git" />
</p>
<p align="center">
  <i>Standard Libraries: <code>tkinter</code>, <code>uuid</code>, <code>datetime</code>, <code>json</code></i>
</p>

---

## 🚀 Getting Started
```bash
# 1. Clone the repository
git clone [https://github.com/your-username/productivity-tracker.git](https://github.com/your-username/productivity-tracker.git)

# 2. Navigate to the project folder
cd productivity-tracker

# 3. Run the application
python main.py


# Follow these steps to deploy the system on your local machine.

# 1. Clone the Repository
#Copy the project files from GitHub to your computer:

git clone https://github.com/katindigcpe/productivity-tracker.git

#2. Navigate to the Source
#Move into the project folder and enter the source directory where the GUI logic resides:
cd productivity-tracker/Productivity_Tracker

#3. Launch the Application
#Run the main script using Python 3:
python Main.py
```

---
## 📦 Prerequisites
- Python 3.8+
- Tkinter library (Included in most Python installations)
- Git
---
