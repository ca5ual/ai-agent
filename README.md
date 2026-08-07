# What Cat Are You?

A silly personality quiz that generates a unique cartoon cat character based on your answers, with AI-generated descriptions and an interactive flip card to discover your feline archetype.

**Live Demo:** [https://backend-453621327073.europe-west1.run.app](https://backend-453621327073.europe-west1.run.app)

---

## Features

- **8-Question Personality Quiz** - Answer playful questions about yourself
- **AI-Generated Cat Characters** - Unique cartoon cat illustrations based on your answers using Gemini 3 Pro
- **Smart Archetype Matching** - Maps your answers to one of 8 cat archetypes (Rebel, Hero, Jester, Ruler, Diplomat, Creator, Dreamer, Explorer)
- **AI Descriptions** - Automatically generated personality descriptions using Gemini Flash
- **Interactive Flip Card** - 3D flip animation to reveal archetype name and description on the back
- **Asynchronous Generation** - Non-blocking image generation with real-time progress polling
- **Mobile-Optimized** - Fully responsive design with smooth animations
- **Sticker Pack Art Style** - Vibrant, satirical cartoon aesthetic (similar to Telegram/LINE stickers)

---

## Architecture

### Tech Stack

**Frontend:**
- Vanilla JavaScript (HTML5, CSS3)
- 3D CSS transforms for flip card animation
- Responsive design with viewport-fit support

**Backend:**
- Python 3.11+
- FastAPI (async REST API)
- Google ADK (Agent Development Kit) for conversational AI
- Google Cloud Run (serverless execution)

**AI/ML:**
- Google Gemini Flash Latest (conversational agent, descriptions)
- Google Gemini 3 Pro (image generation only)

### System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Browser                              │
├─────────────────────────────────────────────────────────────────┤
│  HTML + CSS                                   │
│  Vanilla JavaScript (Polling, Animations)                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                     HTTP/REST API
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    FastAPI Backend                              │
│              (Cloud Run, europe-west1)                          │
├─────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │  /api/session/start      → Greet user, get Q1             │ │
│ │  /api/chat               → Process answer, get next Q       │ │
│ │  /api/generation/{id}    → Poll image generation status    │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
    ┌──────▼──────┐   ┌─────▼─────┐   ┌──────▼──────┐
    │  Google ADK │   │   Gemini  │   │   Cloud    │
    │   (Agent)   │   │  (Image & │   │  Storage   │
    │             │   │   Text)   │   │  (Images)  │
    └─────────────┘   └───────────┘   └────────────┘
```

### Component Overview

**Frontend (index.html)**
- Quiz UI with chatbot-like interface
- Flip card animation with 3D transforms
- Real-time polling for image generation status
- Mobile-friendly touch interactions

**Backend (FastAPI)**

| File | Purpose |
|------|---------|
| `main.py` | REST API endpoints, session management |
| `agent.py` | ADK agent configuration, system prompts |
| `tools.py` | Image generation logic, archetype matching, description generation |
| `data.py` | Quiz questions, archetype prompts, design blocks |

**Google Cloud Integration**
- **Gemini 3 Pro**: High-quality cartoon cat image generation
- **Gemini Flash**: Fast personality description generation
- **Cloud Storage**: Persistent image hosting with public URLs
- **Cloud Run**: Serverless backend execution

---

## How It Works

### 1. Quiz Flow

```
Start
  ↓
Agent greets user (Q1 displayed)
  ↓
User answers A-H (picks personality option)
  ↓
Panel gets scratched by paw animation
  ↓
Agent reacts with short comment, displays Q2
  ↓
[Repeat for Q3-Q8]
  ↓
After Q8 answer:
  - Agent calls generate_cat_image() tool
  - Tool returns {status: "generating", generation_id: "xxx"}
  - Agent STOPS (doesn't write commentary)
  ↓
Frontend begins polling /api/generation/{generation_id}
  ↓
Backend generates image in background (1-2 min)
  ↓
Backend generates AI description
  ↓
Frontend gets {status: "success", image_url, archetype, description}
  ↓
Stamp falls from top, lands with animation + screen shake
  ↓
Card shows image (front), user can click to flip
  ↓
Back shows archetype name + AI-generated personality description
```

### 2. Archetype Matching Algorithm

Each quiz question has 8 options (A-H), each mapped to one archetype:

```python
QUESTIONS[0] = {
    "A": {"archetype": "rebel", ...},
    "B": {"archetype": "hero", ...},
    "C": {"archetype": "jester", ...},
    ...
}
```

**Scoring:**
1. Sum points for each archetype across all 8 answers
2. Archetype with highest score wins
3. If tied, randomly pick from tied archetypes

**Result:** One of 8 archetypes

```
- rebel    → Independent, rule-breaking
- hero     → Brave, self-sacrificing
- jester   → Funny, deflecting
- ruler    → Organized, controlling
- diplomat → Peaceful, anxious
- creator  → Imaginative, blocked
- dreamer  → Idealistic, unbothered
- explorer → Adventurous, reckless
```

### 3. Image Generation (Asynchronous)

**Why async?**
- Image generation via Gemini 3 Pro takes 30-120 seconds
- Without async, browser would timeout (default ~30s)
- Solution: Return `generation_id` immediately, poll for completion

**Process:**

```
POST /api/chat with Q8 answer
  ↓
Agent calls generate_cat_image()
  ↓
Tool acquires semaphore (max 3 concurrent)
  ↓
Tool spawns background thread with _generate_image_background()
  ↓
Immediately returns {status: "generating", generation_id}
  ↓
Background thread:
  - Calls Gemini 3 Pro with enhanced prompt
  - Saves image to Cloud Storage
  - Calls Gemini Flash for description
  - Updates _generation_tasks[generation_id] with final result
  - Releases semaphore
```

**Prompts are reinforced at 3 levels to prevent multiple cats:**
1. **BLOCK_1**: "GENERATE ONLY ONE CAT — NO DUPLICATES"
2. **ARCHETYPE_PROMPTS**: "THIS IS A SINGLE [TYPE] CAT — ONE CAT ONLY"
3. **tools.py enhanced_prompt**: "CRITICAL: There must be ONLY ONE cat"

### 4. Flip Card Interaction
**CSS 3D Transform:**
```css
.stamp-card {
  transform-style: preserve-3d;
  transition: transform 0.6s ease;
}
.stamp-card.flipped {
  transform: rotateY(180deg);
}
```

**Front:** Cat image in decorated stamp box
**Back:** Archetype name + AI description + "Click to flip" hint

---

## 📋 API Endpoints

### POST `/api/session/start`
Start a new quiz session.

**Response:**
```json
{
  "session_id": "abc-123-def",
  "reply": "Ready to find out?\n\nA) Finally! I do it my way\nB) I take it and finish it..."
}
```

### POST `/api/chat`
Send user's answer to the quiz.

**Request:**
```json
{
  "session_id": "abc-123-def",
  "message": "A"
}
```

**Response:**
```json
{
  "reply": "Nice choice!\n\nQuestion 2: People around you start arguing...",
  "generation_id": null
}
```

Or (on question 8):
```json
{
  "reply": "",
  "generation_id": "xyz-789-uvw"
}
```

### GET `/api/generation/{generation_id}`
Poll for image generation status.

**Response (generating):**
```json
{
  "status": "generating",
  "archetype": null,
  "image_url": null,
  "description": null,
  "message": null
}
```

**Response (success):**
```json
{
  "status": "success",
  "archetype": "rebel",
  "image_url": "https://storage.googleapis.com/ai-cats.../cat_rebel_1234567890.png",
  "description": "You're independent, rule-breaking, and secretly anxious...",
  "message": null
}
```

**Response (error):**
```json
{
  "status": "error",
  "archetype": null,
  "image_url": null,
  "description": null,
  "message": "Quota exhausted, try again in 2 minutes"
}
```

### GET `/api/health`
Health check.

**Response:**
```json
{"status": "ok"}
```

---