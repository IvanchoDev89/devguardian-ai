<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 pt-16">
    <div class="container mx-auto px-4 py-12">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-white mb-4">
          Simple, Transparent Pricing
        </h1>
        <p class="text-xl text-gray-400">
          Choose the plan that fits your security needs
        </p>
      </div>

      <!-- Pricing Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
        <div 
          v-for="plan in plans" 
          :key="plan.id"
          :class="[
            'rounded-2xl p-8 border transition-all duration-300',
            plan.popular 
              ? 'bg-gradient-to-b from-cyan-500/20 to-blue-500/20 border-cyan-500 transform scale-105' 
              : 'bg-slate-800/50 border-slate-700 hover:border-slate-600'
          ]"
        >
          <!-- Popular Badge -->
          <div v-if="plan.popular" class="text-center mb-4">
            <span class="bg-gradient-to-r from-cyan-500 to-blue-500 text-white text-sm font-semibold px-4 py-1 rounded-full">
              Most Popular
            </span>
          </div>

          <!-- Plan Name -->
          <h3 class="text-2xl font-bold text-white mb-2">{{ plan.name }}</h3>
          
          <!-- Price -->
          <div class="mb-6">
            <span class="text-5xl font-bold text-white">${{ plan.price }}</span>
            <span class="text-gray-400">/month</span>
          </div>

          <!-- Features -->
          <ul class="space-y-3 mb-8">
            <li 
              v-for="(feature, index) in plan.features" 
              :key="index"
              class="flex items-start gap-3 text-gray-300"
            >
              <svg class="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
              </svg>
              {{ feature }}
            </li>
          </ul>

          <!-- CTA Button -->
          <button
            @click="selectPlan(plan)"
            :class="[
              'w-full py-3 px-6 rounded-lg font-semibold transition-all duration-200',
              plan.popular
                ? 'bg-gradient-to-r from-cyan-500 to-blue-500 text-white hover:from-cyan-600 hover:to-blue-600'
                : 'bg-slate-700 text-white hover:bg-slate-600'
            ]"
          >
            {{ currentPlan === plan.id ? 'Current Plan' : 'Get Started' }}
          </button>
        </div>
      </div>

      <!-- FAQ Section -->
      <div class="mt-20 max-w-3xl mx-auto">
        <h2 class="text-3xl font-bold text-white text-center mb-12">
          Frequently Asked Questions
        </h2>
        
        <div class="space-y-6">
          <div v-for="faq in faqs" :key="faq.question" class="bg-slate-800/50 rounded-xl p-6 border border-slate-700">
            <h3 class="text-lg font-semibold text-white mb-2">{{ faq.question }}</h3>
            <p class="text-gray-400">{{ faq.answer }}</p>
          </div>
        </div>
      </div>

      <!-- Contact Sales -->
      <div class="mt-16 text-center">
        <p class="text-gray-400 mb-4">Need a custom solution?</p>
        <button class="bg-slate-700 hover:bg-slate-600 text-white px-8 py-3 rounded-lg font-semibold transition-colors">
          Contact Sales
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiService } from '../services/api'

const router = useRouter()

interface Plan {
  id: string
  name: string
  price: number
  features: string[]
  popular?: boolean
}

const plans = ref<Plan[]>([])
const currentPlan = ref('free')

const faqs = [
  {
    question: 'Can I change plans anytime?',
    answer: 'Yes, you can upgrade or downgrade your plan at any time. Changes take effect immediately.'
  },
  {
    question: 'What happens if I exceed my scan limit?',
    answer: 'You can purchase additional scans or upgrade to a higher plan. Scans will be paused until you have available quota.'
  },
  {
    question: 'Is there a free trial for Pro?',
    answer: 'Yes! New users get 14 days of Pro features free. No credit card required.'
  },
  {
    question: 'Do you offer annual billing?',
    answer: 'Yes, annual billing comes with a 20% discount. Contact sales for enterprise agreements.'
  },
  {
    question: 'What payment methods do you accept?',
    answer: 'We accept all major credit cards, PayPal, and wire transfers for enterprise plans.'
  }
]

const loadPlans = async () => {
  try {
    const response = await apiService.aiGet('/plans')
    if (response.success && response.data) {
      plans.value = response.data
    }
  } catch (error) {
    console.error('Failed to load plans:', error)
    plans.value = [
      {
        id: 'free',
        name: 'Free',
        price: 0,
        features: [
          '100 scans per month',
          'Basic vulnerability detection',
          'Email support',
          '1 user',
          'Public repositories only'
        ]
      },
      {
        id: 'pro',
        name: 'Pro',
        price: 29,
        popular: true,
        features: [
          '1,000 scans per month',
          'AI-powered fix suggestions',
          'Priority support',
          '5 users',
          'Private repositories',
          'API access'
        ]
      },
      {
        id: 'enterprise',
        name: 'Enterprise',
        price: 199,
        features: [
          '10,000 scans per month',
          'Everything in Pro',
          'Dedicated support',
          'Unlimited users',
          'On-premise deployment',
          'SSO/SAML'
        ]
      }
    ]
  }
}

const selectPlan = (plan: Plan) => {
  if (plan.id === 'free') {
    router.push('/billing')
  } else {
    router.push('/billing?plan=' + plan.id)
  }
}

onMounted(() => {
  loadPlans()
})
</script>
