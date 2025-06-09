"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate student is not already signed up
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    if "@" not in email or "." not in email:
        raise HTTPException(status_code=400, detail="Invalid email format")
    if any(email in activity["participants"] for activity in activities.values()):
        raise HTTPException(status_code=400, detail="Student already signed up for an activity")
    # Validate activity name format
    if not activity_name.isalnum() or len(activity_name) < 3:
        raise HTTPException(status_code=400, detail="Invalid activity name format")
    if not activity_name.replace(" ", "").isalnum():
        raise HTTPException(status_code=400, detail="Activity name must be alphanumeric")
    # Validate activity has not reached max participants
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    if len(activities[activity_name]["participants"]) >= activities[activity_name]["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity has reached maximum participants")
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
