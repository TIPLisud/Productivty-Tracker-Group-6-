import getpass
import json
import os
from datetime import datetime, timedelta

#THIS IS FOR SAVING ACCOUNTS IN JSON
DB_FILE = "productivity_data.json"
users = {}

def load_data():
    #LOADS JSON, IF EMPTY RETURN EMPTY
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

users = load_data()

def save_data(data):
    #SAVES TO JSON
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

    while True:
        password = getpass.getpass("Password: ").strip()
        confirm_password = getpass.getpass("Confirm Password: ").strip()

        if password == confirm_password:
            users[username] = {
                "password": password,
                "total_distractions": 0,
                "projects_completed": 0
            }
            
        save_data(users)
        print("\nAccount created successfully!",f"Welcome '{username}'!")
        pms()
    
def login():
    #print(f"DEBUG: Current users in system: {list(users.keys())}") #FOR DEBUGGING
    print("\n" + "-"*9)
    print("| LOGIN |")
    print("-"*9)
    
    
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").strip()

 
    if username in users and users[username]["password"] == password:
        print("\nSuccessfully logged in.")
        print(f"Welcome back, {username}!\n")
        
       
        stats = users[username]
        print(f"--- Session Stats: {stats['total_distractions']} Distractions Logged ---")
        
        main_menu(username)
    else:
        print("Invalid username or password.")
        return

def productivity_management_system():
    while True:
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
            print("Invalid input. Please try again.")

def main_menu(username):
    #THIS IS FOR THE HEADER ONLY
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
            print(f"\n[SYSTEM] Loading projects for {username}...")
            view_projects(username)
            
        elif choice == "2":
            project_creation_menu(username)

        elif choice == "3":
            print(f"Logging out {username}... See you next time!")
            break 
        
        else:
            print("Invalid choice. Please try again.")

def project_creation_menu(username):
    while True:
        title_text = f"|  PROJECT CREATION MENU - {username}  |"
        width = len(title_text)
        
        print("\n" + "-" * width)
        print(title_text)
        print("-" * width)
        print("1. Solo Project Menu (SPM)")
        print("2. Group Project Menu (GPM)")
        print("3. Back to Main Menu")
        
        type_choice = input("Enter choice: ").strip()

        if type_choice == "1":
            print("\nEntering Solo Project Menu...")
            solo_project_menu(username)
            break
        elif type_choice == "2":
            print("\nEntering Group Project Menu...")
            group_project_menu(username)
            break
        elif type_choice == "3":
            break
        else:
            print("Invalid input. Please try again.")

def solo_project_menu(username):
    while True:
        title_text = f"|  SOLO PROJECT MENU - {username}  |"
        width = len(title_text)
        
        print("\n" + "-" * width)
        print(title_text)
        print("-" * width)
        print("1. View/Manage Solo Projects")
        print("2. Create New Solo Project")
        print("3. Back to main menu")
        
        choice = input("\nEnter choice: ").strip()
        if choice == "1":
            view_solo_project(username) 
        elif choice == "2":
            solo_project_create(username) 
        elif choice == "3":
            break

def solo_project_create(username):
    
    print("\nCreating new solo project..." +"\n")        
    project_name = input("Project Name: ").strip()
    deadline = input("Set Deadline (e.g., YYYY-MM-DD): ").strip()

   #PROJECT STRUCTURE FOR JSON
    new_project = {
        "type": "Solo",
        "name": project_name,
        "deadline": deadline,
        "progress": 0,
        "tasks": [],
        "distractions_logged": 0,
        "status": "In Progress"
    }

    #ADDS PROJECT TO JSON
    if "projects" not in users[username]:
        users[username]["projects"] = []
    
    users[username]["projects"].append(new_project)

    save_data(users)

    print(f"\nProject '{project_name}' has been created!")
    input("Press Enter to return to the Main Menu.")

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
            input("Press Enter to return...")
            break
        
        for i, proj in enumerate(user_projects, 1):
            prog = proj.get("progress", 0)
            deadline_str = proj.get("deadline", "")
            status = "COMPLETED" if prog >= 100 else "IN PROGRESS"
            
            urgency = ""

            print(f"{i}. [{prog}%] {proj['name']} - {status}{urgency}")
            print(f"   Deadline: {deadline_str}")
            print("-" * 20)
        
        print("\n(0) Back")
        choice = input("\nSelect a project number to manage: ").strip()

        if choice == "0":
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(user_projects):
            manage_single_project(username, int(choice) - 1)
        else:
            print("Invalid input.")
        

