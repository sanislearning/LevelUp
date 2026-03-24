import React from 'react';
import { getStatIcon, getStatName, getStatColor, getDifficultyColor } from '../utils/statIcons';

const TaskCard = ({ task, onComplete, onEdit, onDelete }) => {
  const handleComplete = async () => {
    if (window.confirm('Mark this task as complete?')) {
      await onComplete(task._id);
    }
  };

  return (
    <div className="task-card">
      <div className="task-header">
        <div className="task-stat">
          <span className="stat-icon" style={{ color: getStatColor(task.primaryStat) }}>
            {getStatIcon(task.primaryStat)}
          </span>
          <span className="stat-name">{getStatName(task.primaryStat)}</span>
        </div>
        <div className="task-difficulty" style={{ color: getDifficultyColor(task.difficulty) }}>
          {task.difficulty.toUpperCase()}
        </div>
      </div>

      <h3 className="task-title">{task.title}</h3>
      
      {task.description && (
        <p className="task-description">{task.description}</p>
      )}

      <div className="task-footer">
        <div className="task-xp">
          <span className="xp-label">XP:</span>
          <span className="xp-value">{task.xpReward}</span>
        </div>

        {!task.completed && (
          <div className="task-actions">
            <button onClick={handleComplete} className="btn btn-complete">
              ✓ Complete
            </button>
            {onEdit && (
              <button onClick={() => onEdit(task)} className="btn btn-edit">
                ✏️
              </button>
            )}
            {onDelete && (
              <button onClick={() => onDelete(task._id)} className="btn btn-delete">
                🗑️
              </button>
            )}
          </div>
        )}

        {task.completed && (
          <div className="task-completed">
            <span className="completed-badge">✓ Completed</span>
          </div>
        )}
      </div>

      {task.secondaryStat && (
        <div className="task-secondary-stat">
          <span className="secondary-label">Also trains:</span>
          <span className="stat-icon" style={{ color: getStatColor(task.secondaryStat) }}>
            {getStatIcon(task.secondaryStat)}
          </span>
          <span className="stat-name">{getStatName(task.secondaryStat)}</span>
        </div>
      )}
    </div>
  );
};

export default TaskCard;

// Made with Bob
