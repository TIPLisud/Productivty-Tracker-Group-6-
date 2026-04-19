from datetime import datetime

class Project:
    def __init__(self, name, work_hours, deadline):
        self.name = name
        self.work_hours = work_hours
        self.deadline = deadline
        self.progress = 0  # progress percentage

    def update_progress(self, progress):
        if 0 <= progress <= 100:
            self.progress = progress
            print(f"Progress updated to {self.progress}%")
        else:
            print("Invalid progress. Enter a value between 0 and 100.")

    def display_project(self):
        print("\n" + "Project Details".center(40))
        print(f"Project Name: {self.name}")
        print(f"Work Time (hours): {self.work_hours}")
        print(f"Deadline: {self.deadline.strftime('%m-%d-%Y')}")
        print(f"Progress: {self.progress}%")
        print("---------------------\n")


class ProjectManager:
    def __init__(self):
        self.projects = []

    def add_project(self):
        name = input("Enter Project name: ")
        work_hours = float(input("Enter work time (in hours): "))
        
        date_input = input("Set Deadline (MM-DD-YYYY): ")
        deadline = datetime.strptime(date_input, "%m-%d-%Y")
        
        project = Project(name, work_hours, deadline) 
        self.projects.append(project)
        print("Task added successfully!")

    def show_projects(self):
        if not self.projects:
            print("No projects available.")
            return
        
        for i, project in enumerate(self.projects):
            print(f"\nProject #{i+1}")
            project.display_project()

    def update_project_progress(self):
        self.show_projects()
        if not self.projects:
            return
        
        choice = int(input("Select project number to update: ")) - 1
        if 0 <= choice < len(self.projects):
            progress = int(input("Enter progress (0-100): "))
            self.projects[choice].update_progress(progress)
        else:
            print("Invalid choice.")


# Tracker Menu
def main():
    manager = ProjectManager()

    while True:
        print("\n" + "Progress Tracker Menu".center(40))
        print("1. Add Project")
        print("2. Show Projects")
        print("3. Update Progress")
        print("4. Exit")

        choice = input("Enter option: ")

        if choice == "1":
            manager.add_project()
        elif choice == "2":
            manager.show_projects()
        elif choice == "3":
            manager.update_project_progress()
        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()


