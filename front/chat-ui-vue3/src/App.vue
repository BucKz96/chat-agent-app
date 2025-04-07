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
      messageList: [],
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
        this.messageList.push({
            type: 'text',
              author: 'me',
              data: { text: message.data?.text || '' }
        })

      const history = this.messageList.map(m => ({
        sender: m.author === 'me' ? 'user' : 'agent',
        content: m.data.text
      }))

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
          data: { text: 'Erreur serveur ❌' }
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

