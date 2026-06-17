# 🎨 LevelUp UI Design Guide

## Design Philosophy

**Clean, Clear, Minimal** - No gradients, no blur effects, no glassmorphism. Focus on clarity, readability, and purposeful design.

---

## Color Palette

### Primary Colors
```css
--primary: #2563eb;        /* Blue - primary actions */
--primary-dark: #1e40af;   /* Darker blue - hover states */
--primary-light: #dbeafe;  /* Light blue - backgrounds */
```

### Neutral Colors
```css
--gray-50: #f9fafb;        /* Lightest gray - page background */
--gray-100: #f3f4f6;       /* Light gray - card backgrounds */
--gray-200: #e5e7eb;       /* Border color */
--gray-300: #d1d5db;       /* Disabled states */
--gray-600: #4b5563;       /* Secondary text */
--gray-900: #111827;       /* Primary text */
```

### Stat Colors (Flat, No Gradients)
```css
--strength: #ef4444;       /* Red */
--stamina: #f59e0b;        /* Orange */
--mind: #8b5cf6;           /* Purple */
--discipline: #3b82f6;     /* Blue */
--self-care: #10b981;      /* Green */
--social: #ec4899;         /* Pink */
```

### Status Colors
```css
--success: #10b981;        /* Green */
--warning: #f59e0b;        /* Orange */
--error: #ef4444;          /* Red */
--info: #3b82f6;           /* Blue */
```

---

## Typography

### Font Stack
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 
             'Helvetica Neue', Arial, sans-serif;
```

### Font Sizes
```css
--text-xs: 0.75rem;    /* 12px - labels */
--text-sm: 0.875rem;   /* 14px - secondary text */
--text-base: 1rem;     /* 16px - body text */
--text-lg: 1.125rem;   /* 18px - emphasis */
--text-xl: 1.25rem;    /* 20px - card titles */
--text-2xl: 1.5rem;    /* 24px - section headers */
--text-3xl: 1.875rem;  /* 30px - page titles */
```

### Font Weights
```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

---

## Spacing System

```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
```

---

## Component Styles

### Cards
```css
.card {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: var(--space-6);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s ease;
}
```

### Buttons
```css
/* Primary Button */
.btn-primary {
  background: var(--primary);
  color: white;
  border: none;
  padding: var(--space-3) var(--space-6);
  border-radius: 6px;
  font-weight: var(--font-medium);
  cursor: pointer;
}

.btn-primary:hover {
  background: var(--primary-dark);
}

/* Secondary Button */
.btn-secondary {
  background: white;
  color: var(--gray-900);
  border: 1px solid var(--gray-200);
  padding: var(--space-3) var(--space-6);
  border-radius: 6px;
  font-weight: var(--font-medium);
  cursor: pointer;
}

.btn-secondary:hover {
  background: var(--gray-50);
}

/* Icon Button */
.btn-icon {
  background: transparent;
  border: none;
  padding: var(--space-2);
  cursor: pointer;
  color: var(--gray-600);
}

.btn-icon:hover {
  color: var(--gray-900);
}
```

### Progress Bars
```css
.progress-bar {
  width: 100%;
  height: 8px;
  background: var(--gray-200);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--primary);
  transition: width 0.3s ease;
}

/* Stat-specific progress bars */
.progress-fill.strength { background: var(--strength); }
.progress-fill.stamina { background: var(--stamina); }
.progress-fill.mind { background: var(--mind); }
.progress-fill.discipline { background: var(--discipline); }
.progress-fill.self-care { background: var(--self-care); }
.progress-fill.social { background: var(--social); }
```

### Badges
```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-3);
  border-radius: 12px;
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
}

.badge-primary {
  background: var(--primary-light);
  color: var(--primary);
}

.badge-success {
  background: #d1fae5;
  color: var(--success);
}

.badge-warning {
  background: #fef3c7;
  color: var(--warning);
}
```

---

## Layout Examples

### Page Layout
```css
body {
  background: var(--gray-50);
  color: var(--gray-900);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}

.app-header {
  background: white;
  border-bottom: 1px solid var(--gray-200);
  padding: var(--space-6) var(--space-8);
}

.app-container {
  display: flex;
  max-width: 1400px;
  margin: 0 auto;
  gap: var(--space-8);
  padding: var(--space-8);
}

.sidebar {
  flex: 0 0 350px;
}

.main-content {
  flex: 1;
}
```

### Stats Panel
```css
.stats-panel {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: var(--space-6);
}

.stat-item {
  padding: var(--space-4);
  border: 1px solid var(--gray-200);
  border-radius: 6px;
  margin-bottom: var(--space-3);
}

.stat-item:hover {
  border-color: var(--primary);
  background: var(--gray-50);
}

.stat-icon {
  font-size: var(--text-2xl);
  /* Use flat colors, no gradients */
}

.stat-name {
  font-weight: var(--font-semibold);
  color: var(--gray-900);
}

.stat-level {
  font-size: var(--text-sm);
  color: var(--gray-600);
}
```

