const form = document.getElementById('chat-form');
const conversationDiv = document.getElementById('conversation');
const latestResponseDiv = document.getElementById('latest-response');
const loadingCard = document.getElementById('loading-card');
const toggleHistoryButton = document.getElementById('toggle-history');
const md = window.markdownit();

toggleHistoryButton.addEventListener('click', () => {
    if (conversationDiv.classList.contains('hidden')) {
        conversationDiv.classList.remove('hidden');
        toggleHistoryButton.textContent = 'Hide';
    } else {
        conversationDiv.classList.add('hidden');
        toggleHistoryButton.textContent = 'Show';
    }
});


function renderConversation(userMessage, botMessage) {
    const userHTML = `<div class="message user-message"><strong>User:</strong> ${md.render(userMessage)}</div>`;
    const botHTML = `<div class="message bot-message"><strong>Chatbot:</strong> ${md.render(botMessage)}</div>`;
    conversationDiv.innerHTML += userHTML + botHTML;

    smoothScrollToBottom(conversationDiv);

    sessionStorage.setItem('conversation', conversationDiv.innerHTML);
}

function smoothScrollToBottom(element) {
    element.scrollTo({
        top: element.scrollHeight,
        behavior: 'smooth'
    });
}

window.onload = () => {
    const storedConversation = sessionStorage.getItem('conversation');
    if (storedConversation) {
        conversationDiv.innerHTML = storedConversation;
    }
};

form.onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    loadingCard.classList.remove('hidden');
    form.querySelector('button[type="submit"]').disabled = true; 

    try {
        const response = await fetch('/run_flow', { method: 'POST', body: formData });
        loadingCard.classList.add('hidden'); 
        form.querySelector('button[type="submit"]').disabled = false;

        const data = await response.json();

        if (response.ok) {
            latestResponseDiv.innerHTML = `<div class="bot-message"><strong>Chatbot:</strong> ${md.render(data.response_text)}</div>`;
            renderConversation(data.user_message, data.response_text);
            form.reset();
        } else {
            alert(data.error);
        }
    } catch (error) {
        loadingCard.classList.add('hidden'); 
        form.querySelector('button[type="submit"]').disabled = false; 
        console.error("Error:", error);
        alert("An error occurred while processing your request.");
    }
};
