### SIMPLE TASK MANAGER
---

**Problem Statement**:
Nure is a super busy guy who struggles to keep track of his daily tasks. He often forgets important things and needs a simple, lightweight Task Manager App that will help him add, view, and manage his tasks efficiently.

**Requirements**:
Build a Flask-based API where Nure can:
1. Add new tasks that he needs to complete.
2. View a list of all tasks to stay organized.
3. Mark tasks as completed when done.
4. Delete tasks that are no longer needed.

**Deployment Expectations**:
- The application must be containerized using Docker so Nure can easily run it on any system.
- Use Docker Compose to define the application setup.
- Deploy the **Dockerized application on AWS** using **an EC2 instance**.

**Steps to Follow (Guideline for Students)**:
1. **Setup a Python Flask Application** with basic routes for managing tasks.
2. **Use MySQL Database** to store tasks.
3. **Write a Dockerfile** to containerize the Flask application.
4. **Create a docker-compose.yml file** if needed for better orchestration.
5. **Test the Docker Container** locally before deployment.
6. **Deploy it to AWS**.
 
Create a video of your project and submit the Video link in the Discord group. Please explain how it works.
Note: This project is not optional, it is a must to pass your exam.

**Working procedure**:
- Create working directory: `mkdir task-manager-for-bongodev`
- Initialize git: `git init .` and create a **README.md** and **.gitignore** file for working procedure `touch README.md .gitignore`
- Create a virtual environment: `python3 -m venv vTaskManager` and activate it: `source vTaskManager/bin/activate`
- added `Flask`, `mysql-connector-python`, `python-dotenv` to `requiremets.txt` file.
- Now, install the packages: `pip install -r requirements.txt` and add packages to the file: `pip freeze > requirements.txt`
- Now create some directories and files:
```bash
mkdir -p taskmanager/app/{static,templates}
touch taskmanager/{docker-compose.yml,Dockerfile,init.sql}
touch taskmanager/app/{__init__.py,app.py,routes.py}
touch taskmanager/app/static/style.css taskmanager/app/templates/index.html
```
- now for the next task