def view_projects(username):
    while True:
        title_text = f"|  {username.upper()}'S GLOBAL DASHBOARD  |"
        width = len(title_text)
        
        print("\n" + "-" * width)
        print(title_text)
        print("-" * width)
        
        # GATHER SOLO PROJECTS FROM USER DATA
        solo_projects = users[username].get("projects", [])
        
        # GATHER GROUP PROJECTS WHERE USER IS LEADER
        leader_group_projects = users[username].get("group_projects", [])
        
        # GATHER GROUP PROJECTS WHERE USER IS ONLY A MEMBER (SEARCHING ALL USERS)
        member_group_projects = []
        for owner, data in users.items():
            all_groups = data.get("group_projects", [])
            for p in all_groups:
                # CHECK IF USER IS IN THE MEMBER LIST BUT NOT THE LEADER
                if username in p.get("members", []) and p.get("leader") != username:
                    member_group_projects.append(p)

        # COMBINE INTO A MASTER LIST FOR DISPLAY
        # FORMAT: (PROJECT_DICT, TYPE_LABEL, ROLE_LABEL)
        master_list = []
        for p in solo_projects:
            master_list.append((p, "[SOLO]", "SOLO"))
        for p in leader_group_projects:
            master_list.append((p, "[GROUP]", "LEADER"))
        for p in member_group_projects:
            master_list.append((p, "[GROUP]", "MEMBER"))

        if not master_list:
            print("\n[!] No projects found.")
            input("Press Enter to return...")
            break
        
        # DISPLAY LOOP
        for i, (proj, p_type, role) in enumerate(master_list, 1):
            prog = proj.get("progress", 0)
            deadline_str = proj.get("deadline", "")
            
            # STATUS LOGIC
            if prog >= 100:
                status = "COMPLETED"
                urgency = ""
            else:
                status = "IN PROGRESS"
                urgency = ""

                if deadline_str:
                    try:
                        deadline_date = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                        today = datetime.now().date()
                        days_left = (deadline_date - today).days

                        if days_left < 0:
                            urgency = " [!! OVERDUE !!]"
                        elif days_left <= 3:
                            urgency = f" [! DUE IN {days_left} DAYS !]"
                    except ValueError:
                        urgency = " [Invalid Date Format]"

            # FINAL PRINT LINE
            print(f"{i}. {p_type} [{role}] {proj['name']} - {prog}% {status}{urgency}")
            print(f"   Deadline: {deadline_str}")
            print("-" * 30)
        
        print("\n(0) Back to Main Menu")
        choice = input("\nSelect a project number to manage: ").strip()

        if choice == "0":
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(master_list):
            selected_proj, p_type, role = master_list[int(choice) - 1]
            
            # REDIRECT TO CORRECT MANAGER BASED ON TYPE
            if p_type == "[SOLO]":
                # FIND INDEX IN THE ORIGINAL SOLO LIST
                orig_index = solo_projects.index(selected_proj)
                manage_single_project(username, orig_index)
            else:
                # USE GROUP MANAGER FOR BOTH LEADER AND MEMBER ROLES
                manage_group_project(username, selected_proj, f"[{role}]")
        else:
            print("Invalid input. Please try again.")
            
