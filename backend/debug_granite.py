import sys, os
sys.path.insert(0, '.')
os.environ['WATSONX_API_KEY'] = '4TvA2BpQDSggiItwNqWUxxdIUiQQpkT7U-W05zziIeyc'
os.environ['WATSONX_PROJECT_ID'] = '3e8ed057-d249-4d0e-98aa-d0de87976a52'

from services.granite_service import call_granite

# Use a very short, direct prompt
prompt = """Analyze this student and return ONLY a JSON object, nothing else.
Student: Priya, B.Tech CS, skills: HTML CSS JavaScript Python
Return this exact structure:
{"top_career": "Frontend Developer", "match": 85, "skills_to_learn": ["React", "TypeScript"]}"""

raw = call_granite(prompt, max_tokens=200)
print("RAW RESPONSE:")
print(repr(raw))
print()
print("FIRST 500 CHARS:")
print(raw[:500])
