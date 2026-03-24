# 🎮 LevelUp - AI-Powered Gamified Life System

Transform your daily tasks into an RPG-like progression system. Complete tasks, gain XP, level up your stats, and watch your character evolve!

## 🌟 Features

- **AI-Powered Task Classification**: Claude AI automatically categorizes tasks and assigns stats
- **6 Core Stats**: Strength, Stamina, Mind, Discipline, Self-Care, Social
- **Dynamic XP System**: Adjusted leveling curve for balanced progression
- **Streak Tracking**: Build daily completion streaks
- **Real-time Progress**: Watch your stats grow with every completed task
- **Beautiful UI**: Modern, responsive design with smooth animations

## 🏗️ Tech Stack

### Backend
- **Node.js** + **Express**: RESTful API server
- **MongoDB**: Database for users and tasks
- **Anthropic Claude API**: AI-powered task classification
- **Mongoose**: MongoDB object modeling

### Frontend
- **React** (Vite): Fast, modern UI framework
- **Axios**: HTTP client for API calls
- **CSS3**: Custom styling with gradients and animations

## 📋 Prerequisites

- Node.js (v16 or higher)
- MongoDB (local or Atlas)
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd levelup-app
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env with your configuration
# Required:
# - MONGODB_URI=mongodb://localhost:27017/levelup
# - ANTHROPIC_API_KEY=your_api_key_here
# - PORT=5000
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Edit .env
# VITE_API_URL=http://localhost:5000/api
```

### 4. Start MongoDB

Make sure MongoDB is running:

```bash
# If using local MongoDB
mongod

# Or use MongoDB Atlas connection string in .env
```

## 🎯 Running the Application

### Start Backend Server

```bash
cd backend
npm run dev
```

Backend will run on `http://localhost:5000`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

Frontend will run on `http://localhost:5173`

## 📝 First Time Setup

### Create a User

Before using the app, create a user via API:

```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Your Name",
    "email": "your.email@example.com"
  }'
```

Save the returned `id` and update it in `frontend/src/App.jsx`:

```javascript
const DEMO_USER_ID = 'your_user_id_here';
```

## 🎮 How to Use

### 1. Create a Task
- Click "+ New Task"
- Enter task title (e.g., "Go for a 5km run")
- Click "🤖 Classify with AI"
- Review and adjust AI suggestions
- Click "✓ Create Task"

### 2. Complete Tasks
- Click "✓ Complete" on any pending task
- Earn XP and watch your stats grow!
- Build your daily streak

### 3. Track Progress
- View your stats in the sidebar
- Check your global level and title
- Monitor individual stat levels
- Track your completion streak

## 📊 XP System

### Base XP by Difficulty
- **Easy**: 5 XP
- **Medium**: 10 XP
- **Hard**: 20 XP

### XP Calculation
```
Total XP = Base XP + (Effort Score × 1.5)
```

### Leveling Formula
```
XP Required = 100 × (Level ^ 1.3)
```

This creates a balanced progression:
- Level 5: 844 XP
- Level 10: 2,009 XP
- Level 20: 5,179 XP
- Level 50: 18,946 XP

### XP Distribution
- **Primary Stat**: 80% of XP
- **Secondary Stat**: 20% of XP (if assigned)

## 🏆 Titles

Unlock titles as you level up:
- Level 1: Beginner
- Level 5: Apprentice
- Level 10: Disciplined
- Level 20: Elite
- Level 50: Ascended

## 🔧 API Endpoints

### Users
- `POST /api/users` - Create user
- `GET /api/users/:id` - Get user profile
- `GET /api/users/:id/stats` - Get user stats
- `PUT /api/users/:id` - Update user

### Tasks
- `POST /api/tasks/classify` - Classify task with AI
- `POST /api/tasks` - Create task
- `GET /api/tasks/user/:userId` - Get user's tasks
- `GET /api/tasks/user/:userId/today` - Get today's tasks
- `POST /api/tasks/:id/complete` - Complete task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task

## 🎨 Customization

### Adjust XP Formula

Edit `backend/src/utils/xpCalculator.js`:

```javascript
const EFFORT_MULTIPLIER = 1.5; // Increase for more XP impact
const calculateXPForLevel = (level) => {
  return Math.round(100 * Math.pow(level, 1.3)); // Adjust exponent
};
```

### Add New Stats

1. Update `backend/src/models/User.js` stats schema
2. Update `frontend/src/utils/statIcons.js` with new stat icons/colors
3. Update AI prompt in `backend/src/services/aiService.js`

## 🐛 Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running
- Check connection string in `.env`
- Verify network access if using Atlas

### AI Classification Fails
- Verify Anthropic API key in `.env`
- Check API key has sufficient credits
- Review error logs in backend console

### Frontend Can't Connect to Backend
- Ensure backend is running on port 5000
- Check `VITE_API_URL` in frontend `.env`
- Verify CORS is enabled in backend

## 📈 Future Enhancements

- [ ] User authentication & authorization
- [ ] Weekly/monthly challenges (Quests)
- [ ] Social features (leaderboards, friends)
- [ ] Mobile app (React Native)
- [ ] Data visualization & insights
- [ ] Wearable device integration
- [ ] AI coaching & recommendations
- [ ] Avatar customization
- [ ] Achievement system

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 💬 Support

For issues or questions, please open an issue on GitHub.

---

**Built with ❤️ using React, Node.js, MongoDB, and Claude AI**