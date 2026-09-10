import sys, os
sys.path.insert(0, '.')
os.environ['WATSONX_API_KEY'] = '4TvA2BpQDSggiItwNqWUxxdIUiQQpkT7U-W05zziIeyc'
os.environ['WATSONX_PROJECT_ID'] = '3e8ed057-d249-4d0e-98aa-d0de87976a52'

from services.career_service import analyze_career
import json

print("Running full career analysis with IBM Granite...")
print("Student: Priya Sharma (B.Tech CS, Year 2)\n")

demo = {
    "name": "Priya Sharma",
    "degree": "B.Tech",
    "branch": "Computer Science",
    "year": "2nd Year",
    "cgpa": "7.8",
    "technical_skills": "HTML, CSS, JavaScript (Basic), Python (Beginner), UI/UX Basics",
    "soft_skills": "Communication, Teamwork, Creativity",
    "interests": "Web Design, Data Visualization, User Experience",
    "favorite_subjects": "Web Technologies, Design Thinking",
    "career_goals": "Become a Frontend Developer or Data Analyst",
    "preferred_domain": "Frontend Development, Data Analytics, UI/UX",
    "short_term_goal": "Build portfolio with 3 projects",
    "long_term_goal": "Senior developer at a product company",
    "projects": "Personal blog (HTML/CSS), Python calculator",
    "certifications": "HTML/CSS Basics (freeCodeCamp)",
    "internships": "None",
    "learning_hours": "2",
    "learning_style": "Visual",
}

result = analyze_career(demo)

print("TOP CAREER RECOMMENDATIONS:")
for rec in result.get("career_recommendations", []):
    print(f"  {rec.get('career_name')} - {rec.get('match_percentage')}% match")

print(f"\nSKILL MATCH: {result.get('skill_analysis', {}).get('skill_match_percentage', 'N/A')}%")
print(f"\nROADMAP PHASE 1 FOCUS: {result.get('roadmap', {}).get('phase_1', {}).get('focus', 'N/A')}")
print(f"\nNEXT ACTION: {result.get('next_action', 'N/A')}")
print("\n=== LIVE GRANITE TEST COMPLETE ===")
