import React, { useState } from 'react';
import { taskAPI } from '../services/api';
import { getStatIcon, getStatName, STAT_NAMES } from '../utils/statIcons';

const TaskForm = ({ userId, onTaskCreated, onCancel }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isClassifying, setIsClassifying] = useState(false);
  const [classification, setClassification] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleClassify = async () => {
    if (!title.trim()) {
      alert('Please enter a task title');
      return;
    }

    setIsClassifying(true);
    try {
      const response = await taskAPI.classify(title);
      setClassification(response.data.classification);
    } catch (error) {
      console.error('Classification error:', error);
      alert('Failed to classify task. Please try again.');
    } finally {
      setIsClassifying(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!classification) {
      alert('Please classify the task first');
      return;
    }

    setIsSubmitting(true);
    try {
      const taskData = {
        userId,
        title: title.trim(),
        description: description.trim(),
        primaryStat: classification.primary_stat,
        secondaryStat: classification.secondary_stat,
        difficulty: classification.difficulty,
        effortScore: classification.effort_score,
        aiClassification: {
          confidence: classification.confidence,
          reasoning: classification.reasoning,
          wasEdited: false
        }
      };

      await taskAPI.create(taskData);
      
      // Reset form
      setTitle('');
      setDescription('');
      setClassification(null);
      
      if (onTaskCreated) {
        onTaskCreated();
      }
    } catch (error) {
      console.error('Task creation error:', error);
      alert('Failed to create task. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleStatChange = (field, value) => {
    setClassification({
      ...classification,
      [field]: value,
      wasEdited: true
    });
  };

  return (
    <div className="task-form">
      <h3>Create New Task</h3>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Task Title *</label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="e.g., Go for a 5km run"
            required
            disabled={isClassifying || isSubmitting}
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Description (optional)</label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add more details..."
            rows="3"
            disabled={isClassifying || isSubmitting}
          />
        </div>

        {!classification && (
          <button
            type="button"
            onClick={handleClassify}
            disabled={isClassifying || !title.trim()}
            className="btn btn-classify"
          >
            {isClassifying ? '🤖 Classifying...' : '🤖 Classify with AI'}
          </button>
        )}

        {classification && (
          <div className="classification-result">
            <h4>AI Classification</h4>
            
            {classification.reasoning && (
              <div className="ai-reasoning">
                <strong>Reasoning:</strong> {classification.reasoning}
              </div>
            )}

            <div className="form-group">
              <label>Primary Stat</label>
              <select
                value={classification.primary_stat}
                onChange={(e) => handleStatChange('primary_stat', e.target.value)}
                disabled={isSubmitting}
              >
                {Object.keys(STAT_NAMES).map(stat => (
                  <option key={stat} value={stat}>
                    {getStatIcon(stat)} {getStatName(stat)}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Secondary Stat (optional)</label>
              <select
                value={classification.secondary_stat || ''}
                onChange={(e) => handleStatChange('secondary_stat', e.target.value || null)}
                disabled={isSubmitting}
              >
                <option value="">None</option>
                {Object.keys(STAT_NAMES).map(stat => (
                  <option key={stat} value={stat}>
                    {getStatIcon(stat)} {getStatName(stat)}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Difficulty</label>
              <select
                value={classification.difficulty}
                onChange={(e) => handleStatChange('difficulty', e.target.value)}
                disabled={isSubmitting}
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>

            <div className="form-group">
              <label>Effort Score (1-10)</label>
              <input
                type="number"
                min="1"
                max="10"
                value={classification.effort_score}
                onChange={(e) => handleStatChange('effort_score', parseInt(e.target.value))}
                disabled={isSubmitting}
              />
            </div>

            <div className="xp-preview">
              <strong>XP Reward:</strong> {classification.xpReward}
            </div>

            <div className="form-actions">
              <button
                type="submit"
                disabled={isSubmitting}
                className="btn btn-primary"
              >
                {isSubmitting ? 'Creating...' : '✓ Create Task'}
              </button>
              <button
                type="button"
                onClick={() => setClassification(null)}
                disabled={isSubmitting}
                className="btn btn-secondary"
              >
                ← Reclassify
              </button>
              {onCancel && (
                <button
                  type="button"
                  onClick={onCancel}
                  disabled={isSubmitting}
                  className="btn btn-cancel"
                >
                  Cancel
                </button>
              )}
            </div>
          </div>
        )}
      </form>
    </div>
  );
};

export default TaskForm;

// Made with Bob
