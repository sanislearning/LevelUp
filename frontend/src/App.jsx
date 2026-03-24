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

  // For demo purposes, using a hardcoded user ID
  // In production, this would come from authentication
  const DEMO_USER_ID = '6789abcdef123456'; // Replace with actual user ID after creating user

  useEffect(() => {
    loadUserData();
    loadTasks();
  }, [view]);

  const loadUserData = async () => {
    try {
      const response = await userAPI.getById(DEMO_USER_ID);
      setUser(response.data.user);
    } catch (error) {
      console.error('Error loading user:', error);
      // If user doesn't exist, you might want to create one
      if (error.response?.status === 404) {
        console.log('User not found. Please create a user first.');
      }
    }
  };

  const loadTasks = async () => {
    setLoading(true);
    try {
      let response;
      if (view === 'today') {
        response = await taskAPI.getTodayTasks(DEMO_USER_ID);
        setTodayStats({
          completed: response.data.completed,
          pending: response.data.pending
        });
      } else {
        const params = view === 'completed' ? { completed: true } : {};
        response = await taskAPI.getByUser(DEMO_USER_ID, params);
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

  return (
    <div className="app">
      <header className="app-header">
        <h1>⚔️ LevelUp</h1>
        <p className="tagline">Your Life is an RPG</p>
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
                📅 Today
              </button>
              <button
                className={`tab ${view === 'all' ? 'active' : ''}`}
                onClick={() => setView('all')}
              >
                📋 All Tasks
              </button>
              <button
                className={`tab ${view === 'completed' ? 'active' : ''}`}
                onClick={() => setView('completed')}
              >
                ✓ Completed
              </button>
            </div>

            <button
              className="btn btn-primary btn-add-task"
              onClick={() => setShowTaskForm(!showTaskForm)}
            >
              {showTaskForm ? '✕ Cancel' : '+ New Task'}
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

          {showTaskForm && (
            <TaskForm
              userId={DEMO_USER_ID}
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

// Made with Bob
