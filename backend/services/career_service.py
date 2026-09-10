"""
Career analysis service – builds prompts and calls Granite for career analysis.
"""

import json
import logging
from services.granite_service import call_granite_json

logger = logging.getLogger(__name__)


def build_career_analysis_prompt(profile: dict) -> str:
    return f"""You are CareerPilot AI, a holistic career counselor for college students across ALL industries and domains.

CRITICAL RULES:
1. Do NOT default to technology or software careers unless the student explicitly wants them.
2. Base recommendations primarily on the student's INTERESTS, PASSIONS, SOFT SKILLS, FAVORITE SUBJECTS, and CAREER GOALS.
3. Technical/coding skills are only ONE factor among many — a student who loves writing, people, business, arts, healthcare, law, environment etc. should get recommendations in THOSE domains.
4. Consider ALL career domains: Technology, Business & Management, Finance & Accounting, Marketing & Sales, HR, Design & Creative, Media & Journalism, Education & Teaching, Psychology & Counseling, Law & Legal, Healthcare & Life Sciences, Science & Research, Government & Public Administration, Social Work & Nonprofit, Hospitality & Tourism, Fashion & Lifestyle, Environment & Sustainability, Architecture & Planning, Public Relations & Communication, Entrepreneurship.
5. A student who says "I dislike coding" or whose interests are in arts/people/business must NEVER receive software engineering as a recommendation.

Student Profile:
- Name: {profile.get('name', '')}
- Degree: {profile.get('degree', '')}
- Branch / Specialization: {profile.get('branch', '')}
- Year: {profile.get('year', '')}
- CGPA: {profile.get('cgpa', '')}
- Skills (technical and otherwise): {profile.get('technical_skills', '')}
- Soft Skills & Strengths: {profile.get('soft_skills', '')}
- Interests & Passions: {profile.get('interests', '')}
- Favourite Subjects: {profile.get('favorite_subjects', '')}
- Hobbies: {profile.get('hobbies', '')}
- Career Goals (MOST IMPORTANT): {profile.get('career_goals', '')}
- Preferred Domain / Industry: {profile.get('preferred_domain', '')}
- Preferred Industry: {profile.get('preferred_industry', '')}
- Short-term Goal: {profile.get('short_term_goal', '')}
- Long-term Goal: {profile.get('long_term_goal', '')}
- Projects & Work: {profile.get('projects', '')}
- Certifications: {profile.get('certifications', '')}
- Internships: {profile.get('internships', '')}
- Learning Hours/Day: {profile.get('learning_hours', '')}
- Learning Style: {profile.get('learning_style', '')}

Analyse the FULL profile holistically. The top recommendations must match the student's stated interests and goals, not just their existing technical skills.

Return ONLY this exact JSON structure (no markdown):
{{
  "career_recommendations": [
    {{
      "career_name": "",
      "career_domain": "",
      "match_percentage": 85,
      "why_it_matches": "",
      "existing_skills": [],
      "missing_skills": [],
      "skills_to_learn": [],
      "job_roles": [],
      "recommended_projects": [],
      "recommended_certifications": [],
      "next_steps": []
    }}
  ],
  "current_skills": [],
  "skill_gaps": [],
  "priority_skills": [],
  "job_roles": [],
  "projects": [],
  "certifications": [],
  "next_action": ""
}}

Provide exactly 3 career recommendations ranked by match_percentage descending. career_domain is the broad industry (e.g. "Business & Management", "Healthcare", "Design & Creative")."""


