// ===== CONFIGURATION =====
const API_BASE_URL = 'http://localhost:8000';

// ===== DOM ELEMENTS =====
const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const queryInput = document.getElementById('queryInput');
const explainabilityToggle = document.getElementById('explainabilityToggle');
const submitBtn = document.getElementById('submitBtn');
const loadingContainer = document.getElementById('loadingContainer');
const processingSteps = document.getElementById('processingSteps');
const resultsSection = document.getElementById('resultsSection');
const errorContainer = document.getElementById('errorContainer');
const errorMessage = document.getElementById('errorMessage');

// Results elements
const confidenceValue = document.getElementById('confidenceValue');
const confidenceFill = document.getElementById('confidenceFill');
const coverageValue = document.getElementById('coverageValue');
const completenessValue = document.getElementById('completenessValue');
const evidenceValue = document.getElementById('evidenceValue');
const answerContent = document.getElementById('answerContent');
const explainabilitySection = document.getElementById('explainabilitySection');
const explainabilityContent = document.getElementById('explainabilityContent');
const processingTime = document.getElementById('processingTime');
const timestamp = document.getElementById('timestamp');

// Chat elements
const analyticsBtn = document.getElementById('analyticsBtn');
const chatBtn = document.getElementById('chatBtn');
const analyticsInterface = document.getElementById('analyticsInterface');
const chatInterface = document.getElementById('chatInterface');
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendChatBtn = document.getElementById('sendChatBtn');

let conversationHistory = [];

// ===== AI LOADING SCREEN =====
function initAILoadingScreen() {
    const canvas = document.getElementById('neuralCanvas');
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    const particleCount = 80;
    const connectionDistance = 150;

    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.vx = (Math.random() - 0.5) * 0.5;
            this.vy = (Math.random() - 0.5) * 0.5;
            this.radius = Math.random() * 2 + 1;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
            if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = '#00d4ff';
            ctx.shadowBlur = 10;
            ctx.shadowColor = '#00d4ff';
            ctx.fill();
        }
    }

    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }

    function drawConnections() {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < connectionDistance) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    const opacity = 1 - (distance / connectionDistance);
                    ctx.strokeStyle = `rgba(0, 212, 255, ${opacity * 0.3})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        drawConnections();

        particles.forEach(particle => {
            particle.update();
            particle.draw();
        });

        requestAnimationFrame(animate);
    }

    animate();

    setTimeout(() => {
        const loadingScreen = document.getElementById('aiLoadingScreen');
        loadingScreen.classList.add('hidden');
        setTimeout(() => {
            loadingScreen.remove();
        }, 800);
    }, 3000);
}

window.addEventListener('load', initAILoadingScreen);

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    checkServerHealth();
    setupEventListeners();

    setInterval(checkServerHealth, 30000);
});

// ===== EVENT LISTENERS =====
function setupEventListeners() {
    submitBtn.addEventListener('click', handleSubmit);

    queryInput.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 'Enter') {
            handleSubmit();
        }
    });

    document.querySelectorAll('.suggestion-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            queryInput.value = chip.dataset.query;
            queryInput.focus();
        });
    });

    analyticsBtn.addEventListener('click', () => switchMode('analytics'));
    chatBtn.addEventListener('click', () => switchMode('chat'));

    sendChatBtn.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendChatMessage();
        }
        chatInput.style.height = 'auto';
        chatInput.style.height = chatInput.scrollHeight + 'px';
    });
}

// ===== MODE SWITCHING =====
function switchMode(mode) {
    if (mode === 'analytics') {
        analyticsBtn.classList.add('active');
        chatBtn.classList.remove('active');
        analyticsInterface.style.display = 'block';
        chatInterface.style.display = 'none';
    } else {
        chatBtn.classList.add('active');
        analyticsBtn.classList.remove('active');
        chatInterface.style.display = 'block';
        analyticsInterface.style.display = 'none';
    }
}

// ===== SERVER HEALTH CHECK =====
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const data = await response.json();
            updateStatus('connected', 'Connected');
        } else {
            updateStatus('error', 'Server Error');
        }
    } catch (error) {
        updateStatus('error', 'Disconnected');
    }
}

function updateStatus(status, text) {
    statusDot.className = `status-dot ${status}`;
    statusText.textContent = text;
}

// ===== QUERY SUBMISSION =====
async function handleSubmit() {
    const query = queryInput.value.trim();

    if (!query) {
        showError('Please enter a query');
        return;
    }

    hideAll();

    loadingContainer.style.display = 'block';
    submitBtn.disabled = true;

    showProcessingSteps();

    try {
        const requestData = {
            query: query,
            include_explainability: explainabilityToggle.checked
        };

        const response = await fetch(`${API_BASE_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (data.success && data.response) {
            displayResults(data.response, data.explainability);
        } else {
            showError(data.error || 'Query processing failed');
        }
    } catch (error) {
        showError(`Connection error: ${error.message}`);
    } finally {
        loadingContainer.style.display = 'none';
        submitBtn.disabled = false;
    }
}

