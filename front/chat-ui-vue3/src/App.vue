<template>
  <div id="app">
    <beautiful-chat
      :participants="participants"
      :titleImageUrl="titleImageUrl"
      :onMessageWasSent="onMessageWasSent"
      :messageList="messageList"
      :newMessagesCount="newMessagesCount"
      :isOpen="isChatOpen"
      :close="closeChat"
      :open="openChat"
      :showEmoji="true"
      :showFile="true"
      :showTypingIndicator="showTypingIndicator"
      :colors="colors"
      :alwaysScrollToBottom="alwaysScrollToBottom"
    />
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      apiBaseUrl: process.env.VUE_APP_API_URL || 'http://localhost:8000',
      participants: [
        {
          id: 'user',
          name: 'Utilisateur',
          imageUrl: '',
        },
        {
          id: 'agent',
          name: 'Agent Virtuel',
          imageUrl: '',
        },
      ],
      titleImageUrl: '',
      messageList: [],      // affichage dans le chat
      validMessages: [],    // uniquement ce qu'on envoie au backend
      newMessagesCount: 0,
      isChatOpen: true,
      showTypingIndicator: '',
      alwaysScrollToBottom: true,
      colors: {
        header: {
          bg: '#4e8cff',
          text: '#ffffff',
        },
        launcher: {
          bg: '#4e8cff',
        },
        messageList: {
          bg: '#ffffff',
        },
        sentMessage: {
          bg: '#4e8cff',
          text: '#ffffff',
        },
        receivedMessage: {
          bg: '#eaeaea',
          text: '#222222',
        },
        userInput: {
          bg: '#f4f7f9',
          text: '#565867',
        },
      },
    };
  },
  methods: {
    async onMessageWasSent(message) {
      const text = message.data?.text?.trim()

      if (!text || text.length < 2 || !/[a-zA-ZÀ-ÿ]/.test(text)) {
        this.messageList.push({
          type: 'text',
          author: 'agent',
          data: { text: "Ton message est trop court ou incompréhensible" }
        })
        return
      }

      // Ajout visuel côté UI
      this.messageList.push({
        type: 'text',
        author: 'me',
        data: { text }
      })

      // Ajout logique pour l'historique backend
      this.validMessages.push({
        sender: 'user',
        content: text
      })

      const history = [...this.validMessages]

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000);

      try {
        const res = await fetch(`${this.apiBaseUrl}/chat/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ history }),
          signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data = await res.json();

        if (data && data.content && data.sender) {
          this.messageList.push({
            type: 'text',
            author: data.sender,
            data: { text: data.content }
          });

          this.validMessages.push({
            sender: 'agent',
            content: data.content
          });
        } else {
          throw new Error('Invalid response format');
        }
      } catch (err) {
        clearTimeout(timeoutId);
        const errorMessage = err.name === 'AbortError'
          ? 'La requête a expiré. Veuillez réessayer.'
          : err.message || 'Une erreur est survenue lors de la communication avec le serveur.';
        this.messageList.push({
          type: 'text',
          author: 'agent',
          data: { text: `Erreur: ${errorMessage}` }
        });
      }
    },
    closeChat() {
      this.isChatOpen = false
    },
    openChat() {
      this.isChatOpen = true
    }
  }
}
</script>

<style>
body, html, #app {
  height: 100%;
  margin: 0;
}
</style>
