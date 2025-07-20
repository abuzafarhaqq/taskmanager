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
touch taskmanager.py config.py
```
- now for the next task


python package
```python
# Core  
Flask-SQLAlchemy  # Database ORM  
Flask-Migrate     # DB migrations (Alembic wrapper)  
Flask-Login       # User session/auth  
Flask-CORS        # API security (if frontend is separate)  
python-dateutil   # Timezone handling  

# Security  
bcrypt            # Password hashing  
Flask-Talisman    # HTTPS/security headers  
Flask-Limiter     # Rate limiting (prevent brute-force)  

# API/Dev  
Flask-RESTX       # Swagger docs + API scaffolding  
Flask-SocketIO    # Real-time sync (optional)  
pytest-flask      # Testing framework  

class Task(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(80), nullable=False)  
    deadline = db.Column(db.DateTime(timezone=True))  
    # Use `python-dateutil` for TZ conversions  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  
    status = db.Column(db.Enum('todo', 'in_progress', 'done'))  

# password hashing
from bcrypt import hashpw, gensalt  
hashed_pw = hashpw(user_password.encode(), gensalt())  

# rate limiting
from flask_limiter import Limiter  
limiter = Limiter(app, key_func=get_remote_address)  
@app.route("/api/tasks")  
@limiter.limit("10/minute")  
def get_tasks(): ...  

# frontend decoupling, kill flaskwtf/jinja2: use react/vue.js for dynamic UI
# Flask-RESTX for API
from flask_restx import Api, Resource  
api = Api(app)  
@api.route('/tasks')  
class TaskList(Resource):  
    def get(self):  
        return {'tasks': [task.serialize() for task in Task.query.all()]}  
```

```bash
# Run this in your project root directory:  Launch the PostgreSQL Docker container
docker run -d --name taskmanager-db -p 5432:5432 -e POSTGRES_USER=taskadmin -e POSTGRES_PASSWORD=taskAdminPass123! -e POSTGRES_DB=taskmanager -v pgdata:/var/lib/postgresql/data postgres:15-alpine

# Verify:  
docker ps -a | grep taskmanager-db  
```

```bash
# First database Migration and Database Creation
# Initialize migrations (run once):  
flask db init

# Generate migration script:  
flask db migrate -m "Initial tables: User, Task"

# Apply to PostgreSQL:  
flask db upgrade

# Verify in PostgreSQL:
docker exec -it taskmanager-db psql -U taskadmin -d taskmanager
taskmanager=# \dt
taskmanager=# \q
```

# Docker Compose Commands:
```bash
# for building use up --build, to remove use down
docker-compose up --build
docker-compose down
```

# Install Flask-Login: `pip install flask-login` and `pip freeze > requirements.txt`

- Now we're creating for user login, registration, logout functions.
- In `forms.py` we've an email validator function in the registration form comes from `email-validator` package.
- Install `email-validator` package: `pip install email-validator` and `pip freeze > requirements.txt`