def build_skill_gap_prompt(profile: dict, target_career: str) -> str:
    return f"""You are a career skills analyst. Analyse a student's skills for their target career — which may be in ANY domain (technology, business, healthcare, law, design, media, education, etc.).

Student's Current Skills & Strengths: {profile.get('technical_skills', '')}
Soft Skills: {profile.get('soft_skills', '')}
Interests: {profile.get('interests', '')}
Target Career: {target_career}
Degree: {profile.get('degree', '')} in {profile.get('branch', '')}

List skills relevant to "{target_career}" — these could be domain-specific tools, knowledge areas, certifications, communication skills, analytical abilities, creative skills, etc. Do NOT restrict to coding/programming unless the career requires it.

Return ONLY a valid JSON object:
{{
  "strong_skills": [{{"name": "", "proficiency": 70, "relevance": ""}}],
  "beginner_skills": [{{"name": "", "proficiency": 30, "action": ""}}],
  "missing_skills": [{{"name": "", "importance": "critical", "learning_time": "4 weeks"}}],
  "priority_skills": [],
  "skill_match_percentage": 65,
  "analysis_summary": ""
}}

proficiency is 0-100, importance is critical/high/medium. Skills must be appropriate for the specific career domain."""


def build_roadmap_prompt(profile: dict, target_career: str, skill_gaps: list) -> str:
    gaps_str = ", ".join(skill_gaps) if skill_gaps else "key domain-specific skills"
    return f"""You are an expert career roadmap planner for students across ALL industries and domains.

Student: {profile.get('name', 'Student')}
Target Career: {target_career}
Current Skills & Strengths: {profile.get('technical_skills', '')}
Soft Skills: {profile.get('soft_skills', '')}
Interests: {profile.get('interests', '')}
Skills & Knowledge to Develop: {gaps_str}
Learning Hours/Day: {profile.get('learning_hours', '2')}
Degree: {profile.get('degree', '')} in {profile.get('branch', '')}
Goals: {profile.get('career_goals', '')}

Create a realistic 12-month roadmap for "{target_career}" based on {profile.get('learning_hours', '2')} hours/day.
The roadmap must be domain-appropriate — if this is a business, creative, healthcare, or non-technical career, the skills, topics, projects and certifications must reflect THAT domain specifically, not generic coding tasks.
Return ONLY a valid JSON object:
{{
  "phase_1": {{
    "duration": "0-3 months",
    "focus": "",
    "skills_to_learn": [],
    "topics": [],
    "practice_activities": [],
    "projects": [],
    "certifications": [],
    "expected_outcome": "",
    "weekly_plan": ""
  }},
  "phase_2": {{
    "duration": "3-6 months",
    "focus": "",
    "skills_to_learn": [],
    "topics": [],
    "practice_activities": [],
    "projects": [],
    "certifications": [],
    "expected_outcome": "",
    "weekly_plan": ""
  }},
  "phase_3": {{
    "duration": "6-12 months",
    "focus": "",
    "skills_to_learn": [],
    "topics": [],
    "practice_activities": [],
    "projects": [],
    "certifications": [],
    "expected_outcome": "",
    "weekly_plan": ""
  }},
  "total_duration": "12 months",
  "immediate_next_action": ""
}}"""


