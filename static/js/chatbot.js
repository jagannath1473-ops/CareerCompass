document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.getElementById("chatbotToggle");
  const panel = document.getElementById("chatbotPanel");
  const closeButton = document.getElementById("closeChatButton");
  const newButton = document.getElementById("newChatButton");
  const deleteButton = document.getElementById("deleteChatButton");
  const select = document.getElementById("conversationSelect");
  const messages = document.getElementById("chatbotMessages");
  const form = document.getElementById("chatbotForm");
  const input = document.getElementById("chatbotInput");
  if (!toggle || !panel) return;
  let currentConversationId = null;

  const api = async (url, options = {}) => {
    const response = await fetch(url, { headers: { "Content-Type": "application/json", ...(options.headers || {}) }, ...options });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "The local chatbot request failed.");
    return data;
  };
  const addMessage = (message) => {
    const bubble = document.createElement("div");
    bubble.className = `chat-message ${message.sender}`;
    const text = document.createElement("p");
    text.textContent = message.content;
    text.style.whiteSpace = "pre-line";
    bubble.appendChild(text);
    const links = Array.isArray(message.links) && message.links.length
      ? message.links
      : (message.link_url ? [{ text: message.link_text, url: message.link_url }] : []);
    links.forEach((item) => {
      const link = document.createElement("a");
      link.href = item.url;
      link.textContent = item.text || "View details";
      link.className = "chat-message-link";
      if (/^https?:\/\//.test(item.url)) { link.target = "_blank"; link.rel = "noopener"; }
      bubble.appendChild(link);
    });
    messages.appendChild(bubble);
    messages.scrollTop = messages.scrollHeight;
  };
  const loadConversation = async (conversationId) => {
    const data = await api(`/api/chat/conversations/${conversationId}`);
    currentConversationId = Number(conversationId);
    select.value = String(conversationId);
    messages.innerHTML = "";
    data.messages.forEach(addMessage);
  };
  const refreshConversations = async (preferredId = null) => {
    let conversations = await api("/api/chat/conversations");
    if (!conversations.length) {
      const created = await api("/api/chat/conversations", { method: "POST", body: "{}" });
      conversations = [created];
      preferredId = created.id;
    }
    select.innerHTML = "";
    conversations.forEach((conversation) => {
      const option = document.createElement("option");
      option.value = conversation.id;
      option.textContent = conversation.title;
      select.appendChild(option);
    });
    await loadConversation(preferredId || currentConversationId || conversations[0].id);
  };
  const createConversation = async () => {
    const conversation = await api("/api/chat/conversations", { method: "POST", body: "{}" });
    await refreshConversations(conversation.id);
  };
  const showError = (message) => addMessage({ sender: "bot", content: message });
  const openPanel = async () => {
    panel.classList.add("open"); panel.setAttribute("aria-hidden", "false"); toggle.setAttribute("aria-expanded", "true");
    if (!currentConversationId) try { await refreshConversations(); } catch (error) { showError(error.message); }
    input.focus();
  };
  const closePanel = () => { panel.classList.remove("open"); panel.setAttribute("aria-hidden", "true"); toggle.setAttribute("aria-expanded", "false"); };
  toggle.addEventListener("click", () => panel.classList.contains("open") ? closePanel() : openPanel());
  closeButton.addEventListener("click", closePanel);
  newButton.addEventListener("click", () => createConversation().catch((error) => showError(error.message)));
  deleteButton.addEventListener("click", async () => {
    if (!currentConversationId || !window.confirm("Delete this local conversation?")) return;
    try { await api(`/api/chat/conversations/${currentConversationId}`, { method: "DELETE" }); currentConversationId = null; await refreshConversations(); }
    catch (error) { showError(error.message); }
  });
  select.addEventListener("change", () => loadConversation(select.value).catch((error) => showError(error.message)));
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = input.value.trim();
    if (!message) return;
    if (!currentConversationId) await createConversation();
    addMessage({ sender: "user", content: message });
    input.value = ""; input.disabled = true;
    try {
      const reply = await api(`/api/chat/conversations/${currentConversationId}/messages`, { method: "POST", body: JSON.stringify({ message }) });
      addMessage(reply); await refreshConversations(currentConversationId);
    } catch (error) { showError(error.message); }
    finally { input.disabled = false; input.focus(); }
  });
});
