from flask import Flask, render_template, request, jsonify
import json
import os
import sys

# Get the parent directory to import modules and access files
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import the planner module
from planner import (
    suggest_next_courses,
    suggest_ai_electives,
    get_course_info,
    generate_semester_schedule,
    get_career_paths,
    analyze_workload,
    get_ai_schedule_guidance
)

# Create Flask app
app = Flask(__name__)

# Set template and static folders
app.template_folder = os.path.join(parent_dir, 'templates')
app.static_folder = os.path.join(parent_dir, 'static')


def load_colleges():
    """Load college data"""
    json_path = os.path.join(parent_dir, 'college_curriculums.json')
    with open(json_path, 'r') as f:
        return json.load(f)


@app.route('/')
def index():
    """Main page"""
    colleges_data = load_colleges()
    colleges = [(key, colleges_data['colleges'][key]['name']) 
                for key in colleges_data['colleges'].keys()]
    career_paths = get_career_paths()
    return render_template('index.html', 
                         colleges=colleges, 
                         career_paths=list(career_paths.keys()))


@app.route('/get_courses', methods=['POST'])
def get_courses():
    """Get course list for selected college"""
    college_key = request.json.get('college')
    colleges_data = load_colleges()
    
    if college_key in colleges_data['colleges']:
        return jsonify({'courses': colleges_data['colleges'][college_key]['courses']})
    else:
        return jsonify({'error': 'College not found'}), 400


@app.route('/recommend', methods=['POST'])
def recommend():
    """Get course recommendations"""
    try:
        data = request.json
        college_key = data.get('college')
        completed_courses = data.get('completed_courses', [])
        interests = data.get('interests', '')
        
        colleges_data = load_colleges()
        if college_key not in colleges_data['colleges']:
            return jsonify({'error': 'College not found'}), 400
        
        college_courses = colleges_data['colleges'][college_key]['courses']
        next_courses = suggest_next_courses(completed_courses, college_courses)
        elective_suggestions = suggest_ai_electives(interests)
        
        available_electives = [e for e in elective_suggestions 
                              if e['name'] in college_courses]
        
        return jsonify({
            'next_courses': next_courses,
            'elective_suggestions': available_electives[:5],
            'college_name': colleges_data['colleges'][college_key]['name']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate_schedule', methods=['POST'])
def generate_schedule():
    """Generate semester schedule"""
    try:
        data = request.json
        college_key = data.get('college')
        completed_courses = data.get('completed_courses', [])
        career_path = data.get('career_path', '')
        interests = data.get('interests', '')
        num_semesters = data.get('semesters', 8)
        
        colleges_data = load_colleges()
        if college_key not in colleges_data['colleges']:
            return jsonify({'error': 'College not found'}), 400
        
        college_courses = colleges_data['colleges'][college_key]['courses']
        schedule = generate_semester_schedule(
            completed=completed_courses,
            all_courses=college_courses,
            career_path=career_path,
            interests=interests,
            semesters=num_semesters
        )
        
        enhanced_schedule = []
        for idx, semester in enumerate(schedule):
            semester_course_names = [c['name'] for c in semester['courses']]
            workload_analysis = analyze_workload(semester_course_names)
            remaining_sems = num_semesters - idx - 1
            ai_guidance = get_ai_schedule_guidance(
                current_semester=semester,
                completed=completed_courses,
                career_path=career_path,
                interests=interests,
                remaining_semesters=remaining_sems
            )
            
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


@app.route('/course_info/<course_name>')
def course_info(course_name):
    """Get course information"""
    try:
        info = get_course_info(course_name)
        if info:
            return jsonify(info)
        else:
            return jsonify({'error': 'Course not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# This is what Vercel needs
app = app
