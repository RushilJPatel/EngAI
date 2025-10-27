from flask import Flask, render_template, request, jsonify
import json
from planner import suggest_next_courses, suggest_ai_electives, get_course_info, generate_semester_schedule, get_career_paths, analyze_workload, get_ai_schedule_guidance

app = Flask(__name__)


def load_colleges():
    """Load college data from college_curriculums.json"""
    with open('college_curriculums.json', 'r') as f:
        return json.load(f)


@app.route('/')
def index():
    """Render the main page with college dropdown"""
    colleges_data = load_colleges()
    colleges = [(key, colleges_data['colleges'][key]['name']) for key in colleges_data['colleges'].keys()]
    career_paths = get_career_paths()
    return render_template('index.html', colleges=colleges, career_paths=list(career_paths.keys()))


@app.route('/get_courses', methods=['POST'])
def get_courses():
    """Return course list for selected college"""
    college_key = request.json.get('college')
    colleges_data = load_colleges()
    
    if college_key in colleges_data['colleges']:
        college_courses = colleges_data['colleges'][college_key]['courses']
        return jsonify({'courses': college_courses})
    else:
        return jsonify({'error': 'College not found'}), 400


@app.route('/recommend', methods=['POST'])
def recommend():
    """Process completed courses and interests, return recommendations"""
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


@app.route('/generate_schedule', methods=['POST'])
def generate_schedule():
    """Generate a semester-by-semester schedule"""
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


@app.route('/course_info/<course_name>')
def course_info(course_name):
    """Get detailed information about a specific course"""
    try:
        info = get_course_info(course_name)
        if info:
            return jsonify(info)
        else:
            return jsonify({'error': 'Course not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# For Vercel deployment, don't run the development server
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

# This allows Vercel to import the app
application = app
