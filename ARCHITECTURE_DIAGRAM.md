# 🏗️ LevelUp System Architecture

## System Overview

```mermaid
graph TB
    subgraph "Frontend - React"
        UI[User Interface]
        TaskForm[Task Form]
        StatsPanel[Stats Panel]
        ChallengeModal[Challenge Modal]
        ChallengeTracker[Challenge Tracker]
    end
    
    subgraph "Backend - FastAPI"
        API[API Gateway]
        UserRoutes[User Routes]
        TaskRoutes[Task Routes]
        ChallengeRoutes[Challenge Routes]
    end
    
    subgraph "Services"
        AIService[AI Service - Claude]
        XPCalc[XP Calculator]
        ChallengeGen[Challenge Generator]
        TitleSystem[Title System]
    end
    
    subgraph "Database - MongoDB"
        Users[(Users)]
        Tasks[(Tasks)]
        Challenges[(Challenges)]
    end
    
    UI --> API
    TaskForm --> API
    StatsPanel --> API
    ChallengeModal --> API
    ChallengeTracker --> API
    
    API --> UserRoutes
    API --> TaskRoutes
    API --> ChallengeRoutes
    
    UserRoutes --> Users
    TaskRoutes --> Tasks
    TaskRoutes --> AIService
    TaskRoutes --> XPCalc
    ChallengeRoutes --> Challenges
    ChallengeRoutes --> ChallengeGen
    
    ChallengeGen --> AIService
    XPCalc --> TitleSystem
```

## Data Flow: Task Completion with Challenge System

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant TaskAPI
    participant XPCalc
    participant ChallengeAPI
    participant Database
    
    User->>Frontend: Complete Task
    Frontend->>TaskAPI: POST /tasks/:id/complete
    TaskAPI->>Database: Get Task & User
    TaskAPI->>XPCalc: Calculate XP Distribution
    TaskAPI->>Database: Update User Stats
    
    alt Level-Up Available
        TaskAPI->>XPCalc: Check Level-Up Status
        XPCalc-->>TaskAPI: canLevelUp: true
        TaskAPI->>Database: Set pendingLevelUp: true
        TaskAPI-->>Frontend: Level-Up Available!
        Frontend->>User: Show Level-Up Button
    end
    
    alt Active Challenge Exists
        TaskAPI->>Database: Get Active Challenges
        TaskAPI->>ChallengeAPI: Update Challenge Progress
        ChallengeAPI->>Database: Update Progress
        
        alt Challenge Complete
            ChallengeAPI->>Database: Level Up Stat
            ChallengeAPI->>Database: Mark Challenge Complete
            ChallengeAPI-->>Frontend: Challenge Complete!
            Frontend->>User: Show Success Animation
        end
    end
    
    TaskAPI-->>Frontend: Task Complete Response
    Frontend->>User: Show XP Gained
```

## Challenge System Flow

```mermaid
stateDiagram-v2
    [*] --> XPAccumulating: User completes tasks
    XPAccumulating --> LevelUpAvailable: XP threshold reached
    LevelUpAvailable --> ViewingChallenges: User clicks Level Up
    ViewingChallenges --> ChallengeGeneration: Request challenges
    
    ChallengeGeneration --> AIGeneration: Try AI first
    AIGeneration --> TemplateGeneration: AI fails
    AIGeneration --> PresentOptions: AI succeeds
    TemplateGeneration --> PresentOptions: Use templates
    
    PresentOptions --> ChallengeAccepted: User selects challenge
    ChallengeAccepted --> InProgress: Challenge starts
    
    InProgress --> TrackingProgress: User completes tasks
    TrackingProgress --> InProgress: Progress updated
    TrackingProgress --> ChallengeComplete: Requirements met
    TrackingProgress --> ChallengeFailed: Expired/abandoned
    
    ChallengeComplete --> LevelUp: Award level
    LevelUp --> [*]: Return to XP accumulating
    
    ChallengeFailed --> LevelUpAvailable: Can retry
