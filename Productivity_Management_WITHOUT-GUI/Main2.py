import getpass
import json
import os
from datetime import datetime, timedelta

# THIS IS FOR SAVING ACCOUNTS IN JSON
DB_FILE = "productivity_data.json"
users = {}

def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)
        
def create_account():
    print("\n" + "-"*22)
    print("| CREATE NEW ACCOUNT |")
    print("-"*22,"\n")
    
    username = input("Username: ").strip()
    if username in users:
        print("Username already exists!")
        return

    password = getpass.getpass("Password: ").strip()
    confirm_password = getpass.getpass("Confirm Password: ").strip()

    if password == confirm_password:
        users[username] = {
            "password": password,
            "total_distractions": 0,
            "projects_completed": 0,
            "projects": [],
            "group_projects": [],
            "invites": []
        }
        save_data(users)
        print(f"\nAccount created successfully! Welcome '{username}'!")
    else:
        print("Passwords do not match.")
    
def login():
    print("\n" + "-"*9)
    print("| LOGIN |")
    print("-"*9)
    
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").strip()

    if username in users and users[username]["password"] == password:
        print("\nSuccessfully logged in.")
        print(f"Welcome back, {username}!\n")
        
        stats = users[username]
        print(f"--- Session Stats: {stats.get('total_distractions', 0)} Distractions Logged ---")
        main_menu(username)
    else:
        print("Invalid username or password.")

def productivity_management_system():
    global users
    while True:
        users = load_data()
        print("\n" + "-"*32)
        print("| PRODUCTIVITY MANAGEMENT SYSTEM |")
        print("-"*32,"\n")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting Program.")
            break
        else:
            print("Invalid input.")