def analyze_career(profile: dict) -> dict:
    """
    Full career analysis pipeline: recommendations + skill gaps + roadmap.

    Args:
        profile: Student profile dictionary.

    Returns:
        Complete analysis result dict.
    """
    # Step 1: Career recommendations
    logger.info(f"Analyzing career for: {profile.get('name', 'student')}")
    career_prompt = build_career_analysis_prompt(profile)
    career_data = call_granite_json(
        career_prompt,
        max_tokens=2500,
        system_prompt="You are CareerPilot AI, an expert career counselor. Always respond with valid JSON only. No markdown, no explanation text outside the JSON."
    )

    if "error" in career_data and "career_recommendations" not in career_data:
        logger.error(f"Career analysis failed: {career_data.get('error')}")
        career_data = _fallback_career_data(profile)

    # Step 2: Skill gap analysis for top recommended career
    top_career = "Professional in your chosen field"
    if career_data.get("career_recommendations"):
        top_career = career_data["career_recommendations"][0].get("career_name", "Software Developer")

    skill_prompt = build_skill_gap_prompt(profile, top_career)
    skill_data = call_granite_json(
        skill_prompt,
        max_tokens=1500,
        system_prompt="You are a technical skills analyst. Always respond with valid JSON only. No markdown, no explanation."
    )

    if "error" in skill_data and "strong_skills" not in skill_data:
        skill_data = _fallback_skill_data(top_career)

    # Step 3: Roadmap
    missing_skills = [s.get("name", "") for s in skill_data.get("missing_skills", [])]
    roadmap_prompt = build_roadmap_prompt(profile, top_career, missing_skills)
    roadmap_data = call_granite_json(
        roadmap_prompt,
        max_tokens=3000,
        system_prompt="You are an expert career roadmap planner. Always respond with valid JSON only. No markdown, no explanation."
    )

    if "error" in roadmap_data and "phase_1" not in roadmap_data:
        roadmap_data = _fallback_roadmap(top_career)

    return {
        "career_recommendations": career_data.get("career_recommendations", []),
        "match_scores": {
            rec.get("career_name", f"Career {i+1}"): rec.get("match_percentage", 0)
            for i, rec in enumerate(career_data.get("career_recommendations", []))
        },
        "current_skills": career_data.get("current_skills", []),
        "skill_gaps": career_data.get("skill_gaps", []),
        "priority_skills": career_data.get("priority_skills", []),
        "job_roles": career_data.get("job_roles", []),
        "projects": career_data.get("projects", []),
        "certifications": career_data.get("certifications", []),
        "next_action": career_data.get("next_action", ""),
        "skill_analysis": skill_data,
        "roadmap": roadmap_data,
        "top_career": top_career,
    }


# ---------------------------------------------------------------------------
# Fallback data when Granite is unavailable
# ---------------------------------------------------------------------------

# Domain keyword maps for smarter fallback detection
_DOMAIN_KEYWORDS = {
    "business": ["business", "management", "entrepreneur", "startup", "mba", "commerce"],
    "finance": ["finance", "accounting", "banking", "investment", "ca", "cfa", "economics"],
    "marketing": ["marketing", "sales", "brand", "advertising", "digital marketing", "seo"],
    "hr": ["human resource", "hr ", "people", "recruitment", "talent"],
    "design": ["design", "creative", "art", "illustration", "fashion", "visual"],
    "media": ["media", "journalism", "content", "writing", "film", "broadcast", "blogging"],
    "education": ["teaching", "education", "trainer", "professor", "tutor"],
    "psychology": ["psychology", "counseling", "mental health", "therapy", "social work"],
    "law": ["law", "legal", "advocate", "attorney", "judiciary", "policy"],
    "healthcare": ["healthcare", "medicine", "doctor", "nurse", "pharma", "biotech", "health"],
    "science": ["research", "science", "biology", "chemistry", "physics", "lab"],
    "environment": ["environment", "sustainability", "climate", "ecology", "green"],
    "hospitality": ["hospitality", "tourism", "hotel", "travel", "event management"],
    "government": ["government", "civil service", "ias", "upsc", "public administration"],
    "tech": ["software", "developer", "coding", "programming", "data science", "machine learning", "ai", "cloud"],
}

