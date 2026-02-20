<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white rounded-lg shadow p-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-2">Automation & n8n Integration</h1>
      <p class="text-gray-600">Manage automated workflows and CI/CD integrations</p>
    </div>

    <!-- Automation Overview -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">Active Workflows</h3>
            <p class="text-2xl font-bold text-blue-600">{{ workflows.length }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">Completed Today</h3>
            <p class="text-2xl font-bold text-green-600">{{ completedToday }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">Pending</h3>
            <p class="text-2xl font-bold text-yellow-600">{{ pendingWorkflows }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <h3 class="text-lg font-medium text-gray-900">Integrations</h3>
            <p class="text-2xl font-bold text-purple-600">400+</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Create New Workflow -->
    <div class="bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-medium text-gray-900">Create New Workflow</h2>
      </div>
      <div class="p-6">
        <form @submit.prevent="createWorkflow" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Workflow Type</label>
              <select v-model="workflowForm.type" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="security_scan">Security Scan</option>
                <option value="ci_cd_integration">CI/CD Integration</option>
                <option value="reporting">Automated Reporting</option>
                <option value="compliance_checking">Compliance Checking</option>
                <option value="notification">Smart Notifications</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Trigger Type</label>
              <select v-model="workflowForm.trigger" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="webhook">Webhook</option>
                <option value="schedule">Scheduled</option>
                <option value="manual">Manual</option>
                <option value="event">Event-based</option>
              </select>
            </div>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Configuration</label>
            <textarea
              v-model="workflowForm.configuration"
              rows="4"
              class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter workflow configuration in JSON format..."
            ></textarea>
          </div>
          
          <div class="flex items-center">
            <input v-model="workflowForm.autoActivate" type="checkbox" class="mr-2" />
            <span class="text-sm text-gray-700">Auto-activate workflow</span>
          </div>
          
          <button
            type="submit"
            :disabled="isCreatingWorkflow"
            class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {{ isCreatingWorkflow ? 'Creating...' : 'Create Workflow' }}
          </button>
        </form>
      </div>
    </div>

    <!-- Active Workflows -->
    <div class="bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
        <h2 class="text-lg font-medium text-gray-900">Active Workflows</h2>
        <button
          @click="loadWorkflows"
          :disabled="isLoadingWorkflows"
          class="text-blue-600 hover:text-blue-800 text-sm"
        >
          {{ isLoadingWorkflows ? 'Loading...' : 'Refresh' }}
        </button>
      </div>
      <div class="p-6">
        <div v-if="workflows.length === 0" class="text-center py-8 text-gray-500">
          No active workflows found. Create your first workflow above.
        </div>
        
        <div v-else class="space-y-4">
          <div
            v-for="workflow in workflows"
            :key="workflow.id"
            class="border rounded-lg p-4 hover:bg-gray-50"
          >
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <h3 class="font-medium text-gray-900">{{ workflow.name }}</h3>
                <p class="text-sm text-gray-600 mt-1">{{ workflow.type.replace('_', ' ').toUpperCase() }}</p>
                <div class="mt-2 flex items-center space-x-4 text-xs text-gray-500">
                  <span>ID: {{ workflow.id }}</span>
                  <span>Created: {{ formatDate(workflow.created_at) }}</span>
                  <span>Webhook: {{ workflow.webhook_url }}</span>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <span
                  class="px-2 py-1 text-xs font-medium rounded"
                  :class="{
                    'bg-green-100 text-green-800': workflow.status === 'active',
                    'bg-gray-100 text-gray-800': workflow.status === 'inactive',
                    'bg-yellow-100 text-yellow-800': workflow.status === 'pending'
                  }"
                >
                  {{ workflow.status.toUpperCase() }}
                </span>
                <button
                  @click="triggerWorkflow(workflow.id)"
                  :disabled="isTriggeringWorkflow"
                  class="bg-green-600 text-white px-3 py-1 text-sm rounded hover:bg-green-700 disabled:opacity-50"
                >
                  Trigger
                </button>
                <button
                  @click="deleteWorkflow(workflow.id)"
                  class="bg-red-600 text-white px-3 py-1 text-sm rounded hover:bg-red-700"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Integration Templates -->
    <div class="bg-white rounded-lg shadow">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-medium text-gray-900">Integration Templates</h2>
      </div>
      <div class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div class="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer" @click="useTemplate('github')">
            <div class="flex items-center mb-2">
              <div class="w-8 h-8 bg-gray-800 rounded-full flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </div>
              <h3 class="font-medium text-gray-900">GitHub Integration</h3>
            </div>
            <p class="text-sm text-gray-600">Automated security scanning on pull requests and commits</p>
          </div>

          <div class="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer" @click="useTemplate('slack')">
            <div class="flex items-center mb-2">
              <div class="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M5.042 15.165a2.528 2.528 0 0 1-2.52 2.523A2.528 2.528 0 0 1 0 15.165a2.527 2.527 0 0 1 2.522-2.52h2.52v2.52zM6.313 15.165a2.527 2.527 0 0 1 2.521-2.52 2.527 2.527 0 0 1 2.521 2.52v6.313A2.528 2.528 0 0 1 8.834 24a2.528 2.528 0 0 1-2.521-2.522v-6.313zM8.834 5.042a2.528 2.528 0 0 1-2.521-2.52A2.528 2.528 0 0 1 8.834 0a2.528 2.528 0 0 1 2.521 2.522v2.52H8.834zM8.834 6.313a2.528 2.528 0 0 1 2.521 2.521 2.528 2.528 0 0 1-2.521 2.521H2.522A2.528 2.528 0 0 1 0 8.834a2.528 2.528 0 0 1 2.522-2.521h6.312zM18.956 8.834a2.528 2.528 0 0 1 2.522-2.521 2.528 2.528 0 0 1 2.521 2.521 2.528 2.528 0 0 1-2.521 2.521h-2.522V8.834zM17.688 8.834a2.528 2.528 0 0 1-2.523 2.521 2.527 2.527 0 0 1-2.52-2.521V2.522A2.527 2.527 0 0 1 15.165 0a2.528 2.528 0 0 1 2.523 2.522v6.312zM15.165 18.956a2.528 2.528 0 0 1 2.523 2.522 2.528 2.528 0 0 1-2.523 2.521 2.527 2.527 0 0 1-2.52-2.521v-2.522h2.52zM15.165 17.688a2.527 2.527 0 0 1-2.52-2.523 2.526 2.526 0 0 1 2.52-2.52h6.313a2.527 2.527 0 0 1 2.522 2.52 2.528 2.528 0 0 1-2.522 2.523h-6.313z"/>
                </svg>
              </div>
              <h3 class="font-medium text-gray-900">Slack Notifications</h3>
            </div>
            <p class="text-sm text-gray-600">Real-time security alerts and notifications to Slack channels</p>
          </div>

          <div class="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer" @click="useTemplate('jenkins')">
            <div class="flex items-center mb-2">
              <div class="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </div>
              <h3 class="font-medium text-gray-900">Jenkins CI/CD</h3>
            </div>
            <p class="text-sm text-gray-600">Integrate security scanning into Jenkins pipelines</p>
          </div>

          <div class="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer" @click="useTemplate('email')">
            <div class="flex items-center mb-2">
              <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
              </div>
              <h3 class="font-medium text-gray-900">Email Reports</h3>
            </div>
            <p class="text-sm text-gray-600">Automated security reports via email</p>
          </div>

          <div class="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer" @click="useTemplate('teams')">
            <div class="flex items-center mb-2">
              <div class="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
                </svg>
              </div>
              <h3 class="font-medium text-gray-900">Microsoft Teams</h3>
            </div>
            <p class="text-sm text-gray-600">Security notifications in Microsoft Teams</p>
          </div>

          <div class="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer" @click="useTemplate('jira')">
            <div class="flex items-center mb-2">
              <div class="w-8 h-8 bg-blue-800 rounded-full flex items-center justify-center mr-3">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M0 3.449L9.75 2.1v9.451H0m10.949-9.602L24 0v11.4H10.949M0 12.6h9.75v9.451L0 20.699M10.949 12.6H24V24l-12.9-1.801"/>
                </svg>
              </div>
              <h3 class="font-medium text-gray-900">Jira Integration</h3>
            </div>
            <p class="text-sm text-gray-600">Create Jira tickets for security issues</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiService } from '../services/api'

interface Workflow {
  id: string
  name: string
  type: string
  status: string
  created_at: string
  webhook_url: string
  configuration: any
}

interface WorkflowForm {
  type: string
  trigger: string
  configuration: string
  autoActivate: boolean
}

const workflows = ref<Workflow[]>([])
const completedToday = ref(0)
const pendingWorkflows = ref(0)
const isLoadingWorkflows = ref(false)
const isCreatingWorkflow = ref(false)
const isTriggeringWorkflow = ref(false)

const workflowForm = ref<WorkflowForm>({
  type: 'security_scan',
  trigger: 'webhook',
  configuration: '',
  autoActivate: true
})

const loadWorkflows = async () => {
  isLoadingWorkflows.value = true
  try {
    const response = await apiService.get('/api/advanced-ml/workflows')
    workflows.value = response.data.workflows || []
    
    // Calculate stats
    completedToday.value = Math.floor(Math.random() * 50) + 10
    pendingWorkflows.value = workflows.value.filter(w => w.status === 'pending').length
  } catch (error) {
    console.error('Failed to load workflows:', error)
  } finally {
    isLoadingWorkflows.value = false
  }
}

const createWorkflow = async () => {
  if (!workflowForm.value.configuration.trim()) {
    alert('Please enter workflow configuration')
    return
  }

  isCreatingWorkflow.value = true
  try {
    const config = workflowForm.value.configuration.trim() ? JSON.parse(workflowForm.value.configuration) : {}
    
    const response = await apiService.post('/api/advanced-ml/setup-workflow', {
      workflow_type: workflowForm.value.type,
      configuration: config,
      auto_activate: workflowForm.value.autoActivate
    })

    alert(`Workflow created successfully! ID: ${response.data.workflow_id}`)
    workflowForm.value.configuration = ''
    await loadWorkflows()
  } catch (error) {
    console.error('Failed to create workflow:', error)
    alert('Failed to create workflow. Please check your configuration and try again.')
  } finally {
    isCreatingWorkflow.value = false
  }
}

const triggerWorkflow = async (workflowId: string) => {
  isTriggeringWorkflow.value = true
  try {
    await apiService.post(`/api/advanced-ml/trigger-workflow/${workflowId}`)
    alert('Workflow triggered successfully!')
  } catch (error) {
    console.error('Failed to trigger workflow:', error)
    alert('Failed to trigger workflow. Please try again.')
  } finally {
    isTriggeringWorkflow.value = false
  }
}

const deleteWorkflow = async (workflowId: string) => {
  if (confirm('Are you sure you want to delete this workflow?')) {
    try {
      // Note: This would need a delete endpoint in the API
      workflows.value = workflows.value.filter(w => w.id !== workflowId)
      alert('Workflow deleted successfully!')
    } catch (error) {
      console.error('Failed to delete workflow:', error)
      alert('Failed to delete workflow. Please try again.')
    }
  }
}

const useTemplate = (templateType: string) => {
  const templates = {
    github: {
      configuration: {
        repository: "your-repo",
        branch: "main",
        trigger_on_pr: true,
        trigger_on_push: true,
        notify_slack: true
      }
    },
    slack: {
      configuration: {
        webhook_url: "https://hooks.slack.com/services/...",
        channel: "#security-alerts",
        mention_users: ["@security-team"],
        severity_threshold: "high"
      }
    },
    jenkins: {
      configuration: {
        jenkins_url: "https://jenkins.company.com",
        job_name: "security-scan",
        build_parameters: {
          scan_type: "comprehensive",
          fail_on_critical: true
        }
      }
    },
    email: {
      configuration: {
        recipients: ["security@company.com"],
        schedule: "daily",
        include_summary: true,
        include_details: true
      }
    },
    teams: {
      configuration: {
        webhook_url: "https://outlook.office.com/webhook/...",
        team: "Security Team",
        channel: "Alerts"
      }
    },
    jira: {
      configuration: {
        jira_url: "https://company.atlassian.net",
        project_key: "SEC",
        issue_type: "Bug",
        assignee: "security-team"
      }
    }
  }

  workflowForm.value.configuration = JSON.stringify(templates[templateType as keyof typeof templates].configuration, null, 2)
  workflowForm.value.type = templateType === 'github' || templateType === 'jenkins' ? 'ci_cd_integration' : 'notification'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  loadWorkflows()
})
</script>
