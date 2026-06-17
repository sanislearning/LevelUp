// Stat icon mappings using emojis
export const STAT_ICONS = {
  strength: '💪',
  stamina: '🫁',
  mind: '🧠',
  discipline: '🧘',
  selfCare: '❤️',
  social: '🗣️'
};

export const STAT_NAMES = {
  strength: 'Strength',
  stamina: 'Stamina',
  mind: 'Mind',
  discipline: 'Discipline',
  selfCare: 'Self-Care',
  social: 'Social'
};

export const STAT_COLORS = {
  strength: '#ef4444',
  stamina: '#f59e0b',
  mind: '#8b5cf6',
  discipline: '#3b82f6',
  selfCare: '#ec4899',
  social: '#10b981'
};

export const DIFFICULTY_COLORS = {
  easy: '#10b981',
  medium: '#f59e0b',
  hard: '#ef4444'
};

export const getStatIcon = (stat) => STAT_ICONS[stat] || '⭐';
export const getStatName = (stat) => STAT_NAMES[stat] || stat;
export const getStatColor = (stat) => STAT_COLORS[stat] || '#6b7280';
export const getDifficultyColor = (difficulty) => DIFFICULTY_COLORS[difficulty] || '#6b7280';

