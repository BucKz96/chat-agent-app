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
      this.messageList.push(message)

      const history = this.messageList.map(m => ({
        sender: m.author,
        content: m.data.text
      }))

      try {
        const res = await fetch('http://localhost:8000/chat/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ history })
        })

        const data = await res.json()

        this.messageList.push({
          type: 'text',
          author: 'agent',
          data: { text: data.content }
        })
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

