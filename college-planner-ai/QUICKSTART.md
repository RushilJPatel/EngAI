# College Planner AI - Quick Start Guide

## 🚀 Getting Started

Your College Planner AI application is ready to use! Follow these steps:

### 1. Start the Application

Open PowerShell in the `college-planner-ai` folder and run:

```powershell
python app.py
```

The application will start at: **http://127.0.0.1:5000**

### 2. Open Your Browser

Navigate to: **http://127.0.0.1:5000**

### 3. Use the Application

**Step-by-Step Process:**

1. **Select Your College** - Choose from 10 top-tier CS universities
2. **Choose Your Career Path** (Optional) - Select Software Engineer, Data Scientist, AI Researcher, etc.
3. **Mark Completed Courses** - Check off courses you've already taken
4. **Enter Your Interests** - Type interests like "AI, cybersecurity, data science"
5. **Get Recommendations** - Click either:
   - "Get Course Recommendations" - Shows next available courses
   - "Generate Full 4-Year Schedule" - Creates complete semester-by-semester plan

## ✨ Features

### Course Recommendations
- Smart prerequisite checking
- Prioritized by academic level
- Shows available courses based on your progress

### AI-Powered Scheduling
- Full 4-year degree plan
- Career-focused course prioritization
- Interest-based elective suggestions
- Workload analysis (if AI is enabled)

### Additional Features
- Beautiful, modern UI with gradient design
- Responsive layout (mobile-friendly)
- Real-time course suggestions
- Detailed course descriptions
- Career path alignment

## 🔑 Optional: Enable AI Features

For enhanced AI-powered workload analysis and guidance:

1. Get a Google Gemini API key from: https://aistudio.google.com/
2. Create a `.env` file in the `college-planner-ai` folder
3. Add your API key: `GEMINI_API_KEY=your-actual-api-key-here`
4. Restart the application

**Note:** The app works without an API key but uses basic analysis instead of AI-enhanced insights.

## 📋 Supported Universities

- MIT (Massachusetts Institute of Technology)
- Stanford University
- Carnegie Mellon University (CMU)
- UC Berkeley
- Caltech (California Institute of Technology)
- Georgia Tech
- UIUC (University of Illinois at Urbana-Champaign)
- Cornell University
- Princeton University
- UT Austin (University of Texas at Austin)

## 🎯 Career Paths

- Software Engineer
- Data Scientist
- AI Researcher
- Security Engineer
- Systems Engineer
- Full-Stack Developer

## 📦 What's Included

- ✅ Complete Flask backend with REST API
- ✅ Beautiful, responsive frontend
- ✅ Prerequisite logic engine
- ✅ Course recommendation system
- ✅ Semester schedule generator
- ✅ Career path prioritization
- ✅ Interest-based elective suggestions
- ✅ AI workload analysis (with Gemini API)
- ✅ Modern gradient UI design

## 🛠️ Technical Details

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **AI:** Google Gemini 1.5 Flash (optional)
- **Data:** JSON files (courses.json, college_curriculums.json)
- **Dependencies:** Flask, google-generativeai, python-dotenv

## 📚 Course Structure

### Core Courses (All Levels)
- Intro to Computer Science
- Data Structures
- Discrete Mathematics
- Algorithms
- Computer Architecture
- Operating Systems
- Database Systems

### Specialized Courses
- Machine Learning
- Artificial Intelligence
- Computer Security
- Computer Networks
- Software Engineering
- Data Science
- Web Development
- Computer Graphics
- Distributed Systems
- Mobile App Development
- Cryptography
- Natural Language Processing

## 🎓 How It Works

1. **Course Prerequisites:** The system checks if you've completed required prerequisites before suggesting courses
2. **Level Prioritization:** Courses are organized by academic year (freshman, sophomore, junior, senior)
3. **Career Alignment:** Your selected career path prioritizes relevant courses
4. **Interest Matching:** Electives are suggested based on keywords matching your interests
5. **Workload Analysis:** AI analyzes course difficulty and time commitment

## 💡 Tips

- **Mark all completed courses** for accurate recommendations
- **Enter specific interests** to get relevant elective suggestions
- **Select a career path** for optimized course sequencing
- **Generate full schedule** to see your complete 4-year plan

## 🐛 Troubleshooting

**Port 5000 already in use?**
- Change the port in `app.py` (line 147): `app.run(debug=True, host='127.0.0.1', port=5001)`

**Can't find colleges/courses?**
- Make sure you're in the `college-planner-ai` directory
- Ensure `college_curriculums.json` and `courses.json` exist

**AI features not working?**
- Check if `.env` file exists with your Gemini API key
- API key is optional - app works without it

## 🎉 You're All Set!

Open your browser and start planning your computer science degree!

**Happy Planning! 🎓**

