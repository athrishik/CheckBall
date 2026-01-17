# CheckBall Deployment Guide

> **Important**: This is a Flask app, not a Streamlit app. Deploy using one of the methods below.

## 🚀 Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

**Steps:**
1. Create a `render.yaml` in your project root (already included below)
2. Push code to GitHub
3. Go to [render.com](https://render.com) and sign up
4. Click "New +" → "Web Service"
5. Connect your GitHub repository
6. Render will auto-detect the configuration
7. Click "Deploy"

**Pros:**
- Free tier available
- Auto-deploys from GitHub
- Easy setup
- Good performance

**Estimated time:** 10-15 minutes

---

### Option 2: Railway (Easy, Free Tier)

**Steps:**
1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "Start a New Project"
4. Select "Deploy from GitHub repo"
5. Railway auto-detects Flask and deploys

**Pros:**
- Very easy setup
- Free $5 credit/month
- Fast deployment

**Estimated time:** 5-10 minutes

---

### Option 3: Heroku (Paid but reliable)

**Steps:**
1. Install Heroku CLI: `brew install heroku` (Mac) or download from heroku.com
2. Login: `heroku login`
3. Create app: `heroku create checkball-sports`
4. Push code: `git push heroku main`

**Pros:**
- Very stable
- Good documentation
- Easy scaling

**Cons:**
- No free tier (starts at $5/month)

**Estimated time:** 15-20 minutes

---

### Option 4: PythonAnywhere (Beginner-friendly)

**Steps:**
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Go to "Web" tab → "Add a new web app"
3. Choose "Flask" and Python 3.9+
4. Upload your code via Git or file upload
5. Set working directory and configure WSGI

**Pros:**
- Free tier available
- Beginner-friendly
- No credit card required

**Cons:**
- Slower than other options
- Limited free tier

**Estimated time:** 20-30 minutes

---

### Option 5: DigitalOcean App Platform

**Steps:**
1. Push code to GitHub
2. Go to [digitalocean.com](https://www.digitalocean.com)
3. Create "App" → Connect GitHub repo
4. Configure as Flask app
5. Deploy

**Pros:**
- $5/month
- Very fast
- Good scaling options

**Estimated time:** 15 minutes

---

## 📋 Required Files (Already Included)

### `requirements.txt`
Already present - lists all Python dependencies

### `Procfile` (for Render/Heroku)
Create this file in project root:
```
web: gunicorn checkball:app
```

### `render.yaml` (for Render)
Create this file in project root:
```yaml
services:
  - type: web
    name: checkball
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn checkball:app"
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
```

---

## 🔧 Environment Variables

Set these on your hosting platform:

| Variable | Value | Purpose |
|----------|-------|---------|
| `PORT` | `5000` or auto | Port to run on |
| `FLASK_ENV` | `production` | Production mode |

---

## ✅ Pre-Deployment Checklist

- [ ] Push code to GitHub
- [ ] Verify `requirements.txt` is complete
- [ ] Create `Procfile` (if using Render/Heroku)
- [ ] Test locally: `python3 checkball.py`
- [ ] Ensure port is configurable (already done)

---

## 🎯 Recommended: Render (Free)

**Quick Start with Render:**

1. Add `Procfile` to project root:
   ```bash
   echo "web: gunicorn checkball:app" > Procfile
   ```

2. Add `gunicorn` to requirements.txt:
   ```bash
   echo "gunicorn==21.2.0" >> requirements.txt
   ```

3. Push to GitHub:
   ```bash
   git add .
   git commit -m "Add deployment files"
   git push
   ```

4. Deploy on Render:
   - Go to render.com
   - New Web Service
   - Connect GitHub repo
   - Deploy!

---

## 🌐 Custom Domain (Optional)

Once deployed, you can add a custom domain:

**Render:** Settings → Custom Domain → Add your domain
**Railway:** Settings → Domain → Add custom domain
**Heroku:** Settings → Domains → Add custom domain

---

## 📊 Monitoring & Analytics

After deployment, consider adding:

- **Google Analytics** - Track visitors
- **Sentry** - Error tracking
- **Uptime Robot** - Monitor uptime (free)

---

## 🐛 Common Issues

**Issue**: App crashes on startup
**Fix**: Check logs, ensure all dependencies in requirements.txt

**Issue**: Port binding error
**Fix**: Use `PORT` environment variable (already configured)

**Issue**: Static files not loading
**Fix**: Ensure `/static` folder is included in deployment

---

## 🚀 Next Steps After Deployment

1. Test all features (predictions, game details, etc.)
2. Share your live URL!
3. Monitor for errors in first 24 hours
4. Set up automatic GitHub deployments (auto-deploy on push)

---

## 💡 Why Not Streamlit?

This app uses:
- **Flask** (not Streamlit) for the backend
- **Vanilla JavaScript** for interactivity
- **ESPN API** for live data

Streamlit is for data science dashboards. CheckBall is a full web app with custom UI, real-time updates, and advanced features that require Flask.

---

## Need Help?

If you encounter issues:
1. Check the hosting platform's logs
2. Verify all files are uploaded
3. Ensure environment variables are set
4. Test locally first

Happy deploying! 🎉
