"""
Vercel Python Serverless Function for College Planner AI
This file needs to be in the api/ directory for Vercel to recognize it
"""
import json
import os
import sys
import traceback
import logging

# Add parent directory to path so we can import planner
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from flask import Flask, render_template, request, jsonify
try:
    from flask_cors import CORS
except Exception:
    CORS = None

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try importing project-specific modules but don't let import errors crash the function at import-time.
startup_error = None
try:
    from planner import (
        suggest_next_courses,
        suggest_ai_electives,
        get_course_info,
        generate_semester_schedule,
        get_career_paths,
        analyze_workload,
        get_ai_schedule_guidance,
    )
    logger.info("Imported planner module successfully")
except Exception:
    startup_error = traceback.format_exc()
    logger.exception("Failed to import planner or dependencies at startup")

# Create Flask app with correct paths
app = Flask(__name__, 
           template_folder=os.path.join(parent_dir, 'templates'),
           static_folder=os.path.join(parent_dir, 'static'))

# Enable CORS for the API so a static site (served from Live Server) can call it
if CORS is not None:
    CORS(app)
else:
    # If flask_cors isn't installed, set CORS headers in responses as a fallback
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

def load_colleges():
    """Load college data from college_curriculums.json"""
    json_path = os.path.join(parent_dir, 'college_curriculums.json')
    with open(json_path, 'r') as f:
        return json.load(f)


@app.route('/', methods=['GET'])
def index():
    """Optional server-rendered index for environments that use Flask to serve the site.
    When deployed with static hosting + serverless APIs, the static `static/index.html`
    will be served instead.
    """
    if startup_error:
        # Application reachable but backend failed to start properly
        return jsonify({'error': 'startup_error', 'details': startup_error}), 500
    colleges_data = load_colleges()
    colleges = [(key, colleges_data['colleges'][key]['name']) for key in colleges_data['colleges'].keys()]
    career_paths = get_career_paths()
    try:
        return render_template('index.html', colleges=colleges, career_paths=list(career_paths.keys()))
    except Exception:
        # If templates are not desired (static-first deployment), return a short message
        return jsonify({'status': 'ok', 'message': 'Flask app running. Use static/index.html for the frontend.'})


@app.route('/api/get_courses', methods=['POST'])
def get_courses():
    """Return course list for selected college"""
    if startup_error:
        return jsonify({'error': 'startup_error', 'details': startup_error}), 500
    college_key = request.json.get('college')
    colleges_data = load_colleges()
    
    if college_key in colleges_data['colleges']:
        college_courses = colleges_data['colleges'][college_key]['courses']
        return jsonify({'courses': college_courses})
    else:
        return jsonify({'error': 'College not found'}), 400


@app.route('/api/recommend', methods=['POST'])
def recommend():
    """Process completed courses and interests, return recommendations"""
    if startup_error:
        return jsonify({'error': 'startup_error', 'details': startup_error}), 500
    try:
        data = request.json
        college_key = data.get('college')
        completed_courses = data.get('completed_courses', [])
        interests = data.get('interests', '')
        
        # Get college courses
        colleges_data = load_colleges()
        if college_key not in colleges_data['colleges']:
            return jsonify({'error': 'College not found'}), 400
        
        college_courses = colleges_data['colleges'][college_key]['courses']
        
        # Get course recommendations
        next_courses = suggest_next_courses(completed_courses, college_courses)
        
        # Get elective suggestions
        elective_suggestions = suggest_ai_electives(interests)
        
        # Filter electives to only include courses available at this college
        available_electives = [elective for elective in elective_suggestions 
                             if elective['name'] in college_courses]
        
        return jsonify({
            'next_courses': next_courses,
            'elective_suggestions': available_electives[:5],  # Limit to top 5
            'college_name': colleges_data['colleges'][college_key]['name']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/generate_schedule', methods=['POST'])
def generate_schedule():
    """Generate a semester-by-semester schedule"""
    if startup_error:
        return jsonify({'error': 'startup_error', 'details': startup_error}), 500
    try:
        data = request.json
        college_key = data.get('college')
        completed_courses = data.get('completed_courses', [])
        career_path = data.get('career_path', '')
        interests = data.get('interests', '')
        num_semesters = data.get('semesters', 8)
        
        # Get college courses
        colleges_data = load_colleges()
        if college_key not in colleges_data['colleges']:
            return jsonify({'error': 'College not found'}), 400
        
        college_courses = colleges_data['colleges'][college_key]['courses']
        
        # Generate semester schedule
        schedule = generate_semester_schedule(
            completed=completed_courses,
            all_courses=college_courses,
            career_path=career_path,
            interests=interests,
            semesters=num_semesters
        )
        
        # Add AI-powered workload analysis and guidance to each semester
        enhanced_schedule = []
        for idx, semester in enumerate(schedule):
            semester_course_names = [c['name'] for c in semester['courses']]
            
            # Analyze workload using AI
            workload_analysis = analyze_workload(semester_course_names)
            
            # Get AI guidance for this semester
            remaining_sems = num_semesters - idx - 1
            ai_guidance = get_ai_schedule_guidance(
                current_semester=semester,
                completed=completed_courses,
                career_path=career_path,
                interests=interests,
                remaining_semesters=remaining_sems
            )
            
            # Add analyses to semester data
            semester['workload_analysis'] = workload_analysis
            semester['ai_guidance'] = ai_guidance if ai_guidance else ""
            
            enhanced_schedule.append(semester)
        
        return jsonify({
            'schedule': enhanced_schedule,
            'college_name': colleges_data['colleges'][college_key]['name'],
            'career_path': career_path
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/course_info/<course_name>')
def course_info(course_name):
    """Get detailed information about a specific course"""
    if startup_error:
        return jsonify({'error': 'startup_error', 'details': startup_error}), 500
    try:
        info = get_course_info(course_name)
        if info:
            return jsonify(info)
        else:
            return jsonify({'error': 'Course not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Lightweight health endpoint for Vercel / debugging (under /api/ so routing works with /api/*)
@app.route('/api/_health', methods=['GET'])
def _health():
    """Simple health check returning 200 so we can verify the function is reachable."""
    return jsonify({'status': 'ok'}), 200


# Endpoint to list colleges + career paths for static frontend initialization
@app.route('/api/colleges', methods=['GET'])
def api_colleges():
    try:
        colleges_data = load_colleges()
        career_paths = get_career_paths()
        # Return a simplified mapping of college_key -> name
        colleges_simple = {k: v['name'] for k, v in colleges_data['colleges'].items()}
        return jsonify({'colleges': colleges_simple, 'career_paths': list(career_paths.keys())})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Vercel expects this variable name to be exported
# This is the WSGI application object that Vercel will serve
application = app