// ===== PROCESSING STEPS ANIMATION =====
function showProcessingSteps() {
    const steps = [
        '1. Classifying query intent...',
        '2. Decomposing into sub-questions...',
        '3. Retrieving evidence from multiple sources...',
        '4. Running multi-agent analysis...',
        '5. Validating evidence and insights...',
        '6. Computing confidence scores...',
        '7. Generating final answer...'
    ];

    processingSteps.innerHTML = '';

    steps.forEach((step, index) => {
        setTimeout(() => {
            const stepEl = document.createElement('div');
            stepEl.className = 'processing-step';
            stepEl.textContent = step;
            processingSteps.appendChild(stepEl);
        }, index * 300);
    });
}

// ===== DISPLAY RESULTS =====
function displayResults(response, explainability) {
    hideAll();
    resultsSection.style.display = 'block';

    const confidence = response.confidence;
    const confidencePercent = Math.round(confidence.overall_confidence * 100);

    confidenceValue.textContent = formatConfidenceLevel(confidence.confidence_level);
    confidenceFill.style.width = `${confidencePercent}%`;

    if (confidence.confidence_level === 'high_confidence') {
        confidenceFill.style.background = 'linear-gradient(90deg, #00ff88, #00cc66)';
        confidenceValue.style.color = '#00ff88';
    } else if (confidence.confidence_level === 'partial_evidence') {
        confidenceFill.style.background = 'linear-gradient(90deg, #ffaa00, #ff8800)';
        confidenceValue.style.color = '#ffaa00';
    } else {
        confidenceFill.style.background = 'linear-gradient(90deg, #ff3366, #cc0044)';
        confidenceValue.style.color = '#ff3366';
    }

    coverageValue.textContent = `${Math.round(confidence.coverage_score * 100)}%`;
    completenessValue.textContent = `${Math.round(confidence.completeness_score * 100)}%`;
    evidenceValue.textContent = response.evidence_count;

    answerContent.textContent = response.answer;

    if (explainability) {
        explainabilitySection.style.display = 'block';
        explainabilityContent.textContent = formatExplainability(explainability);
    } else {
        explainabilitySection.style.display = 'none';
    }

    processingTime.textContent = `${response.processing_time_ms.toFixed(2)}ms`;
    timestamp.textContent = new Date(response.timestamp).toLocaleString();

    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ===== FORMATTING HELPERS =====
function formatConfidenceLevel(level) {
    const levels = {
        'high_confidence': 'High Confidence',
        'partial_evidence': 'Partial Evidence',
        'insufficient_data': 'Insufficient Data'
    };
    return levels[level] || level;
}

function formatExplainability(explainability) {
    let text = '';

    // Query decomposition
    text += '=== QUERY DECOMPOSITION ===\n';
    text += `Intent: ${explainability.query_decomposition.intent}\n`;
    text += `Sub-questions: ${explainability.query_decomposition.sub_questions.length}\n\n`;

    explainability.query_decomposition.sub_questions.forEach((sq, i) => {
        text += `${i + 1}. ${sq.question}\n`;
        if (sq.required_metrics.length > 0) {
            text += `   Metrics: ${sq.required_metrics.join(', ')}\n`;
        }
        if (sq.required_segments.length > 0) {
            text += `   Segments: ${sq.required_segments.join(', ')}\n`;
        }
    });

    // Evidence
    text += `\n=== EVIDENCE COLLECTED ===\n`;
    text += `Total: ${explainability.evidence_objects.length} objects\n`;
    text += `Sources: ${[...new Set(explainability.evidence_objects.map(e => e.source))].join(', ')}\n\n`;

    explainability.evidence_objects.slice(0, 5).forEach((evidence, i) => {
        text += `${i + 1}. ${evidence.metric} (${evidence.segment})\n`;
        text += `   Value: ${evidence.value.toFixed(2)}\n`;
        if (evidence.change !== null) {
            text += `   Change: ${evidence.change > 0 ? '+' : ''}${evidence.change.toFixed(1)}%\n`;
        }
        text += `   Confidence: ${(evidence.confidence * 100).toFixed(0)}%\n`;
    });

    // Agent execution
    text += `\n=== AGENT EXECUTION ===\n`;
    explainability.agent_responses.forEach(agent => {
        text += `${agent.agent_name}: ${agent.processing_time_ms.toFixed(2)}ms\n`;
    });

    // Validation
    text += `\n=== VALIDATION ===\n`;
    text += `Valid: ${explainability.validation_result.is_valid}\n`;
    text += `Validated Evidence: ${explainability.validation_result.validated_evidence.length}\n`;

    // Confidence details
    text += `\n=== CONFIDENCE ASSESSMENT ===\n`;
    text += `Level: ${formatConfidenceLevel(explainability.confidence_details.confidence_level)}\n`;
    text += `Coverage: ${(explainability.confidence_details.coverage_score * 100).toFixed(1)}%\n`;
    text += `Completeness: ${(explainability.confidence_details.completeness_score * 100).toFixed(1)}%\n`;
    text += `Reasoning: ${explainability.confidence_details.reasoning}\n`;

    // Reasoning steps
    if (explainability.reasoning_steps && explainability.reasoning_steps.length > 0) {
        text += `\n=== REASONING STEPS ===\n`;
        explainability.reasoning_steps.forEach(step => {
            text += `${step}\n`;
        });
    }

    return text;
}

// ===== ERROR HANDLING =====
function showError(message) {
    hideAll();
    errorContainer.style.display = 'block';
    errorMessage.textContent = message;
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function hideAll() {
    loadingContainer.style.display = 'none';
    resultsSection.style.display = 'none';
    errorContainer.style.display = 'none';
}

// ===== COSMIC EFFECTS =====
// Add particle effects on mouse move
document.addEventListener('mousemove', (e) => {
    if (Math.random() > 0.95) {
        createParticle(e.clientX, e.clientY);
    }
});

function createParticle(x, y) {
    const particle = document.createElement('div');
    particle.style.position = 'fixed';
    particle.style.left = x + 'px';
    particle.style.top = y + 'px';
    particle.style.width = '4px';
    particle.style.height = '4px';
    particle.style.borderRadius = '50%';
    particle.style.background = `rgba(${Math.random() * 100 + 155}, ${Math.random() * 100 + 155}, 255, 0.8)`;
    particle.style.pointerEvents = 'none';
    particle.style.zIndex = '9999';
    particle.style.boxShadow = '0 0 10px currentColor';

    document.body.appendChild(particle);

    const animation = particle.animate([
        { transform: 'translate(0, 0) scale(1)', opacity: 1 },
        { transform: `translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px) scale(0)`, opacity: 0 }
    ], {
        duration: 1000,
        easing: 'ease-out'
    });

    animation.onfinish = () => particle.remove();
}

// Add glow effect to input on focus
queryInput.addEventListener('focus', () => {
    queryInput.style.boxShadow = '0 0 30px rgba(0, 212, 255, 0.5)';
});

queryInput.addEventListener('blur', () => {
    queryInput.style.boxShadow = 'none';
});

// ===== CHAT FUNCTIONALITY =====
async function sendChatMessage() {
    const message = chatInput.value.trim();

    if (!message) return;

    chatInput.disabled = true;
    sendChatBtn.disabled = true;

    addMessageToChat('user', message);

    chatInput.value = '';
    chatInput.style.height = 'auto';

    conversationHistory.push({
        role: 'user',
        content: message
    });

    const typingIndicator = showTypingIndicator();

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                messages: conversationHistory
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        typingIndicator.remove();

        const assistantMessageDiv = createAssistantMessageContainer();
        const contentDiv = assistantMessageDiv.querySelector('.message-content');
        let fullMessage = '';

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();

            if (done) break;

            const chunk = decoder.decode(value, { stream: true });

            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const jsonStr = line.substring(6);
                        const data = JSON.parse(jsonStr);

                        if (data.error) {
                            contentDiv.textContent = `Error: ${data.error}`;
                            break;
                        }

                        if (data.token && !data.done) {
                            fullMessage += data.token;
                            contentDiv.textContent = fullMessage;

                            chatMessages.scrollTop = chatMessages.scrollHeight;
                        }

                        if (data.done) {
                            break;
                        }
                    } catch (e) {
                        console.warn('Failed to parse SSE data:', e);
                    }
                }
            }
        }

        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = new Date().toLocaleTimeString();
        contentDiv.appendChild(timeDiv);

        conversationHistory.push({
            role: 'assistant',
            content: fullMessage
        });

    } catch (error) {
        typingIndicator.remove();
        addMessageToChat('assistant', `Connection error: ${error.message}`);
    } finally {
        chatInput.disabled = false;
        sendChatBtn.disabled = false;
        chatInput.focus();
    }
}

function createAssistantMessageContainer() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = '';

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;

    return messageDiv;
}

function addMessageToChat(role, content) {
    const welcomeMsg = chatMessages.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;

    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString();

    contentDiv.appendChild(timeDiv);
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    chatMessages.appendChild(messageDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';

    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';

    typingDiv.appendChild(avatar);
    typingDiv.appendChild(indicator);
    chatMessages.appendChild(typingDiv);

    chatMessages.scrollTop = chatMessages.scrollHeight;

    return typingDiv;
}

console.log('%c🌌 RAG++ Cosmic Interface Loaded 🌌', 'color: #00d4ff; font-size: 20px; font-weight: bold;');
console.log('%cBackend API: ' + API_BASE_URL, 'color: #ff00ff; font-size: 14px;');
console.log('%c💬 Chat Mode: Powered by Ollama', 'color: #00ff88; font-size: 14px;');
