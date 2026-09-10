import sys, os, json, requests
sys.path.insert(0, '.')
os.environ['WATSONX_API_KEY'] = '4TvA2BpQDSggiItwNqWUxxdIUiQQpkT7U-W05zziIeyc'
os.environ['WATSONX_PROJECT_ID'] = '3e8ed057-d249-4d0e-98aa-d0de87976a52'

def get_token():
    resp = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data="grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=4TvA2BpQDSggiItwNqWUxxdIUiQQpkT7U-W05zziIeyc",
        timeout=30,
    )
    return resp.json()["access_token"]

token = get_token()
print("IAM token obtained:", token[:20], "...")

# Try with chat format (messages) - granite-4 likely uses chat API
url_chat = "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"
url_gen  = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# Test 1: Generation API
print("\n--- Test 1: text/generation ---")
payload1 = {
    "model_id": "ibm/granite-4-h-small",
    "project_id": "3e8ed057-d249-4d0e-98aa-d0de87976a52",
    "input": "Say hello in one sentence.",
    "parameters": {"max_new_tokens": 50}
}
r1 = requests.post(url_gen, headers=headers, json=payload1, timeout=30)
print("Status:", r1.status_code)
print("Body:", r1.text[:500])

# Test 2: Chat API
print("\n--- Test 2: text/chat ---")
payload2 = {
    "model_id": "ibm/granite-4-h-small",
    "project_id": "3e8ed057-d249-4d0e-98aa-d0de87976a52",
    "messages": [{"role": "user", "content": "Say hello in one sentence."}],
    "parameters": {"max_tokens": 50}
}
r2 = requests.post(url_chat, headers=headers, json=payload2, timeout=30)
print("Status:", r2.status_code)
print("Body:", r2.text[:500])