### Task Card
```css
.task-card {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: var(--space-5);
  margin-bottom: var(--space-4);
}

.task-card.completed {
  background: var(--gray-50);
  opacity: 0.7;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-3);
}

.task-stat {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.task-difficulty {
  font-size: var(--text-xs);
  font-weight: var(--font-semibold);
  padding: var(--space-1) var(--space-2);
  border-radius: 4px;
}

.task-difficulty.easy {
  background: #d1fae5;
  color: var(--success);
}

.task-difficulty.medium {
  background: #fef3c7;
  color: var(--warning);
}

.task-difficulty.hard {
  background: #fee2e2;
  color: var(--error);
}
```

### Challenge Modal
```css
.challenge-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 12px;
  padding: var(--space-8);
  max-width: 600px;
  width: 90%;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.challenge-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.challenge-option {
  border: 2px solid var(--gray-200);
  border-radius: 8px;
  padding: var(--space-5);
  margin-bottom: var(--space-4);
  cursor: pointer;
}

.challenge-option:hover {
  border-color: var(--primary);
  background: var(--gray-50);
}

.challenge-option.selected {
  border-color: var(--primary);
  background: var(--primary-light);
}
```

### Challenge Tracker
```css
.challenge-tracker {
  background: white;
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: var(--space-6);
  margin-top: var(--space-6);
}

.active-challenge {
  border-left: 4px solid var(--primary);
  padding: var(--space-4);
  background: var(--gray-50);
  border-radius: 4px;
  margin-bottom: var(--space-4);
}

.challenge-progress {
  margin: var(--space-3) 0;
}

.challenge-expires {
  font-size: var(--text-sm);
  color: var(--gray-600);
}
```

---

## Level-Up Indicator

```css
.level-up-available {
  position: relative;
}

.level-up-available::after {
  content: '';
  position: absolute;
  top: -4px;
  right: -4px;
  width: 12px;
  height: 12px;
  background: var(--success);
  border-radius: 50%;
  border: 2px solid white;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.level-up-button {
  background: var(--success);
  color: white;
  border: none;
  padding: var(--space-2) var(--space-4);
  border-radius: 6px;
  font-weight: var(--font-semibold);
  font-size: var(--text-sm);
  cursor: pointer;
  width: 100%;
  margin-top: var(--space-3);
}

.level-up-button:hover {
  background: #059669;
}
```

---

## Animations

### Subtle Transitions
```css
/* Use sparingly, only for interactive elements */
.transition-all {
  transition: all 0.2s ease;
}

.transition-colors {
  transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease;
}

.transition-shadow {
  transition: box-shadow 0.2s ease;
}
```

### Success Animation
```css
@keyframes success-bounce {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.success-animation {
  animation: success-bounce 0.3s ease;
}
```

---

## Responsive Design

### Breakpoints
```css
/* Mobile */
@media (max-width: 640px) {
  .app-container {
    flex-direction: column;
    padding: var(--space-4);
  }
  
  .sidebar {
    flex: 1;
  }
}

/* Tablet */
@media (max-width: 1024px) {
  .app-container {
    gap: var(--space-6);
  }
}
```

---

## Accessibility

### Focus States
```css
*:focus {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

button:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}
```

### Color Contrast
- All text must meet WCAG AA standards (4.5:1 for normal text)
- Interactive elements must be clearly distinguishable
- Use color + icon/text to convey information (not color alone)

---

## Design Principles

### 1. Clarity Over Decoration
- Remove unnecessary visual elements
- Use whitespace effectively
- Clear hierarchy through size and weight, not effects

### 2. Consistent Spacing
- Use the spacing system consistently
- Maintain visual rhythm
- Group related elements

### 3. Purposeful Color
- Use color to convey meaning
- Maintain consistency across stat colors
- Avoid color overload

### 4. Readable Typography
- Sufficient line height (1.5 for body text)
- Appropriate font sizes
- Clear hierarchy

### 5. Subtle Interactions
- Hover states for clickable elements
- Smooth transitions (200ms)
- Clear feedback for actions

---

## Implementation Notes

### Remove from Current Design
- ❌ Background gradients (`linear-gradient(135deg, #667eea 0%, #764ba2 100%)`)
- ❌ Backdrop blur effects (`backdrop-filter: blur(10px)`)
- ❌ Glassmorphism (`rgba(255, 255, 255, 0.1)`)
- ❌ Gradient text/buttons
- ❌ Heavy shadows

### Add to New Design
- ✅ Solid background colors
- ✅ Clear borders
- ✅ Subtle shadows (1-3px)
- ✅ Flat stat colors
- ✅ Clean typography
- ✅ Purposeful whitespace

---

## Example Component Updates

### Before (Gradient Style)
```css
.level-value {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
}
```

### After (Clean Style)
```css
.level-value {
  background: var(--primary);
  color: white;
  padding: var(--space-2) var(--space-4);
  border-radius: 6px;
  font-weight: var(--font-semibold);
}
```

---

**This design system creates a clean, professional interface that prioritizes clarity and usability over visual effects.**