import requests
import random
import string

# --- CONFIGURATION ---
BASE_URL = "http://127.0.0.1:8000/api"

# Helper to generate random users
def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

RANDOM_USER = generate_random_string()
EMAIL = f"{RANDOM_USER}@example.com"
PASSWORD = "complex_password_123"

print(f"🤖 STARTING TEST BOT: User '{RANDOM_USER}'")
print("-" * 50)

# 1. REGISTER USER
print(f"1. Registering user...")
reg_url = f"{BASE_URL}/auth/users/"
reg_data = {
    "username": RANDOM_USER, 
    "email": EMAIL, 
    "password": PASSWORD, 
    "re_password": PASSWORD 
}
response = requests.post(reg_url, json=reg_data)

if response.status_code == 201:
    print("✅ Registration Successful")
else:
    print(f"❌ Registration Failed: {response.text}")
    exit()

# 2. LOGIN (GET TOKEN)
print(f"2. Logging in...")
auth_url = f"{BASE_URL}/auth/jwt/create/"
auth_data = {
    "username": RANDOM_USER, 
    "email": EMAIL, 
    "password": PASSWORD
}
response = requests.post(auth_url, json=auth_data)

if response.status_code == 200:
    TOKEN = response.json().get("access")
    print("✅ Login Successful (Token received)")
else:
    print(f"❌ Login Failed: {response.text}")
    exit()

# HEADERS for future requests
headers = {
    "Authorization": f"JWT {TOKEN}", 
    "Content-Type": "application/json"
}

# 3. CREATE A PROJECT
print(f"3. Creating a Project...")
proj_url = f"{BASE_URL}/projects/"
proj_data = {
    "name": f"Project Nexus by {RANDOM_USER}", 
    "description": "This is an automated test project.",
    "repository_link": "https://github.com/test/repo",
    "live_link": "https://nexus.test",
    "category": "poll" # Added category to be safe
}
response = requests.post(proj_url, json=proj_data, headers=headers)

if response.status_code == 201:
    PROJECT_ID = response.json().get("id")
    print(f"✅ Project Created! ID: {PROJECT_ID}")
else:
    print(f"❌ Project Creation Failed: {response.text}")
    exit()

# 4. VOTE FOR THE PROJECT
print(f"4. Voting for Project {PROJECT_ID}...")
vote_url = f"{BASE_URL}/projects/{PROJECT_ID}/vote/"
response = requests.post(vote_url, headers=headers)

if response.status_code in [200, 201]:
    print("✅ Voted Successfully")
else:
    print(f"❌ Vote Failed: {response.text}")

# 5. COMMENT ON THE PROJECT
print(f"5. Adding a comment...")
comment_url = f"{BASE_URL}/projects/{PROJECT_ID}/comments/"
comment_data = {"content": "This looks like a great project! (Automated Comment)"} 
response = requests.post(comment_url, json=comment_data, headers=headers)

if response.status_code == 201:
    print("✅ Comment Added")
else:
    print(f"❌ Comment Failed: {response.text}")

# 6. VERIFY RESULTS
print(f"6. Verifying Data...")
verify_url = f"{BASE_URL}/projects/{PROJECT_ID}/"
response = requests.get(verify_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    # 🔥 FIX: Read 'vote_count' (Integer) instead of 'votes' (List)
    vote_count = data.get('vote_count', 0)
    
    print(f"\n--- REPORT ---")
    print(f"Project: {data.get('name')}")
    print(f"Current Votes: {vote_count}")
    print("-" * 50)

    if vote_count == 1:
        print("🎉 SUCCESS: Vote count updated correctly!")
    else:
        print(f"⚠️ WARNING: Expected 1 vote, but got {vote_count}")

    print("\nDEBUG - Full Response:", data)
else:
    print(f"❌ Verification Failed: {response.text}")