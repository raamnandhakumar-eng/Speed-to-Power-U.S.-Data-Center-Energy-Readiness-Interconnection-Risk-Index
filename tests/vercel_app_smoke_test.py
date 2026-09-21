from app import app

assert app.title == "Speed-to-Power"
paths = {route.path for route in app.routes}

assert "/" in paths
assert "/api/health" in paths
assert "/api/v1" in paths
assert "/api/v2" in paths
assert "/api/v3" in paths
assert "/api/v4" in paths

print("Vercel FastAPI entrypoint check passed.")