_DOMAIN_FALLBACKS = {
    "business": {
        "recs": [
            ("Business Development Manager", 82, "Business & Management",
             "Strong interest in entrepreneurship and management aligns with business development.",
             ["Communication", "Analytical thinking"], ["CRM tools", "Financial modelling", "Negotiation"],
             ["Business Development Executive", "Sales Manager", "Growth Strategist"],
             ["Market research report", "Business pitch deck", "Go-to-market plan"],
             ["Google Project Management", "HubSpot Sales Certification"]),
            ("Marketing Manager", 74, "Marketing & Sales",
             "Creative and strategic interests suit a marketing leadership role.",
             ["Communication", "Creativity"], ["SEO/SEM", "Analytics tools", "Campaign planning"],
             ["Digital Marketing Specialist", "Brand Manager", "Content Strategist"],
             ["Social media campaign", "Brand audit report"], ["Google Digital Marketing", "Meta Blueprint"]),
            ("Entrepreneur / Startup Founder", 70, "Entrepreneurship",
             "Entrepreneurial mindset and drive to build something new.",
             ["Ideation", "Communication"], ["Business planning", "Fundraising", "Product management"],
             ["Startup Founder", "Product Manager", "Business Consultant"],
             ["Mini startup MVP", "Business plan competition"],
             ["Startup India certification", "Y Combinator resources"]),
        ],
        "skills": ["Communication", "Business analysis", "CRM knowledge"],
        "gaps": ["Financial modelling", "CRM tools", "Data analysis"],
        "action": "Enroll in a business fundamentals course and shadow a local business or startup.",
    },
    "design": {
        "recs": [
            ("UI/UX Designer", 85, "Design & Creative",
             "Creative interests and attention to visual detail are a strong match for UX design.",
             ["Creativity", "Visual thinking"], ["Figma", "User research", "Prototyping"],
             ["UX Designer", "Product Designer", "Interaction Designer"],
             ["App redesign case study", "User research report"], ["Google UX Design Certificate", "Interaction Design Foundation"]),
            ("Graphic Designer", 75, "Design & Creative",
             "Artistic interest and creativity suit graphic design work.",
             ["Creativity", "Aesthetics"], ["Adobe Illustrator", "Photoshop", "Typography"],
             ["Graphic Designer", "Visual Designer", "Brand Identity Designer"],
             ["Logo design portfolio", "Brand identity project"], ["Adobe Certified Professional"]),
            ("Content Creator / Digital Media", 68, "Media & Journalism",
             "Creative storytelling and digital interests fit content creation.",
             ["Creativity", "Communication"], ["Video editing", "Social media tools", "Copywriting"],
             ["Content Creator", "Social Media Manager", "Digital Marketer"],
             ["YouTube channel", "Instagram portfolio"], ["HubSpot Content Marketing"]),
        ],
        "skills": ["Creativity", "Visual thinking", "Adobe basics"],
        "gaps": ["Figma", "User research", "Brand strategy"],
        "action": "Start learning Figma for free and complete a UI redesign challenge this week.",
    },
    "media": {
        "recs": [
            ("Content Writer / Journalist", 83, "Media & Journalism",
             "Strong interest in writing and storytelling suits journalism and content creation.",
             ["Writing", "Research", "Communication"], ["SEO writing", "AP style", "Video tools"],
             ["Content Writer", "Journalist", "Copywriter"],
             ["Personal blog", "News article portfolio"], ["HubSpot Content Marketing", "Google News Initiative"]),
            ("Digital Marketing Specialist", 74, "Marketing & Sales",
             "Media savvy and communication skills align with digital marketing.",
             ["Communication", "Creativity"], ["SEO", "Analytics", "Paid ads"],
             ["Digital Marketing Analyst", "Social Media Manager", "SEO Specialist"],
             ["Campaign report", "SEO audit"], ["Google Digital Marketing Certificate"]),
            ("PR & Communications Manager", 68, "Public Relations",
             "Interpersonal skills and writing ability suit public relations.",
             ["Communication", "Writing"], ["Media relations", "Crisis communication", "Press releases"],
             ["PR Executive", "Communications Manager", "Brand Spokesperson"],
             ["Press release portfolio", "PR campaign plan"], ["PRSA Foundation courses"]),
        ],
        "skills": ["Writing", "Communication", "Research"],
        "gaps": ["SEO tools", "Video editing", "Media relations"],
        "action": "Start a blog or write 3 sample articles in your area of interest this month.",
    },
    "healthcare": {
        "recs": [
            ("Healthcare Administrator", 80, "Healthcare & Life Sciences",
             "Interest in healthcare combined with management potential suits hospital/clinic administration.",
             ["Empathy", "Organisation"], ["Healthcare systems", "Medical terminology", "MS Excel"],
             ["Hospital Administrator", "Healthcare Manager", "Clinic Coordinator"],
             ["Healthcare process improvement report", "Patient journey map"],
             ["Coursera Health Management", "ACHE certification"]),
            ("Public Health Analyst", 72, "Healthcare & Life Sciences",
             "Interest in social impact and health aligns with public health work.",
             ["Research", "Analytical thinking"], ["Epidemiology basics", "Data tools", "Policy analysis"],
             ["Public Health Officer", "Health Policy Analyst", "NGO Health Researcher"],
             ["Community health survey", "Policy brief"], ["Johns Hopkins Public Health (Coursera)"]),
            ("Health & Wellness Coach", 65, "Psychology & Counseling",
             "Empathy and interest in wellbeing suit a coaching or counseling career.",
             ["Empathy", "Communication"], ["Coaching techniques", "Nutrition basics", "Psychology basics"],
             ["Wellness Coach", "Life Coach", "Health Educator"],
             ["Wellness program design", "Client case study"], ["ICF Coaching certification"]),
        ],
        "skills": ["Empathy", "Organisation", "Research"],
        "gaps": ["Healthcare systems", "Medical terminology", "Policy analysis"],
        "action": "Volunteer at a clinic or NGO to gain hands-on healthcare exposure.",
    },
    "tech": {
        "recs": [
            ("Software Developer", 82, "Technology & IT",
             "Programming skills and technology interests are well aligned with software development.",
             ["Logical thinking", "Problem solving"], ["Advanced frameworks", "Testing", "System design"],
             ["Junior Developer", "Full Stack Developer", "Backend Engineer"],
             ["Portfolio web app", "Open source contribution"], ["Meta Developer Certificate", "AWS Certified Developer"]),
            ("Data Analyst", 74, "Technology & IT",
             "Analytical mindset and interest in data suit a data analytics role.",
             ["Analytical thinking", "Python basics"], ["SQL", "Pandas", "Tableau"],
             ["Data Analyst", "Business Intelligence Analyst", "Reporting Analyst"],
             ["Sales data dashboard", "EDA project"], ["Google Data Analytics", "IBM Data Analyst Certificate"]),
            ("Product Manager", 68, "Business & Management",
             "Technical understanding combined with strategic thinking suits product management.",
             ["Problem solving", "Communication"], ["Product roadmapping", "Agile", "User research"],
             ["Associate Product Manager", "Product Analyst", "Business Analyst"],
             ["Product spec document", "Competitive analysis"], ["Google PM Certificate", "Pragmatic Institute"]),
        ],
        "skills": ["Programming", "Logical thinking", "Problem solving"],
        "gaps": ["Advanced frameworks", "System design", "SQL"],
        "action": "Build one complete project end-to-end and deploy it on GitHub Pages or Vercel.",
    },
}
_DOMAIN_FALLBACKS["finance"] = {
    "recs": [
        ("Financial Analyst", 83, "Finance & Accounting",
         "Interest in finance and numbers aligns with financial analysis.",
         ["Numerical aptitude", "Analytical thinking"], ["Excel/financial modelling", "Accounting basics", "CFA concepts"],
         ["Financial Analyst", "Investment Analyst", "Budget Analyst"],
         ["Stock analysis report", "Personal finance model"], ["CFA Level 1", "Corporate Finance (Coursera)"]),
        ("Chartered Accountant / CPA", 76, "Finance & Accounting",
         "Strong academic background and interest in finance suit CA/CPA.",
         ["Numerical aptitude", "Attention to detail"], ["Taxation", "Audit", "Financial reporting"],
         ["Chartered Accountant", "Tax Consultant", "Audit Associate"],
         ["Tax return simulation", "Financial statement analysis"], ["ICAI CA Foundation", "ACCA"]),
        ("Management Consultant", 68, "Business & Management",
         "Problem-solving and strategic thinking suit consulting.",
         ["Analytical thinking", "Communication"], ["Case analysis", "PowerPoint", "Business strategy"],
         ["Business Analyst", "Strategy Consultant", "Operations Analyst"],
         ["Business case study", "Market entry analysis"], ["McKinsey Problem Solving (online)", "BCG Insights"]),
    ],
    "skills": ["Numerical aptitude", "Analytical thinking", "MS Excel"],
    "gaps": ["Financial modelling", "Accounting software", "CFA knowledge"],
    "action": "Begin a free Corporate Finance course on Coursera and practice financial modelling in Excel.",
}
_DOMAIN_FALLBACKS["education"] = {
    "recs": [
        ("Teacher / Educator", 84, "Education & Teaching",
         "Passion for sharing knowledge and strong communication skills suit teaching.",
         ["Communication", "Patience", "Subject knowledge"], ["Pedagogy", "Curriculum design", "Classroom management"],
         ["School Teacher", "Corporate Trainer", "Online Educator"],
         ["Lesson plan portfolio", "Tutorial video series"], ["B.Ed", "CTET", "Coursera Learning How to Learn"]),
        ("Instructional Designer", 74, "Education & Teaching",
         "Creativity and interest in education align with designing learning experiences.",
         ["Creativity", "Communication"], ["eLearning tools", "Articulate Storyline", "LMS platforms"],
         ["Instructional Designer", "eLearning Developer", "L&D Specialist"],
         ["eLearning module", "Training needs analysis"], ["ATD Instructional Design certificate"]),
        ("EdTech Product Manager", 65, "Business & Management",
         "Interest in education combined with technology awareness suits EdTech PM roles.",
         ["Communication", "Analytical thinking"], ["Product strategy", "User research", "Agile basics"],
         ["Product Manager – EdTech", "Business Analyst", "Growth Manager"],
         ["Product roadmap for an EdTech app", "User interview report"],
         ["Google PM Certificate", "Product School free courses"]),
    ],
    "skills": ["Communication", "Subject knowledge", "Patience"],
    "gaps": ["Pedagogy", "Curriculum design", "LMS tools"],
    "action": "Start creating a mini online course or tutorial series on a subject you love.",
}


