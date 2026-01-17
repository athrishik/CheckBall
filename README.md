# CheckBall ⚡

**Your Premium Sports Dashboard with AI-Powered Predictions**

A stunning, modern sports dashboard that delivers real-time scores, live game tracking, and intelligent predictions powered by live ESPN data. Experience the future of sports tracking with premium glassmorphic design and stadium-lights aesthetic.

---

## ✨ Features

### 🎯 Core Features
- **Smart Game Prioritization**: Live games first, then today's completed games, then upcoming matches
- **AI-Powered Predictions**: Win probabilities and predicted scores based on recent team performance
- **Multi-Sport Coverage**: NBA, WNBA, NFL, MLS, Premier League, La Liga, MLB, NHL
- **Real-Time Data**: Live ESPN API integration for up-to-the-second accuracy
- **Dual Display Logic**: Completed games show scores, upcoming games show times

### 🔮 Prediction Engine
- **Win Probability Analysis**: Advanced statistical modeling using recent team performance
- **Predicted Score Forecasting**: Data-driven score predictions based on team averages and form
- **Home Court Advantage**: Factors in location impact on game outcomes
- **Confidence Ratings**: High/Medium/Low confidence indicators for each prediction
- **Sport-Specific Metrics**: Basketball (FG%, 3PT%), Football, Soccer, Baseball, Hockey stats

### 🎨 Premium Design
- **Stadium Lights Aesthetic**: Dramatic neon glows and atmospheric effects
- **Glassmorphic UI**: Modern, translucent cards with depth and shadows
- **Custom Typography**: Orbitron and Rajdhani fonts for athletic feel
- **Kinetic Animations**: Smooth transitions, pulsing live games, hover effects
- **Responsive Design**: Perfect on desktop, tablet, and mobile

### ⚙️ User Experience
- **Individual Widget Control**: Reconfigure any widget independently
- **Manual Refresh**: Static display until "Check In" button clicked
- **Persistent Configuration**: Your settings saved automatically
- **Game Details Modal**: Deep dive into statistics and player performance
- **Next Game Preview**: See upcoming matchups below main scores

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/athrishik/checkball.git
cd checkball
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python checkball.py
```

4. **Open your browser**:
Navigate to `http://localhost:5000`

---

## 🎮 Usage Guide

### Getting Started
1. **Select Sports**: Choose from 8 different sports leagues
2. **Pick Teams**: Select your favorite teams from comprehensive lists
3. **Check Scores**: Click "Check In" to get latest scores and schedules
4. **View Predictions**: Click game details to see AI-powered win predictions
5. **Reconfigure**: Use the ⚙️ button to change teams without resetting

### Prediction Features
- **Win Probability Bars**: Visual representation of each team's chances
- **Predicted Final Scores**: AI forecast based on recent team performance
- **Confidence Indicators**: Know how reliable each prediction is
- **Recent Form Analysis**: See team performance trends

---

## 🎯 Game Priority Logic

CheckBall intelligently displays games in this order:
1. **Live/In-Progress games** (with pulsing animations and live updates)
2. **Today's completed games** (with final scores)
3. **Recent completed games** (yesterday or earlier)
4. **Upcoming games** (shows times and predictions, not 0-0 scores)

---

## 🧠 Prediction Model

### How It Works
Our prediction engine analyzes:
- **Recent Team Performance**: Last 10 games statistics
- **Scoring Trends**: Average points for and against
- **Home Court Advantage**: 3-point boost for home teams
- **Sport-Specific Metrics**:
  - Basketball: Field Goal %, 3-Point %, Rebounds, Assists
  - Football: Passing Yards, Rushing Yards, Touchdowns
  - Soccer: Goals, Assists, Shots, Saves
  - Baseball: Hits, RBIs, Pitching Stats
  - Hockey: Goals, Assists, Saves

### Prediction Accuracy
- Weighted algorithm based on correlation analysis
- Field Goal % is the strongest predictor for basketball (45% correlation with wins)
- Home court provides 5% win probability boost
- Confidence ratings: High (>70% probability), Medium (55-70%), Low (<55%)

---

## 🎨 Design Features

### Stadium Lights Aesthetic
- **Neon Glow Effects**: Electric blue/purple gradient theme
- **Atmospheric Background**: Animated radial gradients simulate stadium lighting
- **Field Lines Pattern**: Subtle grid overlay for sports field feel
- **Dramatic Shadows**: Deep, layered shadows for premium depth

