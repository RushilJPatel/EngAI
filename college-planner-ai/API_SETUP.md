# Setting Up Gemini API Key

## Quick Setup Instructions

### 1. Create the .env file (if it doesn't exist)

In PowerShell, run:
```powershell
cd "C:\Users\Rushi\OneDrive\Desktop\EngAI\college-planner-ai"
Copy-Item env.example .env
```

### 2. Add Your API Key

Edit the `.env` file and replace `your-actual-api-key-here` with your actual Gemini API key:

```
GEMINI_API_KEY=AIzaSy...your-actual-key-here
```

**Example:**
```
GEMINI_API_KEY=AIzaSyABCD1234efgh5678ijkl
```

### 3. Restart the Flask Application

Since the app is already running:
1. Press `CTRL+C` in the terminal where Flask is running
2. Run `python app.py` again

Or just restart it from VS Code terminal.

### 4. Verify It's Working

When you generate a full 4-year schedule, you should see:
- AI-powered workload analysis (not just basic analysis)
- Detailed study tips and recommendations
- Personalized guidance per semester

## What You'll Get With AI Features

✅ **Advanced Workload Analysis**
- AI-analyzed difficulty ratings
- Time commitment estimates
- Study challenges and tips
- Balance analysis

✅ **Personalized Guidance**
- Career-focused recommendations
- Semester optimization tips
- Learning strategy suggestions

## Troubleshooting

**API key not working?**
- Make sure there are no extra spaces in the `.env` file
- Verify your API key is valid at https://aistudio.google.com/
- Check the Flask console for error messages

**Don't have an API key?**
- Get one free at: https://aistudio.google.com/
- The app works without it, just uses basic analysis instead

## Security Note

⚠️ **Never commit your `.env` file to Git!**

The `.env` file is already in `.gitignore` for your protection. Keep your API key safe and never share it publicly.

