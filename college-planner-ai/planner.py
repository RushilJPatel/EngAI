import json
import os
from typing import List, Dict, Set

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Warning: Google Generative AI library not installed. Install with: pip install google-generativeai")


def load_courses() -> Dict:
    """Load course data from courses.json"""
    with open('courses.json', 'r') as f:
        return json.load(f)


def suggest_next_courses(completed: List[str], all_courses: List[str]) -> List[Dict]:
    """
    Suggest next courses based on completed courses and prerequisites.
    
    Args:
        completed: List of completed course names
        all_courses: List of all available courses at the college
        
    Returns:
        List of dictionaries with course info, prioritized by level
    """
    courses_data = load_courses()['courses']
    completed_set = set(completed)
    
    # Find courses that can be taken next
    available_courses = []
    
    for course_name in all_courses:
        if course_name in courses_data and course_name not in completed_set:
            course_info = courses_data[course_name]
            prerequisites = course_info.get('prerequisites', [])
            
            # Check if all prerequisites are met
            if all(prereq in completed_set for prereq in prerequisites):
                available_courses.append({
                    'name': course_name,
                    'level': course_info.get('level', 'unknown'),
                    'credits': course_info.get('credits', 3),
                    'description': course_info.get('description', ''),
                    'prerequisites': prerequisites
                })
    
    # Sort by level priority (freshman -> sophomore -> junior -> senior)
    level_order = {'freshman': 1, 'sophomore': 2, 'junior': 3, 'senior': 4, 'unknown': 5}
    available_courses.sort(key=lambda x: level_order.get(x['level'], 5))
    
    return available_courses


def suggest_ai_electives(interests: str) -> List[Dict]:
    """
    Suggest electives based on user interests using keyword matching.
    
    Args:
        interests: Comma-separated string of interests
        
    Returns:
        List of dictionaries with elective suggestions and match reasons
    """
    courses_data = load_courses()['courses']
    interest_keywords = [interest.strip().lower() for interest in interests.split(',') if interest.strip()]
    
    suggestions = []
    
    for course_name, course_info in courses_data.items():
        course_tags = course_info.get('tags', [])
        
        # Check for keyword matches
        matches = []
        for keyword in interest_keywords:
            # Direct tag match
            if keyword in [tag.lower() for tag in course_tags]:
                matches.append(f"matches '{keyword}' tag")
            
            # Course name contains keyword
            elif keyword in course_name.lower():
                matches.append(f"course name contains '{keyword}'")
            
            # Description contains keyword
            elif keyword in course_info.get('description', '').lower():
                matches.append(f"description contains '{keyword}'")
        
        if matches:
            suggestions.append({
                'name': course_name,
                'level': course_info.get('level', 'unknown'),
                'credits': course_info.get('credits', 3),
                'description': course_info.get('description', ''),
                'matches': matches,
                'match_count': len(matches)
            })
    
    # Sort by number of matches (most relevant first)
    suggestions.sort(key=lambda x: x['match_count'], reverse=True)
    
    return suggestions


def get_course_info(course_name: str) -> Dict:
    """Get detailed information about a specific course"""
    courses_data = load_courses()['courses']
    return courses_data.get(course_name, {})


def get_all_course_names() -> List[str]:
    """Get list of all available course names"""
    courses_data = load_courses()['courses']
    return list(courses_data.keys())


