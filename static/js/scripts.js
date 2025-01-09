const form = document.getElementById('chat-form');
const conversationDiv = document.getElementById('conversation');
const latestResponseDiv = document.getElementById('latest-response');
const loadingCard = document.getElementById('loading-card');
const toggleHistoryButton = document.getElementById('toggle-history');
const md = window.markdownit();

// Toggle conversation history visibility
toggleHistoryButton.addEventListener('click', () => {
    if (conversationDiv.classList.contains('hidden')) {
        conversationDiv.classList.remove('hidden');
        toggleHistoryButton.textContent = 'Hide';
    } else {
        conversationDiv.classList.add('hidden');
        toggleHistoryButton.textContent = 'Show';
    }
});

// Render conversation history
function renderConversation(userMessage, botMessage) {
    const userHTML = `<div class="message user-message"><strong>User:</strong> ${md.render(userMessage)}</div>`;
    const botHTML = `<div class="message bot-message"><strong>Chatbot:</strong> ${md.render(botMessage)}</div>`;
    conversationDiv.innerHTML += userHTML + botHTML;

    // Scroll to the bottom of the conversation history
    smoothScrollToBottom(conversationDiv);

    // Save updated conversation to sessionStorage
    sessionStorage.setItem('conversation', conversationDiv.innerHTML);
}

// Smooth scrolling to the bottom of the conversation history
function smoothScrollToBottom(element) {
    element.scrollTo({
        top: element.scrollHeight,
        behavior: 'smooth'
    });
}

// Load conversation history from sessionStorage (if available)
window.onload = () => {
    const storedConversation = sessionStorage.getItem('conversation');
    if (storedConversation) {
        conversationDiv.innerHTML = storedConversation;
    }
};

// Submit form
form.onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    loadingCard.classList.remove('hidden'); // Show loading card
    form.querySelector('button[type="submit"]').disabled = true; // Disable submit button during the request

    try {
        const response = await fetch('/run_flow', { method: 'POST', body: formData });
        loadingCard.classList.add('hidden'); // Hide loading card
        form.querySelector('button[type="submit"]').disabled = false; // Enable submit button after the request

        const data = await response.json();

        if (response.ok) {
            latestResponseDiv.innerHTML = `<div class="bot-message"><strong>Chatbot:</strong> ${md.render(data.response_text)}</div>`;
            renderConversation(data.user_message, data.response_text);
            form.reset();
        } else {
            alert(data.error);
        }
    } catch (error) {
        loadingCard.classList.add('hidden'); // Ensure loading card is hidden on error
        form.querySelector('button[type="submit"]').disabled = false; // Re-enable the button
        console.error("Error:", error);
        alert("An error occurred while processing your request.");
    }
};
