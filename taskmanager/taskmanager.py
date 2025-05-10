import sqlalchemy as sa
import sqlalchemy.orm as so
from app import taskmanager, db
from app.models import User, Task


@taskmanager.shell_context_processor
def shell_context_processor():
    print(f"db: {db}\n user: {User}\n task: {Task}")
    return {"sa": sa, "so": so, "db": db, "user": User, "task": Task}