def manage_single_project(username, index):
    project = users[username]["projects"][index]

    while True:
        print("\n" + "-"*30)
        print(f" PROJECT: {project['name']}")
        print(f" Current Progress: {project['progress']}%")
        print(f" Distractions Logged: {project['distractions_logged']}")
        print("-"*30)
        print("1. Update Progress %")
        print("2. Log a Distraction")
        print("3. Mark as Completed")
        print("4. Back")

        choice = input("Choice: ").strip()

        if choice == "1":
            new_val = input("Enter new progress (0-100): ").strip()
            if new_val.isdigit() and 0 <= int(new_val) <= 100:
                project["progress"] = int(new_val)
                save_data(users) 
                print("Progress updated!")
            else:
                print("Please enter a valid number between 0 and 100.")

        elif choice == "2":
            project["distractions_logged"] += 1
            users[username]["total_distractions"] += 1 # Global stat
            save_data(users)
            print("Distraction logged. Stay focused!")

        elif choice == "3":
            project["progress"] = 100
            project["status"] = "Completed"
            save_data(users)
            print("Project Finished! Great job.")
            break

        elif choice == "4":
            break

def group_project_menu(username):
    while True:
        title_text = f"|  GROUP PROJECT MENU - {username}  |"
        width = len(title_text)
        
        print("\n" + "-" * width)
        print(title_text)
        print("-" * width)
        
        print("1. View My Group Projects (Leader & Member)")
        print("2. Create New Group Project (As Leader)")
        print("3. Back to Main Menu")
        
        choice = input("\nEnter choice: ").strip()
        if choice == "1":
            view_group_projects(username)
        elif choice == "2":
            group_project_create(username)
        elif choice == "3":
            break

