<template>
  <div class="code-input-container">
    <div class="language-selector">
      <label for="language">Programming Language:</label>
      <select 
        id="language" 
        v-model="selectedLanguage"
        :disabled="loading"
      >
        <option value="python">Python</option>
        <option value="javascript">JavaScript</option>
        <option value="typescript">TypeScript</option>
        <option value="java">Java</option>
        <option value="csharp">C#</option>
        <option value="php">PHP</option>
        <option value="ruby">Ruby</option>
        <option value="go">Go</option>
        <option value="rust">Rust</option>
        <option value="c">C</option>
        <option value="cpp">C++</option>
      </select>
    </div>

    <div class="code-textarea-wrapper">
      <label for="code">Source Code:</label>
      <textarea
        id="code"
        v-model="code"
        :class="['code-textarea', `language-${selectedLanguage}`]"
        :disabled="loading"
        placeholder="Paste your code here for security analysis..."
        rows="15"
        spellcheck="false"
      ></textarea>
      <div class="char-count">
        {{ code.length }} / {{ maxLength }} characters
      </div>
    </div>

    <div class="actions">
      <button 
        class="btn-analyze"
        :disabled="loading || !isValid"
        @click="analyzeCode"
      >
        <span v-if="loading" class="spinner"></span>
        <span v-else>Analyze Code</span>
      </button>
      
      <button 
        class="btn-clear"
        :disabled="loading"
        @click="clearCode"
      >
        Clear
      </button>
    </div>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const emit = defineEmits<{
  (e: 'analyze', payload: { code: string; language: string }): void
}>()

const code = ref('')
const selectedLanguage = ref('python')
const loading = ref(false)
const error = ref('')
const maxLength = 10240

const isValid = computed(() => {
  return code.value.trim().length > 0 && code.value.length <= maxLength
})

const analyzeCode = () => {
  error.value = ''
  
  if (!code.value.trim()) {
    error.value = 'Please enter some code to analyze'
    return
  }
  
  if (code.value.length > maxLength) {
    error.value = `Code exceeds maximum length of ${maxLength} characters`
    return
  }
  
  loading.value = true
  emit('analyze', {
    code: code.value,
    language: selectedLanguage.value
  })
}

const clearCode = () => {
  code.value = ''
  error.value = ''
}

// Expose loading state setter for parent component
defineExpose({
  setLoading: (value: boolean) => { loading.value = value },
  setError: (value: string) => { error.value = value }
})
</script>

<style scoped>
.code-input-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.language-selector {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.language-selector label {
  font-weight: 500;
  color: #374151;
}

.language-selector select {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  background-color: white;
  cursor: pointer;
}

.language-selector select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.code-textarea-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.code-textarea-wrapper label {
  font-weight: 500;
  color: #374151;
}

.code-textarea {
  font-family: 'Fira Code', 'Monaco', 'Consolas', monospace;
  font-size: 0.875rem;
  padding: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  resize: vertical;
  background-color: #1e1e1e;
  color: #d4d4d4;
  line-height: 1.5;
}

.code-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.code-textarea:disabled {
  background-color: #f3f4f6;
  cursor: not-allowed;
}

.char-count {
  text-align: right;
  font-size: 0.75rem;
  color: #6b7280;
}

.actions {
  display: flex;
  gap: 1rem;
}

.btn-analyze {
  flex: 1;
  padding: 0.75rem 1.5rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-analyze:hover:not(:disabled) {
  background-color: #2563eb;
}

.btn-analyze:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.btn-clear {
  padding: 0.75rem 1.5rem;
  background-color: white;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-clear:hover:not(:disabled) {
  background-color: #f3f4f6;
}

.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid white;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  padding: 0.75rem;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 0.375rem;
  color: #dc2626;
  font-size: 0.875rem;
}
</style>