def _detect_domain(profile: dict) -> str:
    """Detect the most relevant domain from interests, career goals, and preferred domain."""
    text = " ".join([
        profile.get("interests", ""),
        profile.get("career_goals", ""),
        profile.get("preferred_domain", ""),
        profile.get("preferred_industry", ""),
        profile.get("favorite_subjects", ""),
        profile.get("hobbies", ""),
        profile.get("long_term_goal", ""),
    ]).lower()

    scores = {domain: 0 for domain in _DOMAIN_KEYWORDS}
    for domain, keywords in _DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[domain] += 1

    best = max(scores, key=lambda d: scores[d])
    return best if scores[best] > 0 else "tech"


def _fallback_career_data(profile: dict) -> dict:
    domain = _detect_domain(profile)
    fb = _DOMAIN_FALLBACKS.get(domain, _DOMAIN_FALLBACKS["tech"])
    name = profile.get("name", "Student")
    skills_raw = profile.get("technical_skills", "")
    existing_list = [s.strip() for s in skills_raw.split(",") if s.strip()][:3]

    recs = []
    for r in fb["recs"]:
        career_name, pct, career_domain, why, existing, missing, roles, projects, certs = r
        recs.append({
            "career_name": career_name,
            "career_domain": career_domain,
            "match_percentage": pct,
            "why_it_matches": why,
            "existing_skills": existing_list or existing,
            "missing_skills": missing,
            "skills_to_learn": missing,
            "job_roles": roles,
            "recommended_projects": projects,
            "recommended_certifications": certs,
            "next_steps": [f"Research the {career_name} role", f"Build a beginner {career_name} project", "Connect with professionals in this field"],
        })

    return {
        "career_recommendations": recs,
        "current_skills": existing_list or fb["skills"],
        "skill_gaps": fb["gaps"],
        "priority_skills": fb["gaps"][:3],
        "job_roles": recs[0]["job_roles"] if recs else [],
        "projects": recs[0]["recommended_projects"] if recs else [],
        "certifications": recs[0]["recommended_certifications"] if recs else [],
        "next_action": fb["action"],
    }