### Typography
- **Orbitron**: Futuristic display font for headers and scores
- **Rajdhani**: Athletic sans-serif for body text and labels
- **Letter Spacing**: Wide tracking for uppercase headings

### Interactive Elements
- **Hover Transformations**: Cards lift and glow on hover
- **Pulsing Live Indicators**: Animated badges for in-progress games
- **Smooth Transitions**: Cubic-bezier easing for natural motion
- **Shimmer Effects**: Animated highlights on prediction bars

---

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - Main dashboard
- `GET /api/teams/<sport>` - Get teams for a sport
- `GET /api/scores/<sport>/<team>` - Get scores for a team
- `GET /api/game-details/<sport>/<team>` - Get detailed game data

### Prediction Endpoints
- `POST /api/predict` - Get game outcome prediction
  ```json
  {
    "sport": "nba",
    "team1": "Lakers",
    "team2": "Warriors",
    "location": "team1_home"
  }
  ```
- `GET /api/upcoming-games/<sport>/<team>` - Get upcoming games with predictions

### Configuration
- `POST /save_config` - Save widget configuration
- `GET /load_config` - Load saved configuration

---

## 📊 Supported Sports

| Sport | Teams | Prediction Support | Special Metrics |
|-------|-------|-------------------|-----------------|
| NBA | 30 teams | ✅ | FG%, 3PT%, Rebounds |
| WNBA | 12 teams | ✅ | FG%, 3PT%, Assists |
| NFL | 32 teams | ✅ | Pass Yds, Rush Yds |
| MLS | 29 teams | ✅ | Goals, Shots |
| Premier League | 20 teams | ✅ | Goals, Assists |
| La Liga | 20 teams | ✅ | Goals, Shots |
| MLB | 30 teams | ✅ | Hits, RBIs, ERA |
| NHL | 32 teams | ✅ | Goals, Saves |

---

## 🚀 Deployment

### Railway (Recommended)
1. Push to GitHub
2. Connect repo to [Railway](https://railway.app)
3. Auto-deploy on push
4. Set environment variable: `PORT=5000`

### Heroku
```bash
heroku create checkball-app
git push heroku main
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "checkball.py"]
```

### Local Development
```bash
export FLASK_ENV=development
export PORT=5000
python checkball.py
```

---

## 🔒 Security Features

- **Rate Limiting**: Prevents API abuse with per-minute limits
- **Input Sanitization**: XSS protection on all user inputs
- **Security Headers**: CSP, X-Frame-Options, HSTS enabled
- **Secure Cookies**: HttpOnly, SameSite flags for session data
- **Request Timeouts**: Prevents hanging connections
- **API Caching**: TTL cache reduces external API calls

---

## 🛠️ Technical Stack

### Backend
- **Flask**: Lightweight Python web framework
- **NumPy**: Numerical computing for predictions
- **Requests**: HTTP library for ESPN API
- **PyTZ**: Timezone handling
- **Flask-Limiter**: Rate limiting middleware
- **CacheTools**: Response caching

### Frontend
- **Vanilla JavaScript**: No framework dependencies
- **Modern CSS**: Glassmorphism, animations, gradients
- **Google Fonts**: Orbitron & Rajdhani
- **ESPN API**: Live sports data

### Design
- **Custom CSS Variables**: Consistent theming
- **Responsive Grid**: Mobile-first approach
- **Backdrop Filters**: Native blur effects
- **CSS Animations**: Hardware-accelerated transforms

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License & Attribution

CheckBall is open source under the MIT License.

**If you use CheckBall:**
- ✅ Keep the "Developed by Hrishik Kunduru" credit in the footer
- ✅ Include the LICENSE file in your copy
- ✅ Star this repo if it helps you! ⭐

**You're free to:**
- Use for personal or commercial projects
- Modify and customize the code
- Distribute your own versions

**Just remember to give credit where it's due! 🙏**

See the [LICENSE](LICENSE) file for full details.

---

## 🙏 Acknowledgments

- **ESPN** for providing comprehensive sports data APIs
- **Sports fans everywhere** for inspiration
- **Modern web design trends** for the beautiful UI patterns
- **M** for being awesome and supportive always

---

## 📧 Contact

**Hrishik Kunduru** - [@AtHrishik](https://linkedin.com/in/hrishikkunduru)

Project Link: [https://github.com/athrishik/checkball](https://github.com/athrishik/checkball)

---

<div align="center">

⭐ **Star this repo if you found it helpful!** ⭐

Built with ❤️ by [Hrishik Kunduru](https://github.com/athrishik)

</div>
