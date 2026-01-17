# 🚀 Push to GitHub & Deploy

## Step 1: Create GitHub Repository

1. Go to [github.com](https://github.com)
2. Click the **+** icon (top right) → **New repository**
3. Repository name: `checkball-sports-dashboard`
4. Description: `AI-powered sports dashboard with live ESPN data and predictive modeling`
5. Keep it **Public** (or Private if you prefer)
6. **DO NOT** initialize with README (we already have one)
7. Click **Create repository**

---

## Step 2: Push Your Code

GitHub will show you commands. Use these:

```bash
# Navigate to your project
cd "/Users/hrishikkunduru/Documents/NBA-Game-Analysis-CS555-MainCodebase copy"

# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/checkball-sports-dashboard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Example** (if your username is `hrishikkunduru`):
```bash
git remote add origin https://github.com/hrishikkunduru/checkball-sports-dashboard.git
git branch -M main
git push -u origin main
```

---

## Step 3: Deploy on Render (FREE)

### Why Render?
- ✅ **FREE tier** (no credit card required!)
- ✅ Auto-deploys when you push to GitHub
- ✅ Custom domain support
- ✅ SSL certificate included
- ✅ Easy setup (2 minutes)

### Steps:

1. **Go to [render.com](https://render.com)**
2. **Sign up** with your GitHub account (click "GitHub" button)
3. **Authorize Render** to access your repositories
4. Click **New +** → **Web Service**
5. Find your `checkball-sports-dashboard` repository
6. Click **Connect**

### Configuration (Render auto-fills most):
- **Name**: `checkball` (or any name you want)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn checkball:app`
- **Plan**: Select **Free**

7. Click **Create Web Service**

### That's it! 🎉

Render will:
- Install dependencies
- Start your app
- Give you a URL like: `https://checkball.onrender.com`

**First deployment takes ~5 minutes**

---

## Alternative: Railway (Also FREE)

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click **New Project** → **Deploy from GitHub repo**
4. Select `checkball-sports-dashboard`
5. Railway auto-detects Flask and deploys!

**URL**: `checkball.up.railway.app`

---

## Step 4: Test Your Deployed App

Once deployed, test these features:
- ✅ Select a sport and team
- ✅ View game scores
- ✅ Click game details modal
- ✅ Test predictions
- ✅ Check upcoming games

---

## Updating Your App

After making changes locally:

```bash
cd "/Users/hrishikkunduru/Documents/NBA-Game-Analysis-CS555-MainCodebase copy"

# Stage changes
git add .

# Commit
git commit -m "Description of changes"

# Push to GitHub
git push
```

**Render/Railway will auto-deploy** your changes in ~2 minutes!

---

## Custom Domain (Optional)

### On Render:
1. Dashboard → Your service → Settings
2. Scroll to **Custom Domain**
3. Add your domain (e.g., `checkball.app`)
4. Follow DNS instructions

### On Railway:
1. Project → Settings → Domains
2. Add custom domain
3. Configure DNS

---

## Troubleshooting

### "Build failed"
- Check Render logs
- Ensure `requirements.txt` is correct
- Verify `Procfile` exists

### "Application Error"
- Check runtime logs in Render dashboard
- Ensure port binding is correct (already configured)

### "Can't connect to GitHub"
- Re-authorize Render/Railway
- Check repository is public (or grant Render access to private repos)

---

## 📊 Your App URLs After Deployment

- **Render**: `https://checkball.onrender.com`
- **Railway**: `https://checkball.up.railway.app`
- **Custom**: `https://your-domain.com`

---

## GitHub Pages? Hugging Face Spaces?

**GitHub Pages**: ❌ Only for static sites (HTML/CSS/JS), not Flask apps

**Hugging Face Spaces**: ⚠️ For ML demos, but CheckBall would need conversion to Streamlit/Gradio

**Best options for CheckBall**:
1. ✅ **Render** (Recommended - FREE, easy)
2. ✅ **Railway** (FREE $5/month credit)
3. ✅ **Heroku** ($5/month - very stable)
4. ✅ **DigitalOcean** ($5/month - fast)

---

## Need Help?

If you get stuck:
1. Check the logs in Render/Railway dashboard
2. Ensure you pushed all files to GitHub
3. Verify `Procfile` and `requirements.txt` are present

---

**Ready to deploy?** Follow Steps 1-3 above! 🚀