def view_group_projects(username):
    invites = users[username].get("invites", [])
    if invites:
        print("\n--- Group Project Invitations ---")
        for i, inv in enumerate(invites, 1):
            print(f"{i}. {inv['sender']} invited you to: {inv['project_name']}")
        
        choice = input("\nAccept? (Number) or Skip (Enter): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(invites):
            # MOVE FROM INVITE TO MEMBER LIST
            accepted = invites.pop(int(choice) - 1)
            leader = accepted['sender']
            p_name = accepted['project_name']
            
            # FIND PROJECT IN LEADER'S DATA
            for p in users[leader].get("group_projects", []):
                if p['name'] == p_name:
                    p['members'].append(username)
                    print(f"JOINED {p_name}")
                    break
            save_data(users)
            
    while True:
        title_text = f"|  {username.upper()}'S GROUP PROJECTS  |"
        width = len(title_text)
            
        print("\n" + "-" * width)
        print(title_text)
        print("-" * width)
        
        #FOR PROJECT LEADER
        leader_projs = users[username].get("group_projects", [])
        
        #FOR PROJECT MEMBER
        member_projs = []
        for owner, data in users.items():
            all_groups = data.get("group_projects", [])
            for p in all_groups:
                if username in p["members"] and p["leader"] != username:
                    member_projs.append(p)
        
        #LIST ALL LEADER PROJS FIRST, THEN MEMBER PROJS BELOW
        display_list = []
        for p in leader_projs:
            display_list.append((p, "[LEADER]", username))
        for p in member_projs:
            display_list.append((p, "[MEMBER]", p["leader"]))

        if not display_list:
            print("\n[!] No group projects found.")
            input("Press Enter to return...")
            break
            
        #DISPLAY COMVINED LIST
        for i, (proj, role, owner) in enumerate(display_list, 1):
            prog = proj.get("progress", 0)
            deadline = proj.get("deadline", "No Deadline")
                
    
            status = "COMPLETED" if prog >= 100 else "IN PROGRESS"
                
            #FOR LEADER/MEMBER DISPLAY
            print(f"{i}. {role} {proj['name']} - {prog}% {status}")
            print(f"   Leader: {owner} | Deadline: {deadline}")
            print("-" * 30) 

        print("\n(0) Back")
        choice = input("\nSelect a project to manage: ").strip()

        if choice == "0":
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(display_list):
            selected_proj, role, owner = display_list[int(choice) - 1]
            
            # Pass the data to the manager
            manage_group_project(username, selected_proj, role)
        else:
            print("Invalid selection.")

def group_project_create(username):
    title_text = f"|  CREATE NEW GROUP PROJECT  |"
    width = len(title_text)
    print("\n" + "-" * width)
    print(title_text)
    print("-" * width)
    
    project_name = input("Project Name: ").strip()
    deadline = input("Set Deadline (YYYY-MM-DD): ").strip()
    
    # GET POTENTIAL MEMBERS
    members_input = input("Invite members (comma-separated usernames): ").strip()
    potential = [m.strip() for m in members_input.split(",") if m.strip() and m.strip() != username]
    # INITIALIZE PROJECT OBJECT
    new_project = {
        "type": "Group",
        "name": project_name,
        "deadline": deadline,
        "progress": 0,
        "tasks": [],
        "distractions_logged": 0,
        "status": "In Progress",
        "leader": username,
        "members": [username] # ONLY LEADER IS ACTIVE AT START
    }

    # SEND INVITES TO VALID USERS
    for m in potential:
        if m in users:
            # INITIALIZE INVITE LIST IF MISSING
            if "invites" not in users[m]:
                users[m]["invites"] = []
            
            # ATTACH INVITE DATA
            users[m]["invites"].append({
                "project_name": project_name,
                "sender": username
            })
            print(f"INVITE SENT TO: {m}")
        else:
            print(f"USER '{m}' NOT FOUND - SKIPPED")

    # SAVE TO LEADER'S DATA
    if "group_projects" not in users[username]:
        users[username]["group_projects"] = []
    
    users[username]["group_projects"].append(new_project)
    save_data(users)

    print(f"\nPROJECT '{project_name}' CREATED. INVITES DISPATCHED.")
    input("PRESS ENTER TO RETURN...")

def manage_group_project(username, project, role):
    while True:
        print("\n" + "-"*30)
        print(f" GROUP PROJECT: {project['name']}")
        print(f" Role: {role.strip('[]')}")
        print(f" Current Progress: {project['progress']}%")
        print(f" Distractions Logged: {project['distractions_logged']}")
        print("-"*30)
        
        if role == "[LEADER]":
            print("1. Update Progress %")
            print("2. Log a Distraction")
            print("3. Mark as Completed")
            print("4. Manage Members")
            print("5. Assign Tasks")
            print("6. Back")
            
            choice = input("Choice: ").strip()

            if choice == "1":
                new_val = input("Enter new progress (0-100): ").strip()
                if new_val.isdigit() and 0 <= int(new_val) <= 100:
                    project["progress"] = int(new_val)
                    save_data(users) 
                    print("Progress updated!")
            elif choice == "2":
                project["distractions_logged"] += 1
                for member in project["members"]:
                    users[member]["total_distractions"] = users[member].get("total_distractions", 0) + 1
                save_data(users)
                print("Distraction logged for group!")
            elif choice == "3":
                project["progress"] = 100
                project["status"] = "Completed"
                save_data(users)
                print("Project Finished!")
                break
            elif choice == "4":
                manage_group_members(project)
            elif choice == "5":
                assign_group_task(project)
            elif choice == "6":
                break

        else: # MEMBER OPTIONS (CONFIGURED TO BE LIKE SOLO)
            print("1. Update Progress / Tasks")
            print("2. Log a Distraction")
            print("3. Back")

            choice = input("Choice: ").strip()

            if choice == "1":
                # OPTION 1: UPDATE OVERALL PERCENTAGE
                print(f"\nCurrent Progress: {project['progress']}%")
                new_val = input("Update overall progress (0-100) or press Enter to skip: ").strip()
                if new_val.isdigit() and 0 <= int(new_val) <= 100:
                    project["progress"] = int(new_val)
                    print("Overall progress updated!")
                
                # OPTION 2: UPDATE INDIVIDUAL TASKS
                view_member_tasks(username, project)
                save_data(users)

            elif choice == "2":
                project["distractions_logged"] += 1
                users[username]["total_distractions"] = users[username].get("total_distractions", 0) + 1
                save_data(users)
                print("Distraction logged!")
            elif choice == "3":
                break
    
def manage_group_members(project):
    while True:
        print("\n--- Manage Group Members ---")
        print(f"Current Members: {', '.join(project['members'])}")
        print("1. Add Member")
        print("2. Remove Member")
        print("3. Back")

        choice = input("Choice: ").strip()

        if choice == "1":
            new_member = input("Enter username to add: ").strip()
            if new_member in users and new_member not in project["members"] and new_member != project["leader"]:
                project["members"].append(new_member)
                save_data(users)
                print(f"User '{new_member}' added to the project.")
            else:
                print("Invalid username or user already in the project.")

        elif choice == "2":
            rem_member = input("Enter username to remove: ").strip()
            if rem_member in project["members"]:
                project["members"].remove(rem_member)
                save_data(users)
                print(f"User '{rem_member}' removed from the project.")
            else:
                print("User not found in the project.")

        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def check_invites(username):
    invites = users[username].get("invites", [])
    if not invites:
        return

    # DYNAMIC HEADER
    title_text = f"|  {username.upper()}'S PENDING INVITES  |"
    width = len(title_text)
    print("\n" + "-" * width)
    print(title_text)
    print("-" * width)
    
    for i, inv in enumerate(invites, 1):
        print(f"{i}. {inv['sender']} INVITED YOU TO: {inv['project_name']}")
    
    choice = input("\nAccept invite? (Enter number or 'n' to skip): ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(invites):
        # PROCESS ACCEPTANCE
        accepted = invites.pop(int(choice) - 1)
        leader = accepted['sender']
        p_name = accepted['project_name']
        
        # ADD MEMBER TO LEADER'S PROJECT
        for p in users[leader].get("group_projects", []):
            if p['name'] == p_name:
                if username not in p['members']:
                    p['members'].append(username)
                print(f"Joined {p_name} successfully.")
                break
        save_data(users)

def view_member_tasks(username, project):
    # DYNAMIC HEADER
    title_text = f"|  MY TASKS FOR {project['name'].upper()}  |"
    width = len(title_text)
    print("\n" + "-" * width)
    print(title_text)
    print("-" * width)
    
    # FILTER TASKS ASSIGNED TO CURRENT USER
    my_tasks = [t for t in project.get("tasks", []) if username in t.get("assigned_to", [])]

    if not my_tasks:
        print("No tasks assigned to you yet.")
    else:
        for i, t in enumerate(my_tasks, 1):
            status = "DONE" if t['is_done'] else "PENDING"
            print(f"{i}. [{status}] {t['task_name']}")

        choice = input("\nMark task as done? (Enter number or 'n' to back): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(my_tasks):
            my_tasks[int(choice)-1]['is_done'] = True
            save_data(users)
            print("Task updated.")

def assign_group_task(project):
    print("\n--- ASSIGN NEW TASK ---")
    desc = input("Task Description: ").strip()
    print(f"Available Members: {', '.join(project['members'])}")
    
    target_input = input("Assign to (comma-separated): ").strip()
    targets = [t.strip() for t in target_input.split(",") if t.strip() in project['members']]

    if targets:
        project["tasks"].append({
            "task_name": desc,
            "assigned_to": targets,
            "is_done": False
        })
        save_data(users)
        print(f"Task assigned to {', '.join(targets)}")
    else:
        print("Invalid members selected.")
        
pms = productivity_management_system

#STARTER
if __name__ == "__main__":
    users = load_data()
    pms()