def _fallback_skill_data(career: str = "") -> dict:
    """Generic skill fallback — returns placeholder data indicating Granite should be retried."""
    return {
        "strong_skills": [
            {"name": "Communication", "proficiency": 65, "relevance": "Essential in any career"},
            {"name": "Analytical thinking", "proficiency": 55, "relevance": "Problem solving across domains"},
        ],
        "beginner_skills": [
            {"name": "Domain-specific tools", "proficiency": 30, "action": f"Research tools commonly used in {career or 'your target career'}"},
            {"name": "Industry knowledge", "proficiency": 25, "action": "Read industry publications and follow professionals in the field"},
        ],
        "missing_skills": [
            {"name": f"Core {career or 'career'} skills", "importance": "critical", "learning_time": "4-8 weeks"},
            {"name": "Professional certification", "importance": "high", "learning_time": "2-3 months"},
            {"name": "Practical experience / projects", "importance": "high", "learning_time": "Ongoing"},
        ],
        "priority_skills": [f"{career or 'Career'} fundamentals", "Practical projects", "Networking"],
        "skill_match_percentage": 40,
        "analysis_summary": f"You're at an early stage for {career or 'this career'}. Focus on building domain-specific skills and real-world experience.",
    }


def _fallback_roadmap(career: str = "") -> dict:
    label = career or "your target career"
    return {
        "phase_1": {
            "duration": "0-3 months",
            "focus": f"Build foundational knowledge for {label}",
            "skills_to_learn": [f"{label} fundamentals", "Industry tools introduction", "Professional basics"],
            "topics": ["Core concepts overview", "Industry terminology", "Key frameworks or methods"],
            "practice_activities": ["Daily reading/learning in your domain", "Shadow or informational interviews"],
            "projects": [f"Introductory {label} project", "Personal portfolio or case study"],
            "certifications": ["Beginner certification in your domain"],
            "expected_outcome": f"Strong foundational understanding of {label}",
            "weekly_plan": "2 hours/day: 1hr learning + 1hr practice/project",
        },
        "phase_2": {
            "duration": "3-6 months",
            "focus": f"Develop intermediate skills and build domain portfolio",
            "skills_to_learn": ["Intermediate domain tools", "Professional communication", "Domain-specific analysis"],
            "topics": ["Advanced concepts", "Case studies in your field", "Real-world applications"],
            "practice_activities": ["Work on a real project or internship", "Join a relevant community or club"],
            "projects": [f"Intermediate {label} portfolio project", "Collaborative or team project"],
            "certifications": ["Intermediate professional certification"],
            "expected_outcome": f"Capable of entry-level {label} work",
            "weekly_plan": "2 hours/day: split between skill building and project work",
        },
        "phase_3": {
            "duration": "6-12 months",
            "focus": "Job readiness, networking and advanced application",
            "skills_to_learn": ["Advanced domain skills", "Leadership & soft skills", "Interview & job search skills"],
            "topics": ["Industry trends", "Strategic thinking", "Professional development"],
            "practice_activities": ["Mock interviews", "Networking events", "Apply for internships or entry roles"],
            "projects": ["Capstone / showcase project", "Contribution to industry community"],
            "certifications": ["Advanced or recognised industry certification"],
            "expected_outcome": f"Job-ready for {label} positions",
            "weekly_plan": "2 hours/day: job prep + portfolio polishing + networking",
        },
        "total_duration": "12 months",
        "immediate_next_action": f"Spend this week researching the top 3 entry-level job descriptions for {label} and identify the skills they all require.",
    }
