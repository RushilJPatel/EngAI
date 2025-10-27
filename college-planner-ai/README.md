# College Planner AI MVP

A Flask-based web application that helps computer science students plan their degree efficiently by providing personalized course recommendations and elective suggestions based on prerequisites and interests.

## Features

- **College Selection**: Choose from 10 top-tier CS universities (MIT, Stanford, CMU, UC Berkeley, Caltech, Georgia Tech, UIUC, Cornell, Princeton, UT Austin)
- **Career-Focused Planning**: Select your career path (Software Engineer, Data Scientist, AI Researcher, Security Engineer, Systems Engineer, Full-Stack Developer)
- **AI-Powered Schedule Generation**: Create optimized 4-year semester schedules based on your major, aspirations, and interests
- **Workload Analysis**: Get AI-analyzed difficulty ratings, time commitments, and study tips for each semester
- **Personalized Guidance**: Receive AI recommendations to optimize your learning and career preparation
- **Smart Recommendations**: Get personalized suggestions for next core courses based on prerequisite fulfillment
- **Interest-Based Electives**: Receive AI-powered elective suggestions based on your interests (AI, cybersecurity, data science, web development, etc.)
- **Modern UI**: Clean, responsive interface with intuitive user experience

## Installation

1. **Clone or download the project files**
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Gemini API (optional but recommended):**
   - Get an API key from [Google AI Studio](https://aistudio.google.com/)
   - **Recommended (Safe):** Create a `.env` file:
     ```bash
     cp env.example .env
     # Then edit .env and add your actual API key
     ```
   - **Alternative:** Set environment variable:
     ```bash
     export GEMINI_API_KEY='your-api-key-here'
     ```
   - **Important:** Never commit your `.env` file or API key to Git!
   - **Note:** The app works without API key but uses basic rule-based analysis

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser and visit:**
   ```
   http://127.0.0.1:5000
   ```

## Usage

1. **Select Your College**: Choose your university from the dropdown menu
2. **Mark Completed Courses**: Check off courses you have already completed
3. **Enter Your Interests**: List your areas of interest (e.g., "AI, cybersecurity, data science")
4. **Get Recommendations**: Click the button to receive personalized course suggestions

The system will show you:
- **Next Core Courses**: Available courses you can take based on completed prerequisites, prioritized by academic level
- **Suggested Electives**: Courses matching your interests with explanations for why they were recommended

## Project Structure

```
college-planner-ai/
├── app.py                    # Flask application with routes and logic
├── planner.py               # Core recommendation algorithms
├── courses.json            # Course prerequisites and metadata
├── college_curriculums.json # College course offerings
├── requirements.txt         # Python dependencies
├── templates/
│   └── index.html          # Main web interface
└── static/
    └── styles.css          # Modern styling and responsive design
```

## How It Works

### AI-Powered Schedule Generation
- **Career Path Prioritization**: Prioritizes courses essential for your career goals
- **Interest Integration**: Incorporates your interests into elective selection
- **Workload Analysis**: AI analyzes course difficulty, time commitment, and provides study tips
- **Semester Guidance**: AI provides personalized recommendations for optimizing each semester

### Prerequisite Logic
- Supports complex prerequisite requirements (courses requiring multiple prerequisites)
- Checks that ALL prerequisites are completed before suggesting a course
- Prioritizes courses by academic level (freshman → sophomore → junior → senior)

### Elective Suggestions
- Uses keyword matching to find courses relevant to your interests
- Matches against course tags, names, and descriptions
- Ranks suggestions by relevance and number of matches

### Data Structure
- **courses.json**: Contains prerequisite mappings, course levels, credits, descriptions, and career path data
- **college_curriculums.json**: Maps each college to their available course offerings

## Supported Interests

The system recognizes these interest categories:
- **AI**: Artificial Intelligence, Machine Learning, Natural Language Processing
- **Cybersecurity**: Computer Security, Cryptography
- **Data Science**: Data analysis, visualization, statistics
- **Web Development**: Web technologies, mobile app development
- **Networking**: Computer networks, distributed systems
- **Graphics**: Computer graphics, visualization
- **Systems**: Operating systems, computer architecture

## Future Enhancements

- **Enhanced AI Recommendations**: More sophisticated prompt engineering for better suggestions
- **User Accounts**: Save progress and preferences
- **Visual Progress Tracking**: Graphical representation of degree completion
- **College Comparisons**: Side-by-side curriculum comparisons
- **Advanced Prerequisites**: Support for OR prerequisites and credit hour requirements
- **Course Conflict Detection**: Check for scheduling conflicts and suggest alternatives
- **Internship/Capstone Integration**: Plan for internships, research, and capstone projects

## Technical Details

- **Backend**: Flask (Python 3.10+)
- **AI Integration**: Google Gemini 1.5 Flash for workload analysis and schedule guidance
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Data Storage**: JSON files (no database required)
- **Styling**: Modern CSS with responsive design and smooth animations

### AI Features (Powered by Google Gemini)
- **Workload Analysis**: Analyzes course combinations to predict difficulty, time commitment, and potential challenges
- **Schedule Optimization**: Provides personalized recommendations for balancing coursework, career goals, and interests
- **Study Tips**: AI-generated actionable advice for succeeding in each semester
- **Free Tier Support**: Gemini API offers a generous free tier for development and personal use

## Contributing

This is an MVP (Minimum Viable Product) designed to demonstrate core functionality. Future versions will include more sophisticated recommendation algorithms and enhanced user features.

## License

This project is created for educational purposes. Feel free to use and modify as needed.

---

Built with ❤️ for computer science students