def main_menu(username):
    title_text = f"|  MAIN MENU - {username}  |"
    width = len(title_text)
    
    while True:
        print("\n" + "-" * width)
        print(title_text)
        print("-" * width)
        
        print("1. View All Projects (Solo & Group)")
        print("2. Project Creation Menu")
        print("3. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            view_projects(username)
        elif choice == "2":
            project_creation_menu(username)
        elif choice == "3":
            print(f"Logging out {username}...")
            break 
        else:
            print("Invalid choice.")

def project_creation_menu(username):
    while True:
        title_text = f"|  PROJECT CREATION MENU - {username}  |"
        width = len(title_text)
        
        print("\n" + "-" * width)
        print(title_text)
        print("-" * width)
        print("1. Solo Project Menu")
        print("2. Group Project Menu")
        print("3. Back")
        
        type_choice = input("Enter choice: ").strip()

        if type_choice == "1":
            solo_project_menu(username)
        elif type_choice == "2":
            group_project_menu(username)
        elif type_choice == "3":
            break

def solo_project_menu(username):
    while True:
        title_text = f"|  SOLO PROJECT MENU - {username}  |"
        width = len(title_text)
        
        print("\n" + "-" * width)
        print(title_text)
        print("-" * width)
        print("1. View/Manage Solo Projects")
        print("2. Create New Solo Project")
        print("3. Back")
        
        choice = input("\nEnter choice: ").strip()
        if choice == "1":
            view_solo_project(username) 
        elif choice == "2":
            solo_project_create(username) 
        elif choice == "3":
            break

def solo_project_create(username):
    print("\nCreating new solo project...\n")        
    project_name = input("Project Name: ").strip()
    deadline = input("Set Deadline (YYYY-MM-DD): ").strip()

    new_project = {
        "type": "Solo",
        "name": project_name,
        "deadline": deadline,
        "progress": 0,
        "tasks": [],
        "distractions_logged": 0,
        "status": "In Progress"
    }

    if "projects" not in users[username]:
        users[username]["projects"] = []
    
    users[username]["projects"].append(new_project)
    save_data(users)
    print(f"\nProject '{project_name}' created!")

def view_solo_project(username):
    while True:
        title_text = f"|  {username.upper()}'S SOLO PROJECTS  |"
        width = len(title_text)
        print("\n" + "-" * width)
        print(title_text)
        print("-" * width)
    
        user_projects = users[username].get("projects", [])

        if not user_projects:
            print("\n[!] No solo projects found.")
            break
        
        for i, proj in enumerate(user_projects, 1):
            print(f"{i}. [{proj['progress']}%] {proj['name']} - {proj['status']}")
            print(f"   Deadline: {proj['deadline']}")
            print("-" * 20)
        
        choice = input("\nSelect number to manage (0 to back): ").strip()
        if choice == "0": break
        if choice.isdigit() and 1 <= int(choice) <= len(user_projects):
            manage_single_project(username, int(choice) - 1)

def view_projects(username):
    # INTEGRATED INVITE CHECK
    check_invites(username)
    
    while True:
        title_text = f"|  {username.upper()}'S GLOBAL DASHBOARD  |"
        width = len(title_text)
        print("\n" + "-" * width)
        print(title_text)
        print("-" * width)
        
        solo_projects = users[username].get("projects", [])
        leader_groups = users[username].get("group_projects", [])
        member_groups = []
        for owner, data in users.items():
            for p in data.get("group_projects", []):
                if username in p.get("members", []) and p.get("leader") != username:
                    member_groups.append(p)

        master_list = []
        for p in solo_projects: master_list.append((p, "[SOLO]", "SOLO"))
        for p in leader_groups: master_list.append((p, "[GROUP]", "LEADER"))
        for p in member_groups: master_list.append((p, "[GROUP]", "MEMBER"))

        if not master_list:
            print("\n[!] No projects found.")
            break
        
        for i, (proj, p_type, role) in enumerate(master_list, 1):
            prog = proj.get("progress", 0)
            deadline = proj.get("deadline", "")
            urgency = ""
            if prog < 100 and deadline:
                try:
                    days_left = (datetime.strptime(deadline, "%Y-%m-%d").date() - datetime.now().date()).days
                    if days_left < 0: urgency = " [!! OVERDUE !!]"
                    elif days_left <= 3: urgency = f" [! DUE IN {days_left} DAYS !]"
                except: urgency = " [Date Error]"

            print(f"{i}. {p_type} [{role}] {proj['name']} - {prog}% {urgency}")
            print("-" * 30)
        
        choice = input("\nSelect project (0 to back): ").strip()
        if choice == "0": break
        if choice.isdigit() and 1 <= int(choice) <= len(master_list):
            sel_proj, p_type, role = master_list[int(choice) - 1]
            if p_type == "[SOLO]":
                manage_single_project(username, solo_projects.index(sel_proj))
            else:
                manage_group_project(username, sel_proj, f"[{role}]")

def manage_single_project(username, index):
    project = users[username]["projects"][index]
    while True:
        print(f"\n--- {project['name']} ---")
        print(f"Progress: {project['progress']}% | Distractions: {project['distractions_logged']}")
        print("1. Update Progress\n2. Log Distraction\n3. Complete\n4. Back")
        
        c = input("Choice: ").strip()
        if c == "1":
            v = input("New %: ").strip()
            if v.isdigit(): project["progress"] = int(v)
        elif c == "2":
            project["distractions_logged"] += 1
            users[username]["total_distractions"] += 1
        elif c == "3":
            project["progress"] = 100
            break
        elif c == "4": break
        save_data(users)

def group_project_menu(username):
    while True:
        print(f"\n--- GROUP MENU - {username} ---")
        print("1. View Group Projects\n2. Create Group Project\n3. Back")
        c = input("Choice: ").strip()
        if c == "1": view_group_projects(username)
        elif c == "2": group_project_create(username)
        elif c == "3": break

def view_group_projects(username):
    check_invites(username)
    while True:
        leader_projs = users[username].get("group_projects", [])
        member_projs = []
        for owner, data in users.items():
            for p in data.get("group_projects", []):
                if username in p["members"] and p["leader"] != username:
                    member_projs.append(p)

        display_list = [(p, "[LEADER]") for p in leader_projs] + [(p, "[MEMBER]") for p in member_projs]
        if not display_list:
            print("No group projects."); break

        for i, (p, r) in enumerate(display_list, 1):
            print(f"{i}. {r} {p['name']} - {p['progress']}%")

        choice = input("\nSelect project (0 to back): ").strip()
        if choice == "0": break
        if choice.isdigit() and 1 <= int(choice) <= len(display_list):
            p, r = display_list[int(choice)-1]
            manage_group_project(username, p, r)

def group_project_create(username):
    print("\n| CREATE GROUP PROJECT |")
    name = input("Project Name: ").strip()
    deadline = input("Deadline (YYYY-MM-DD): ").strip()
    m_input = input("Invite members (comma-separated): ").strip()
    potential = [m.strip() for m in m_input.split(",") if m.strip() and m.strip() != username]

    new_project = {
        "name": name, "deadline": deadline, "progress": 0, "tasks": [],
        "distractions_logged": 0, "leader": username, "members": [username]
    }

    for m in potential:
        if m in users:
            if "invites" not in users[m]: users[m]["invites"] = []
            users[m]["invites"].append({"project_name": name, "sender": username})
            print(f"INVITE SENT TO: {m}")

    if "group_projects" not in users[username]: users[username]["group_projects"] = []
    users[username]["group_projects"].append(new_project)
    save_data(users)

def manage_group_project(username, project, role):
    while True:
        print(f"\n--- {project['name']} ({role}) ---")
        print(f"Progress: {project['progress']}% | Distractions: {project['distractions_logged']}")
        
        if role == "[LEADER]":
            print("1. Update Progress\n2. Log Distraction\n3. Manage Members\n4. Assign Tasks\n5. Back")
            c = input("Choice: ").strip()
            if c == "1":
                v = input("New %: ").strip()
                if v.isdigit(): project["progress"] = int(v)
            elif c == "2":
                project["distractions_logged"] += 1
                for m in project["members"]: users[m]["total_distractions"] = users[m].get("total_distractions",0) + 1
            elif c == "3": manage_group_members(project)
            elif c == "4": assign_group_task(project)
            elif c == "5": break
        else:
            print("1. Update Progress/Tasks\n2. Log Distraction\n3. Back")
            c = input("Choice: ").strip()
            if c == "1":
                v = input("Update overall % (Enter to skip): ").strip()
                if v.isdigit(): project["progress"] = int(v)
                view_member_tasks(username, project)
            elif c == "2":
                project["distractions_logged"] += 1
                users[username]["total_distractions"] = users[username].get("total_distractions",0) + 1
            elif c == "3": break
        save_data(users)

def manage_group_members(project):
    print(f"Current: {', '.join(project['members'])}")
    print("1. Add\n2. Remove\n3. Back")
    c = input("Choice: ").strip()
    if c == "1":
        m = input("Username: ").strip()
        if m in users and m not in project["members"]: project["members"].append(m)
    elif c == "2":
        m = input("Username: ").strip()
        if m in project["members"] and m != project["leader"]: project["members"].remove(m)
    save_data(users)

def check_invites(username):
    invites = users[username].get("invites", [])
    if not invites: return
    print(f"\n--- {username.upper()}'S INVITES ---")
    for i, inv in enumerate(invites, 1):
        print(f"{i}. {inv['sender']} invited you to: {inv['project_name']}")
    
    c = input("Accept number? (n to skip): ").strip()
    if c.isdigit() and 1 <= int(c) <= len(invites):
        acc = invites.pop(int(c)-1)
        for p in users[acc['sender']].get("group_projects", []):
            if p['name'] == acc['project_name']:
                p['members'].append(username); break
        save_data(users)

def view_member_tasks(username, project):
    my_tasks = [t for t in project.get("tasks", []) if username in t.get("assigned_to", [])]
    if not my_tasks: print("No tasks assigned."); return
    for i, t in enumerate(my_tasks, 1):
        print(f"{i}. [{'DONE' if t['is_done'] else 'PENDING'}] {t['task_name']}")
    c = input("Mark done (number) or n: ").strip()
    if c.isdigit() and 1 <= int(c) <= len(my_tasks):
        my_tasks[int(c)-1]['is_done'] = True
        save_data(users)

def assign_group_task(project):
    desc = input("Task: ").strip()
    target_input = input(f"Assign to ({', '.join(project['members'])}): ").strip()
    targets = [t.strip() for t in target_input.split(",") if t.strip() in project['members']]
    if targets:
        project["tasks"].append({"task_name": desc, "assigned_to": targets, "is_done": False})
        save_data(users)

pms = productivity_management_system

if __name__ == "__main__":
    users = load_data()
    pms()