from app import taskmanager


@taskmanager.route("/")
@taskmanager.route("/index")
def index():
    return "Hello, World!"
