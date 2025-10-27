# Deploying College Planner AI to Vercel

## Prerequisites

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

## Deployment Steps

### 1. Navigate to Project Directory
```bash
cd college-planner-ai
```

### 2. Deploy to Vercel
```bash
vercel --prod
```

Or use Vercel Dashboard:
1. Go to https://vercel.com
2. Import your GitHub repository
3. Vercel will auto-detect the Python project

### 3. Configure Environment Variables

**IMPORTANT:** Add your Gemini API key in Vercel dashboard:

1. Go to your project settings in Vercel
2. Navigate to "Environment Variables"
3. Add:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** Your actual Gemini API key
   - **Environment:** Production (and all others if desired)

### 4. Files Included

The deployment includes:
- ✅ `vercel.json` - Vercel configuration
- ✅ `requirements_vercel.txt` - Python dependencies
- ✅ `app.py` - Flask application
- ✅ `planner.py` - Core logic
- ✅ `courses.json` & `college_curriculums.json` - Data files
- ✅ `templates/` & `static/` - Frontend files

### 5. After Deployment

Your app will be live at:
`https://your-project-name.vercel.app`

## Files Configured

- **vercel.json** - Tells Vercel this is a Python Flask app
- **requirements_vercel.txt** - Python dependencies for production
- **app.py** - Added `application = app` for Vercel compatibility

## Key Differences for Vercel

- Uses `vercel.json` configuration instead of `requirements.txt`
- Needs `application = app` variable for WSGI compatibility
- Environment variables set in Vercel dashboard, not `.env` file
- Automatic HTTPS and CDN

## Troubleshooting

**Build fails?**
- Check that all files are committed to Git
- Ensure `courses.json` and `college_curriculums.json` are in the repository
- Check build logs in Vercel dashboard

**API key not working?**
- Verify `GEMINI_API_KEY` is set in Vercel environment variables
- Redeploy after adding environment variables

**Static files not loading?**
- Check that `static/` and `templates/` folders are in the repository
- Verify file paths in `app.py` are relative

## Local Testing

To test locally with Vercel settings:
```bash
vercel dev
```

This runs your app with Vercel's environment locally.

