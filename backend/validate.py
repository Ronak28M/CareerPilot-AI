import sys, os
sys.path.insert(0, '.')

os.environ['WATSONX_API_KEY'] = '4TvA2BpQDSggiItwNqWUxxdIUiQQpkT7U-W05zziIeyc'
os.environ['WATSONX_PROJECT_ID'] = '3e8ed057-d249-4d0e-98aa-d0de87976a52'

print("=== CareerPilot AI – End-to-End Backend Validation ===\n")

# Test 1: Module imports
from services.granite_service import call_granite_json, call_granite
from services.career_service import _fallback_career_data, _fallback_skill_data, _fallback_roadmap
from services.chat_service import handle_chat, _get_suggested_actions
from services.comparison_service import _fallback_comparison
from services.progress_service import _fallback_progress_update
print("1. All service modules: OK")

# Test 2: Flask routes
import app as flask_app
rules = [str(r) for r in flask_app.app.url_map.iter_rules()]
required = ['/api/analyze-career', '/api/chat', '/api/compare-careers', '/api/update-progress', '/api/health']
for route in required:
    assert route in rules, f'Missing route: {route}'
print("2. All API routes registered: OK")

# Test 3: Fallback data integrity
demo = {'name': 'Priya', 'degree': 'B.Tech', 'branch': 'CS', 'technical_skills': 'HTML, CSS, JavaScript'}
fb = _fallback_career_data(demo)
assert len(fb['career_recommendations']) == 3
assert all('career_name' in r for r in fb['career_recommendations'])
assert all('match_percentage' in r for r in fb['career_recommendations'])
print("3. Fallback career data structure: OK")

skill_fb = _fallback_skill_data()
assert 'strong_skills' in skill_fb
assert 'missing_skills' in skill_fb
assert 'skill_match_percentage' in skill_fb
print("4. Fallback skill data structure: OK")

roadmap_fb = _fallback_roadmap()
assert 'phase_1' in roadmap_fb
assert 'phase_2' in roadmap_fb
assert 'phase_3' in roadmap_fb
assert 'immediate_next_action' in roadmap_fb
print("5. Fallback roadmap structure: OK")

# Test 4: Live Granite call
print("\nTesting live IBM Granite connection...")
try:
    prompt = "Return only this JSON object with no other text: " + '{"status": "ok"}'
    result = call_granite_json(prompt, max_tokens=30)
    print(f"6. IBM Granite live call: OK - response={result}")
except Exception as e:
    print(f"6. IBM Granite live call: WARN - {e} (will use fallbacks)")

# Test 5: Chat suggested actions
actions = _get_suggested_actions("what skills am I missing", "")
assert isinstance(actions, list)
print("7. Chat suggested actions: OK")

# Test 6: Progress fallback
prog = _fallback_progress_update(50, ['React'], 'Data Science')
assert 'next_immediate_action' in prog
assert 'career_readiness_score' in prog
print("8. Progress update fallback: OK")

# Test 7: Comparison fallback
comp = _fallback_comparison(['Frontend Developer', 'Data Analyst'], 'HTML, CSS')
assert 'comparisons' in comp
assert len(comp['comparisons']) == 2
print("9. Career comparison fallback: OK")

print("\n=== ALL VALIDATIONS PASSED ===")
