from .ping import router as ping_router
from .tasks import router as tasks_router
from .user import router as user_router
from .auth import router as auth_router

routers = [ping_router, tasks_router, user_router, auth_router]