import React from 'react';
import { getStatIcon, getStatName, getStatColor } from '../utils/statIcons';

const StatsPanel = ({ user }) => {
  if (!user) return null;

  const stats = user.stats || {};
  const statsArray = Object.entries(stats).map(([name, data]) => ({
    name,
    ...data
  }));

  // Sort by level descending
  statsArray.sort((a, b) => b.level - a.level);

  return (
    <div className="stats-panel">
      <div className="user-header">
        <h2>{user.name}</h2>
        <div className="user-level">
          <span className="level-label">Level</span>
          <span className="level-value">{user.level}</span>
        </div>
        {user.title && (
          <div className="user-title">{user.title}</div>
        )}
      </div>

      <div className="global-xp">
        <div className="xp-label">Total XP</div>
        <div className="xp-value">{user.totalXP?.toLocaleString()}</div>
        {user.levelInfo && (
          <div className="xp-progress">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${user.levelInfo.progress}%` }}
              />
            </div>
            <div className="progress-text">
              {user.levelInfo.currentLevelXP} / {user.levelInfo.xpForNextLevel} XP
            </div>
          </div>
        )}
      </div>

      {user.streak && user.streak.current > 0 && (
        <div className="streak-display">
          <span className="streak-icon">🔥</span>
          <span className="streak-value">{user.streak.current}</span>
          <span className="streak-label">day streak</span>
          {user.streak.longest > user.streak.current && (
            <span className="streak-best">(Best: {user.streak.longest})</span>
          )}
        </div>
      )}

      <div className="stats-grid">
        {statsArray.map(stat => (
          <div key={stat.name} className="stat-item">
            <div className="stat-header">
              <span 
                className="stat-icon-large" 
                style={{ color: getStatColor(stat.name) }}
              >
                {getStatIcon(stat.name)}
              </span>
              <div className="stat-info">
                <div className="stat-name">{getStatName(stat.name)}</div>
                <div className="stat-level">Level {stat.level}</div>
              </div>
            </div>
            <div className="stat-xp">{stat.xp} XP</div>
            {stat.progress !== undefined && (
              <div className="stat-progress">
                <div className="progress-bar">
                  <div 
                    className="progress-fill" 
                    style={{ 
                      width: `${stat.progress}%`,
                      backgroundColor: getStatColor(stat.name)
                    }}
                  />
                </div>
                <div className="progress-text">{stat.progress}%</div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default StatsPanel;

