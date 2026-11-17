from src.app import activities


def test_get_activities_returns_all_activities(client):
    activity_names = set(activities)

    response = client.get("/activities")

    assert response.status_code == 200
    assert set(response.json()) == activity_names


def test_root_redirects_to_index_page(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_signup_adds_student_to_activity(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Gym Class/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Gym Class"}
    assert email in activities["Gym Class"]["participants"]


def test_signup_to_unknown_activity_returns_404(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Unknown Club/signup", params={"email": email})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_rejects_duplicate_registration(client):
    email = "michael@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 400
    assert activities["Chess Club"]["participants"].count(email) == 1


def test_unregister_removes_student_from_activity(client):
    email = "daniel@mergington.edu"

    response = client.delete("/activities/Chess Club/unregister", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_student_not_signed_up_returns_404(client):
    email = "nobody@mergington.edu"

    response = client.delete("/activities/Chess Club/unregister", params={"email": email})

    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}


def test_unregister_from_unknown_activity_returns_404(client):
    email = "daniel@mergington.edu"

    response = client.delete("/activities/Unknown Club/unregister", params={"email": email})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
