import requests
import random
import string
import json

BASE_URL = "http://127.0.0.1:8000/api"

# --- HELPER FUNCTIONS ---
def get_random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def register_and_login(tag):
    username = f"user_{tag}_{get_random_string()}"
    email = f"{username}@example.com"
    password = "TestPassword_123!" 
    
    # 1. Register
    reg_url = f"{BASE_URL}/auth/users/"
    requests.post(reg_url, json={
        "username": username, "email": email, "password": password, "re_password": password
    })
    
    # 2. Login
    login_url = f"{BASE_URL}/auth/jwt/create/"
    response = requests.post(login_url, json={
        "username": username, "email": email, "password": password
    })
    
    if response.status_code == 200:
        token = response.json()["access"]
        print(f"✅ User '{tag}' created & logged in.")
        return token, {"Authorization": f"JWT {token}", "Content-Type": "application/json"}
    else:
        print(f"❌ Failed to login User {tag}: {response.text}")
        exit()

def create_project(headers, name):
    data = {
        "name": name,
        "description": "Sorting test project",
        "category": "poll"
    }
    response = requests.post(f"{BASE_URL}/projects/", json=data, headers=headers)
    if response.status_code != 201:
        print(f"❌ Failed to create project '{name}': {response.text}")
        exit()
    return response.json()["id"]

def vote(headers, project_id):
    requests.post(f"{BASE_URL}/projects/{project_id}/vote/", headers=headers)

# --- MAIN TEST ---
print("🤖 STARTING SORTING TEST (DEBUG MODE)")
print("-" * 50)

# 1. Setup 3 Users
token_a, headers_a = register_and_login("A")
token_b, headers_b = register_and_login("B")
token_c, headers_c = register_and_login("C")

# 2. Setup 3 Projects
print("\n🏗️  Creating 3 Projects...")
id_high = create_project(headers_a, "Project HIGH (3 Votes)")
id_mid  = create_project(headers_a, "Project MID (1 Vote)")
id_low  = create_project(headers_a, "Project LOW (0 Votes)")

# 3. Cast Votes
print("🗳️  Rigging the votes...")
vote(headers_a, id_high)
vote(headers_b, id_high)
vote(headers_c, id_high)
vote(headers_a, id_mid)
print("✅ Votes cast.")

# 4. Fetch Sorted List
print("\n🔍 Requesting sorted list (ordering=-vote_count)...")
sort_url = f"{BASE_URL}/projects/?ordering=-vote_count"
response = requests.get(sort_url, headers=headers_a)

# --- DEBUGGING SECTION ---
print(f"DEBUG: Status Code: {response.status_code}")
if response.status_code != 200:
    print(f"❌ ERROR RESPONSE: {response.text}")
    exit()
# -------------------------

results = response.json()
projects = results.get("results", results) if isinstance(results, dict) else results

# 5. Verify Order
print("\n--- LEADERBOARD REPORT ---")

# Filter only our test projects
relevant_projects = []
try:
    relevant_projects = [p for p in projects if p['id'] in [id_high, id_mid, id_low]]
except TypeError as e:
    print(f"❌ CRASH: Could not process list. Raw data: {projects}")
    exit()

for i, project in enumerate(relevant_projects):
    print(f"{i+1}. {project['name']} (Votes: {project['vote_count']})")

if len(relevant_projects) < 3:
    print("\n⚠️ WARNING: Could not find all 3 test projects.")
else:
    p1, p2, p3 = relevant_projects[0], relevant_projects[1], relevant_projects[2]
    if p1['id'] == id_high and p2['id'] == id_mid and p3['id'] == id_low:
        print("\n🎉 TEST PASSED: Leaderboard is sorted correctly!")
    else:
        print("\n❌ TEST FAILED: Sorting order is wrong.")

