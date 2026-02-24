<template>
  <div class="min-h-screen bg-slate-900">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-white">Messages</h1>
        <p class="text-gray-400 mt-1">View and send messages</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Message List -->
        <div class="lg:col-span-1 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10">
          <div class="p-4 border-b border-white/10">
            <h2 class="text-lg font-medium text-white">Inbox</h2>
          </div>
          
          <div v-if="loading" class="p-4 text-center text-gray-400">
            Loading messages...
          </div>
          
          <div v-else-if="messages.length === 0" class="p-4 text-center text-gray-400">
            No messages yet
          </div>
          
          <div v-else class="divide-y divide-white/5">
            <button
              v-for="message in messages"
              :key="message.id"
              @click="selectMessage(message)"
              class="w-full p-4 text-left hover:bg-white/5 transition-colors"
              :class="selectedMessage?.id === message.id ? 'bg-white/10' : ''"
            >
              <div class="flex items-start">
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-white truncate">
                    {{ message.subject || 'No Subject' }}
                  </p>
                  <p class="text-xs text-gray-400 truncate mt-1">
                    {{ message.body }}
                  </p>
                  <p class="text-xs text-gray-500 mt-2">
                    {{ formatDate(message.created_at) }}
                  </p>
                </div>
                <span 
                  v-if="!message.is_read"
                  class="w-2 h-2 bg-blue-500 rounded-full flex-shrink-0 ml-2 mt-2"
                ></span>
              </div>
            </button>
          </div>
        </div>

        <!-- Message Detail / Compose -->
        <div class="lg:col-span-2 bg-white/5 backdrop-blur-sm rounded-xl border border-white/10">
          <div v-if="selectedMessage" class="h-full flex flex-col">
            <div class="p-4 border-b border-white/10 flex items-center justify-between">
              <div>
                <h3 class="text-lg font-medium text-white">{{ selectedMessage.subject || 'No Subject' }}</h3>
                <p class="text-sm text-gray-400">From: {{ selectedMessage.sender_id }}</p>
              </div>
              <button 
                v-if="!selectedMessage.is_read"
                @click="markAsRead(selectedMessage.id)"
                class="px-3 py-1 text-sm text-blue-400 hover:text-blue-300"
              >
                Mark as read
              </button>
            </div>
            <div class="flex-1 p-4 overflow-y-auto">
              <p class="text-gray-300 whitespace-pre-wrap">{{ selectedMessage.body }}</p>
            </div>
          </div>

          <div v-else class="h-full flex flex-col">
            <div class="p-4 border-b border-white/10">
              <h3 class="text-lg font-medium text-white">Send New Message</h3>
            </div>
            
            <form @submit.prevent="sendMessage" class="flex-1 p-4 space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">To (User ID)</label>
                <input 
                  v-model="newMessage.receiver_id"
                  type="number"
                  required
                  class="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter user ID"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Subject</label>
                <input 
                  v-model="newMessage.subject"
                  type="text"
                  class="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter subject"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">Message</label>
                <textarea 
                  v-model="newMessage.body"
                  required
                  rows="6"
                  class="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  placeholder="Enter your message"
                ></textarea>
              </div>
              
              <div class="flex items-center gap-4">
                <button 
                  type="submit"
                  :disabled="sending"
                  class="px-4 py-2 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-lg font-medium hover:from-blue-500 hover:to-cyan-500 disabled:opacity-50 transition-all"
                >
                  {{ sending ? 'Sending...' : 'Send Message' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { messageService } from '../services/api'

interface Message {
  id: number
  sender_id: number
  receiver_id: number
  subject: string
  body: string
  type: string
  priority: string
  is_read: boolean
  read_at: string | null
  created_at: string
}

const messages = ref<Message[]>([])
const loading = ref(false)
const selectedMessage = ref<Message | null>(null)
const sending = ref(false)

const newMessage = ref({
  receiver_id: null as number | null,
  subject: '',
  body: ''
})

onMounted(async () => {
  await loadMessages()
})

const loadMessages = async () => {
  loading.value = true
  try {
    const response = await messageService.getMessages()
    if (response.success && response.data) {
      messages.value = response.data
    }
  } catch (error) {
    console.error('Error loading messages:', error)
  } finally {
    loading.value = false
  }
}

const selectMessage = async (message: Message) => {
  selectedMessage.value = message
  if (!message.is_read) {
    await markAsRead(message.id)
  }
}

const markAsRead = async (id: number) => {
  try {
    await messageService.markAsRead(id)
    const message = messages.value.find(m => m.id === id)
    if (message) {
      message.is_read = true
      message.read_at = new Date().toISOString()
    }
  } catch (error) {
    console.error('Error marking message as read:', error)
  }
}

const sendMessage = async () => {
  if (!newMessage.value.receiver_id || !newMessage.value.body) return
  
  sending.value = true
  try {
    const response = await messageService.sendMessage({
      receiver_id: newMessage.value.receiver_id,
      subject: newMessage.value.subject,
      body: newMessage.value.body
    })
    
    if (response.success) {
      newMessage.value = { receiver_id: null, subject: '', body: '' }
      await loadMessages()
    }
  } catch (error) {
    console.error('Error sending message:', error)
  } finally {
    sending.value = false
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>
