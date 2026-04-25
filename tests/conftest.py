from fastapi import FastAPI, HTTPException

app = FastAPI()

activities = []

@app.get("/activities")
async def get_activities():
    return activities

@app.post("/signup")
async def signup(data: dict):
    email = data.get("email")
    activity = data.get("activity")
    key = f"{email}:{activity}"

    if key in activities:
        raise HTTPException(status_code=400, detail="Duplicate signup")
    activities.append(key)
    return {"message": "Signed up"}

@app.post("/unregister")
async def unregister(data: dict):
    email = data.get("email")
    activity = data.get("activity")
    key = f"{email}:{activity}"

    if key not in activities:
        raise HTTPException(status_code=404, detail="Not found")
    activities.remove(key)
    return {"message": "Unregistered"}
