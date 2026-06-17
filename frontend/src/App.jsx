import React, { useState, useEffect } from 'react';
import { userAPI, taskAPI } from './services/api';
import StatsPanel from './components/StatsPanel';
import TaskCard from './components/TaskCard';
import TaskForm from './components/TaskForm';
import './styles/App.css';

function App() {
  const [user, setUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [todayStats, setTodayStats] = useState({ completed: 0, pending: 0 });
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState('today'); // 'today', 'all', 'completed'
  const [userId, setUserId] = useState(null);
  const [userError, setUserError] = useState(null);
  const [showUserSetup, setShowUserSetup] = useState(false);
  const [newUserName, setNewUserName] = useState('');
  const [newUserEmail, setNewUserEmail] = useState('');

  // Get user ID from localStorage or prompt for setup
  useEffect(() => {
    const storedUserId = localStorage.getItem('levelup_user_id');
    if (storedUserId) {
      setUserId(storedUserId);
    } else {
      setShowUserSetup(true);
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (userId) {
      loadUserData();
      loadTasks();
    }
  }, [view, userId]);

  const loadUserData = async () => {
    try {
      const response = await userAPI.getById(userId);
      setUser(response.data.user);
      setUserError(null);
    } catch (error) {
      console.error('Error loading user:', error);
      if (error.response?.status === 404) {
        setUserError('User not found. Please set up your account.');
        setShowUserSetup(true);
        localStorage.removeItem('levelup_user_id');
        setUserId(null);
      } else {
        setUserError('Failed to load user data. Please check your connection.');
      }
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    if (!newUserName.trim() || !newUserEmail.trim()) {
      alert('Please enter both name and email');
      return;
    }

    try {
      const response = await userAPI.create({
        name: newUserName.trim(),
        email: newUserEmail.trim()
      });
      const createdUserId = response.data.user.id;
      localStorage.setItem('levelup_user_id', createdUserId);
      setUserId(createdUserId);
      setShowUserSetup(false);
      setUserError(null);
      setNewUserName('');
      setNewUserEmail('');
    } catch (error) {
      console.error('Error creating user:', error);
      console.error('Error details:', error.response?.data);
      alert('Failed to create user. Please try again.');
    }
  };

  const handleResetUser = () => {
    if (window.confirm('Are you sure you want to reset your user? This will clear your current user ID.')) {
      localStorage.removeItem('levelup_user_id');
      setUserId(null);
      setUser(null);
      setTasks([]);
      setShowUserSetup(true);
    }
  };

  const loadTasks = async () => {
    if (!userId) return;
    
    setLoading(true);
    try {
      let response;
      if (view === 'today') {
        response = await taskAPI.getTodayTasks(userId);
        setTodayStats({
          completed: response.data.completed,
          pending: response.data.pending
        });
      } else {
        const params = view === 'completed' ? { completed: true } : {};
        response = await taskAPI.getByUser(userId, params);
      }
      setTasks(response.data.tasks);
    } catch (error) {
      console.error('Error loading tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskComplete = async (taskId) => {
    try {
      const response = await taskAPI.complete(taskId);
      
      // Show success message with XP gained
      alert(`🎉 Task completed! +${response.data.xpGained} XP earned!`);
      
      // Reload data
      await loadUserData();
      await loadTasks();
    } catch (error) {
      console.error('Error completing task:', error);
      alert('Failed to complete task. Please try again.');
    }
  };

  const handleTaskDelete = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await taskAPI.delete(taskId);
        await loadTasks();
      } catch (error) {
        console.error('Error deleting task:', error);
        alert('Failed to delete task. Please try again.');
      }
    }
  };

  const handleTaskCreated = async () => {
    setShowTaskForm(false);
    await loadTasks();
  };

  const pendingTasks = tasks.filter(t => !t.completed);
  const completedTasks = tasks.filter(t => t.completed);

  // Show user setup screen if no user ID
  if (showUserSetup) {
    return (
      <div className="app">
        <header className="app-header">
          <h1>LevelUp</h1>
          <p className="tagline">Your Life is an RPG</p>
        </header>
        <div className="user-setup">
          <div className="setup-card">
            <h2>Welcome to LevelUp</h2>
            <p>Create your account to start your journey</p>
            {userError && <div className="error-message">{userError}</div>}
            <form onSubmit={handleCreateUser}>
              <div className="form-group">
                <label htmlFor="name">Name</label>
                <input
                  type="text"
                  id="name"
                  value={newUserName}
                  onChange={(e) => setNewUserName(e.target.value)}
                  placeholder="Enter your name"
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  value={newUserEmail}
                  onChange={(e) => setNewUserEmail(e.target.value)}
                  placeholder="Enter your email"
                  required
                />
              </div>
              <button type="submit" className="btn btn-primary">
                Start Your Journey
              </button>
            </form>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>LevelUp</h1>
        <p className="tagline">Your Life is an RPG</p>
        {user && (
          <button
            className="btn-reset-user"
            onClick={handleResetUser}
            title="Reset User"
          >
            Settings
          </button>
        )}
      </header>

      <div className="app-container">
        <aside className="sidebar">
          <StatsPanel user={user} />
        </aside>

        <main className="main-content">
          <div className="content-header">
            <div className="view-tabs">
              <button
                className={`tab ${view === 'today' ? 'active' : ''}`}
                onClick={() => setView('today')}
              >
                Today
              </button>
              <button
                className={`tab ${view === 'all' ? 'active' : ''}`}
                onClick={() => setView('all')}
              >
                All Tasks
              </button>
              <button
                className={`tab ${view === 'completed' ? 'active' : ''}`}
                onClick={() => setView('completed')}
              >
                Completed
              </button>
            </div>

            <button
              className="btn btn-primary btn-add-task"
              onClick={() => setShowTaskForm(!showTaskForm)}
            >
              {showTaskForm ? 'Cancel' : 'New Task'}
            </button>
          </div>

          {view === 'today' && (
            <div className="today-stats">
              <div className="stat-box">
                <span className="stat-value">{todayStats.completed}</span>
                <span className="stat-label">Completed</span>
              </div>
              <div className="stat-box">
                <span className="stat-value">{todayStats.pending}</span>
                <span className="stat-label">Pending</span>
              </div>
            </div>
          )}

          {userError && (
            <div className="error-banner">
              {userError}
            </div>
          )}

          {showTaskForm && (
            <TaskForm
              userId={userId}
              onTaskCreated={handleTaskCreated}
              onCancel={() => setShowTaskForm(false)}
            />
          )}

          {loading ? (
            <div className="loading">Loading tasks...</div>
          ) : (
            <>
              {pendingTasks.length > 0 && (
                <section className="tasks-section">
                  <h2>Pending Tasks</h2>
                  <div className="tasks-grid">
                    {pendingTasks.map(task => (
                      <TaskCard
                        key={task._id}
                        task={task}
                        onComplete={handleTaskComplete}
                        onDelete={handleTaskDelete}
                      />
                    ))}
                  </div>
                </section>
              )}

              {completedTasks.length > 0 && view !== 'today' && (
                <section className="tasks-section">
                  <h2>Completed Tasks</h2>
                  <div className="tasks-grid">
                    {completedTasks.map(task => (
                      <TaskCard
                        key={task._id}
                        task={task}
                      />
                    ))}
                  </div>
                </section>
              )}

              {tasks.length === 0 && (
                <div className="empty-state">
                  <p>No tasks yet. Create your first task to start leveling up!</p>
                </div>
              )}
            </>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;

