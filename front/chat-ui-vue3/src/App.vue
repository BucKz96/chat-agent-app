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

      if (!text || text.length < 1 || !/[a-zA-ZÀ-ÿ]/.test(text)) {
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

      try {
        const res = await fetch('http://localhost:8000/chat/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ history })
        })

        const data = await res.json()
        console.log("Réponse backend:", data)

        if (data && data.content && data.sender) {
          this.messageList.push({
            type: 'text',
            author: data.sender,
            data: { text: data.content }
          })

          this.validMessages.push({
            sender: 'agent',
            content: data.content
          })
        } else {
          this.messageList.push({
            type: 'text',
            author: 'agent',
            data: { text: 'Erreur inconnue' }
          })
        }
      } catch (err) {
        this.messageList.push({
          type: 'text',
          author: 'agent',
          data: { text: 'Erreur serveur' }
        })
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
