from app.api.routers.auth import auth_router
from app.api.routers.geometry import geometry_router

ROUTERS = [geometry_router, auth_router]
