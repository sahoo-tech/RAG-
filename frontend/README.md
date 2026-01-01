# RAG++ Cosmic Frontend

A stunning universe-themed frontend for the RAG++ Analytical Reasoning Engine with animated solar system, space background, and seamless backend integration.

## Features

### 🌌 Visual Design
- **Animated Space Background** with twinkling stars and nebula effects
- **Rotating Solar System** with orbiting planets
- **Cosmic Theme** with gradients, glows, and particle effects
- **Smooth Animations** for all interactions
- **Responsive Design** works on all screen sizes

### 🚀 Functionality
- **Real-time Backend Connection** with health status indicator
- **Query Interface** with quick suggestion chips
- **Live Processing Animation** showing multi-agent reasoning steps
- **Confidence Visualization** with animated meter and detailed stats
- **Explainability View** showing complete reasoning process
- **Error Handling** with user-friendly messages

### 🎨 Interactive Elements
- Particle effects on mouse movement
- Glowing buttons and inputs
- Animated loading states
- Smooth scroll to results
- Keyboard shortcuts (Ctrl+Enter to submit)

## Setup

### 1. Ensure Backend is Running

```bash
cd backend
python main.py
```

The backend should be running on `http://localhost:8000`

### 2. Open Frontend

Simply open `index.html` in your web browser:

```bash
# Option 1: Double-click index.html

# Option 2: Use a local server (recommended)
python -m http.server 3000
# Then visit http://localhost:3000
```

### 3. Start Querying!

The frontend will automatically connect to the backend and show connection status in the header.

## Usage

### Quick Start
1. Enter your analytical query in the text area
2. Optionally enable "Include Explainability" for detailed reasoning
3. Click "Analyze" or press Ctrl+Enter
4. Watch the cosmic loading animation
5. View your results with confidence scores and evidence

### Example Queries
Click on the suggestion chips or try:
- "What is the trend in revenue over the last quarter?"
- "Compare customer retention between enterprise and consumer segments"
- "Show me user engagement breakdown by segment"

### Explainability Mode
Enable the checkbox to see:
- Query decomposition steps
- Evidence collection details
- Agent execution timeline
- Validation results
- Complete reasoning process

## Files

- `index.html` - Main HTML structure
- `styles.css` - Cosmic theme and animations
- `script.js` - Backend integration and interactivity

## Customization

### Change Colors
Edit CSS variables in `styles.css`:
```css
:root {
    --primary-color: #00d4ff;    /* Cyan */
    --secondary-color: #ff00ff;  /* Magenta */
    --accent-color: #ffaa00;     /* Orange */
}
```

### Adjust Animations
Modify animation durations in `styles.css`:
```css
.orbit-1 { animation: rotate 10s linear infinite; }
```

### Backend URL
Change API endpoint in `script.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## Browser Compatibility

Works best in modern browsers:
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ⚠️ IE11 (limited support)

## Performance

- Optimized animations using CSS transforms
- Efficient particle system with cleanup
- Lazy loading of results
- Minimal JavaScript overhead

## Troubleshooting

**Issue**: "Disconnected" status
**Solution**: Ensure backend is running on port 8000

**Issue**: Slow animations
**Solution**: Reduce particle effects or disable in `script.js`

**Issue**: CORS errors
**Solution**: Backend includes CORS headers, but use same origin if possible

## Credits

- Fonts: Google Fonts (Orbitron, Space Grotesk)
- Icons: Custom SVG
- Animations: Pure CSS
- Backend: RAG++ Analytical Reasoning Engine

---

**Enjoy exploring the cosmos of analytical reasoning! 🌌✨**