```

## Database Schema

```mermaid
erDiagram
    USER ||--o{ TASK : creates
    USER ||--o{ CHALLENGE : has
    USER {
        ObjectId _id
        string name
        string email
        int totalXP
        int level
        object stats
        object streak
        array activeChallenges
        int completedChallenges
        datetime createdAt
    }
    
    TASK {
        ObjectId _id
        string userId
        string title
        string description
        string primaryStat
        string secondaryStat
        string difficulty
        int effortScore
        int xpReward
        bool completed
        datetime completedAt
        object aiClassification
        datetime createdAt
    }
    
    CHALLENGE {
        ObjectId _id
        string userId
        string stat
        int fromLevel
        int toLevel
        string type
        string title
        string description
        object requirements
        string status
        object progress
        datetime startedAt
        datetime completedAt
        datetime expiresAt
        bool aiGenerated
        string reasoning
    }
    
    STATS {
        int xp
        int level
        bool pendingLevelUp
        string currentChallenge
    }
    
    USER ||--|| STATS : has_six
```

## Component Hierarchy

```mermaid
graph TD
    App[App.jsx]
    App --> Header[Header]
    App --> Sidebar[Sidebar]
    App --> MainContent[Main Content]
    
    Sidebar --> StatsPanel[StatsPanel.jsx]
    StatsPanel --> StatItem[Stat Item]
    StatItem --> LevelUpButton[Level Up Button]
    StatItem --> ProgressBar[Progress Bar]
    
    MainContent --> ViewTabs[View Tabs]
    MainContent --> TaskForm[TaskForm.jsx]
    MainContent --> TaskList[Task List]
    TaskList --> TaskCard[TaskCard.jsx]
    
    App --> ChallengeModal[ChallengeModal.jsx]
    ChallengeModal --> ChallengeOption[Challenge Option]
    
    Sidebar --> ChallengeTracker[ChallengeTracker.jsx]
    ChallengeTracker --> ActiveChallenge[Active Challenge]
    ActiveChallenge --> ChallengeProgress[Challenge Progress]
```

## API Endpoints Structure

```mermaid
graph LR
    subgraph "User Endpoints"
        U1[POST /api/users]
        U2[GET /api/users/:id]
        U3[GET /api/users/:id/stats]
        U4[PUT /api/users/:id]
    end
    
    subgraph "Task Endpoints"
        T1[POST /api/tasks/classify]
        T2[POST /api/tasks]
        T3[GET /api/tasks/user/:userId]
        T4[GET /api/tasks/user/:userId/today]
        T5[POST /api/tasks/:id/complete]
        T6[PUT /api/tasks/:id]
        T7[DELETE /api/tasks/:id]
    end
    
    subgraph "Challenge Endpoints NEW"
        C1[POST /api/challenges/generate]
        C2[POST /api/challenges/accept]
        C3[POST /api/challenges/:id/progress]
        C4[GET /api/challenges/user/:userId/active]
        C5[GET /api/challenges/:id]
    end
```

## XP Calculation Flow

```mermaid
flowchart TD
    Start[Task Completed] --> GetTask[Get Task Details]
    GetTask --> CalcBase[Base XP from Difficulty]
    CalcBase --> CalcEffort[Add Effort Bonus]
    CalcEffort --> TotalXP[Total Task XP]
    
    TotalXP --> Distribute{Has Secondary Stat?}
    Distribute -->|Yes| Split80_20[80% Primary, 20% Secondary]
    Distribute -->|No| All100[100% Primary]
    
    Split80_20 --> UpdateStats[Update Stat XP]
    All100 --> UpdateStats
    
    UpdateStats --> CheckLevel{XP >= Threshold?}
    CheckLevel -->|Yes| MarkPending[Mark pendingLevelUp: true]
    CheckLevel -->|No| Done[Done]
    
    MarkPending --> NotifyUser[Notify User]
    NotifyUser --> Done
    
    style MarkPending fill:#ff9
    style NotifyUser fill:#9f9
```

## Challenge Progress Tracking

```mermaid
flowchart TD
    TaskComplete[Task Completed] --> GetChallenges[Get Active Challenges]
    GetChallenges --> FilterStat{Challenge Stat Matches?}
    
    FilterStat -->|Yes| CheckType{Challenge Type?}
    FilterStat -->|No| Skip[Skip Update]
    
    CheckType -->|Single Session| UpdateCount[Update Count]
    CheckType -->|Multi-Day| UpdateFrequency[Update Frequency]
    CheckType -->|Consistency| UpdateStreak[Update Streak]
    
    UpdateCount --> CheckComplete{Requirements Met?}
    UpdateFrequency --> CheckComplete
    UpdateStreak --> CheckComplete
    
    CheckComplete -->|Yes| LevelUp[Level Up Stat]
    CheckComplete -->|No| SaveProgress[Save Progress]
    
    LevelUp --> MarkComplete[Mark Challenge Complete]
    MarkComplete --> Celebrate[Show Success]
    SaveProgress --> UpdateUI[Update UI]
    
    style LevelUp fill:#9f9
    style Celebrate fill:#9f9
```

## Title System Logic

```mermaid
flowchart LR
    Level[User Level] --> CheckGlobal{Check Global Titles}
    CheckGlobal --> GlobalTitle[Assign Global Title]
    
    StatLevel[Stat Level] --> CheckStat{Check Stat Titles}
    CheckStat --> StatTitle[Assign Stat Title]
    
    GlobalTitle --> Display[Display in UI]
    StatTitle --> Display
    
    subgraph "Global Titles"
        G1[1: Beginner]
        G2[5: Apprentice]
        G3[10: Disciplined]
        G4[20: Elite]
        G5[50: Ascended]
    end
    
    subgraph "Stat-Specific Titles"
        S1[Strength: Iron Trained → Peak Condition]
        S2[Mind: Quick Learner → Brilliant]
        S3[Discipline: Consistent → Master of Self]
    end
```

---

## Key Design Decisions

### 1. Level Gating Mechanism
- XP accumulates normally
- Level-up **requires** challenge completion
- Prevents passive progression
- Creates meaningful milestones

### 2. Challenge Types
- **Single Session**: Complete in one go
- **Multi-Day**: Frequency over time period
- **Consistency**: Maintain streaks

### 3. AI Integration Points
- Task classification (existing)
- Challenge generation (new)
- Fallback to templates if AI fails

### 4. Progress Tracking
- Real-time challenge progress updates
- Automatic detection when tasks contribute to challenges
- Clear visual feedback in UI

### 5. Data Integrity
- Completed tasks cannot be deleted (preserve XP history)
- Challenges have expiration dates
- Failed challenges can be retried

---

## Performance Considerations

### Caching Strategy
- Cache AI-generated challenges for similar level-ups
- Cache title lookups
- Minimize database queries with aggregation

### Scalability
- Index on userId + status for challenges
- Index on stat + level for quick lookups
- Paginate task lists

### Error Handling
- Graceful AI fallback to templates
- Transaction-like updates for level-ups
- Rollback capability for failed operations

---

**This architecture supports the production-grade LevelUp system with robust challenge mechanics and scalable design.**