def generate_semester_schedule(completed: List[str], all_courses: List[str], career_path: str = None, interests: str = "", semesters: int = 8) -> List[Dict]:
    """
    Generate a multi-semester schedule based on completed courses, career path, and interests.
    
    Args:
        completed: List of completed course names
        all_courses: List of all available courses at the college
        career_path: Desired career path (affects course prioritization)
        interests: Comma-separated interests
        semesters: Number of semesters to plan (default 8 for 4 years)
        
    Returns:
        List of dictionaries representing each semester's courses
    """
    courses_data = load_courses()['courses']
    career_paths = load_courses().get('career_paths', {})
    
    # Get prioritized courses for career path
    career_priorities = []
    if career_path and career_path.lower() in career_paths:
        career_priorities = career_paths[career_path.lower()]
    
    # Get interest-based electives
    elective_suggestions = suggest_ai_electives(interests)
    interest_electives = {e['name']: e for e in elective_suggestions}
    
    # Track what's been planned
    completed_set = set(completed)
    planned_courses = set(completed)
    semester_schedules = []
    
    # Generate semester-by-semester plan
    for semester in range(1, semesters + 1):
        # Determine academic year
        year = ((semester - 1) // 2) + 1
        term = "Fall" if (semester - 1) % 2 == 0 else "Spring"
        
        # Get available courses for this semester
        available = []
        
        for course_name in all_courses:
            if course_name in completed_set or course_name in planned_courses:
                continue
                
            if course_name not in courses_data:
                continue
                
            course_info = courses_data[course_name]
            prerequisites = course_info.get('prerequisites', [])
            
            # Check if all prerequisites are met
            if all(prereq in planned_courses for prereq in prerequisites):
                # Calculate priority score
                priority = 0
                
                # Career path match gets highest priority
                if course_name in career_priorities:
                    priority += 1000 - career_priorities.index(course_name)
                
                # Interest match
                if course_name in interest_electives:
                    priority += interest_electives[course_name]['match_count'] * 50
                
                # Level appropriateness (prefer courses that fit the semester)
                level = course_info.get('level', 'unknown')
                level_order = {'freshman': 1, 'sophomore': 2, 'junior': 3, 'senior': 4}
                target_level = 'freshman' if year == 1 else ('sophomore' if year == 2 else ('junior' if year == 3 else 'senior'))
                if level == target_level:
                    priority += 200
                
                available.append({
                    'name': course_name,
                    'level': course_info.get('level', 'unknown'),
                    'credits': course_info.get('credits', 3),
                    'description': course_info.get('description', ''),
                    'priority': priority,
                    'tags': course_info.get('tags', []),
                    'career_relevant': course_name in career_priorities if career_path else False
                })
        
        # Sort by priority and select top courses (12-15 credits per semester is typical)
        available.sort(key=lambda x: x['priority'], reverse=True)
        
        # Select courses for this semester (aim for 12-15 credits)
        semester_courses = []
        total_credits = 0
        
        # Prioritize core/prerequisite courses first
        for course in available:
            if total_credits + course['credits'] <= 18:  # Max 18 credits
                semester_courses.append({
                    'name': course['name'],
                    'credits': course['credits'],
                    'description': course['description'],
                    'career_relevant': course.get('career_relevant', False),
                    'tags': course.get('tags', [])
                })
                planned_courses.add(course['name'])
                total_credits += course['credits']
            
            if total_credits >= 12:  # Minimum full-time
                break
        
        semester_schedules.append({
            'semester': semester,
            'year': year,
            'term': term,
            'courses': semester_courses,
            'total_credits': total_credits,
            'available_courses_count': len(available)
        })
    
    return semester_schedules


def get_career_paths() -> Dict:
    """Get available career paths"""
    return load_courses().get('career_paths', {})


def analyze_workload(semester_courses: List[str]) -> Dict:
    """
    Analyze the workload for a given semester using AI.
    
    Args:
        semester_courses: List of course names for a semester
        
    Returns:
        Dictionary with workload analysis
    """
    if not GEMINI_AVAILABLE:
        return analyze_workload_basic(semester_courses)
    
    try:
        # Configure Gemini API
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        courses_data = load_courses()['courses']
        course_descriptions = []
        total_credits = 0
        
        for course_name in semester_courses:
            if course_name in courses_data:
                info = courses_data[course_name]
                total_credits += info.get('credits', 3)
                course_descriptions.append(f"- {course_name} ({info.get('level', 'unknown')}): {info.get('description', '')}")
        
        prompt = f"""Analyze the workload for this computer science semester schedule and provide a brief, actionable analysis in JSON format.

Courses:
{chr(10).join(course_descriptions)}
Total Credits: {total_credits}

Return a JSON object with these exact keys: difficulty_rating (1-10 integer), weekly_hours (string), challenges (string), tips (string), balance_analysis (string)."""

        response = model.generate_content(prompt)
        
        # Parse the response
        content = response.text.strip()
        # Try to extract JSON if it's wrapped in code blocks
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            content = content.split('```')[1].strip()
        
        analysis = json.loads(content)
        analysis['total_credits'] = total_credits
        analysis['method'] = 'AI (Gemini)'
        return analysis
        
    except Exception as e:
        print(f"AI analysis failed: {e}")
        return analyze_workload_basic(semester_courses)


def analyze_workload_basic(semester_courses: List[str]) -> Dict:
    """Fallback workload analysis without AI"""
    courses_data = load_courses()['courses']
    total_credits = 0
    difficult_courses = ['Algorithms', 'Operating Systems', 'Machine Learning', 'Artificial Intelligence']
    moderate_courses = ['Data Structures', 'Database Systems', 'Computer Networks']
    
    difficulty_count = 0
    credit_count = 0
    
    for course_name in semester_courses:
        if course_name in courses_data:
            info = courses_data[course_name]
            credits = info.get('credits', 3)
            credit_count += credits
            
            if course_name in difficult_courses:
                difficulty_count += 2
            elif course_name in moderate_courses:
                difficulty_count += 1
    
    # Simple difficulty estimation
    if credit_count >= 15:
        difficulty = 8
        weekly_hours = "25-30 hours"
    elif credit_count >= 12:
        difficulty = 6 + (difficulty_count * 0.5)
        weekly_hours = "20-25 hours"
    else:
        difficulty = 5
        weekly_hours = "15-20 hours"
    
    return {
        'difficulty_rating': min(10, int(difficulty)),
        'weekly_hours': weekly_hours,
        'challenges': 'Multiple challenging courses may overlap. Prioritize time management.',
        'tips': 'Start assignments early and maintain consistent study schedule.',
        'balance_analysis': f"Managing {credit_count} credit hours. Balance varies based on course difficulty.",
        'total_credits': credit_count,
        'method': 'Basic'
    }


def get_ai_schedule_guidance(current_semester: Dict, completed: List[str], career_path: str, interests: str, remaining_semesters: int) -> str:
    """
    Get AI guidance for improving the current semester schedule.
    
    Args:
        current_semester: Current semester schedule
        completed: Completed courses
        career_path: Career aspiration
        interests: User interests
        remaining_semesters: Number of remaining semesters
        
    Returns:
        AI-generated guidance string
    """
    if not GEMINI_AVAILABLE:
        return ""
    
    try:
        # Configure Gemini API
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        courses_data = load_courses()['courses']
        semester_courses = [c['name'] for c in current_semester['courses']]
        course_info = []
        
        for course in semester_courses:
            if course in courses_data:
                info = courses_data[course]
                course_info.append(f"{course} ({info.get('level', 'unknown')}): {info.get('description', '')}")
        
        prompt = f"""As an academic advisor, provide brief, actionable guidance for this CS student:

Career Goal: {career_path if career_path else 'General CS'}
Interests: {interests if interests else 'None specified'}
Completed Courses: {', '.join(completed) if completed else 'None yet'}
Remaining Semesters: {remaining_semesters}

Current Semester Courses:
{chr(10).join(course_info)}

Provide 2-3 specific, actionable recommendations to optimize their learning and career preparation. Keep it under 100 words."""

        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        print(f"AI guidance failed: {e}")
        return ""
