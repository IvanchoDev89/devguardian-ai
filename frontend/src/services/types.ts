// Type definitions for DevGuardian AI API responses

export interface User {
  id: string
  name: string
  email: string
  created_at: string
  updated_at: string
}

export interface Repository {
  id: string
  name: string
  url: string
  provider: 'github' | 'gitlab' | 'bitbucket'
  owner: string
  description?: string
  is_active: boolean
  last_scan_at?: string
  created_at: string
  updated_at: string
}

export interface Vulnerability {
  id: string
  repository_id?: string
  title: string
  description: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  cwe_id?: string
  file_path?: string
  line_number?: number
  code_snippet?: string
  status: 'open' | 'fixed' | 'ignored'
  discovered_at: string
  created_at: string
  updated_at: string
}

export interface AiFix {
  id: string
  vulnerability_id: string
  repository_id?: string
  title: string
  description: string
  fixed_code?: string
  explanation?: string
  recommendations?: string[]
  diff_content?: string
  confidence_score?: number
  status: 'pending' | 'applied' | 'failed'
  created_at: string
  updated_at: string
}

export interface SecurityEvent {
  id: string
  type: string
  description: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  metadata?: Record<string, any>
  resolved_at?: string
  created_at: string
}

export interface Organization {
  id: string
  name: string
  slug: string
  description?: string
  created_at: string
  updated_at: string
}

export interface ApiResponse<T> {
  data: T
  message?: string
  status?: string
}

export interface PaginatedResponse<T> {
  data: T[]
  current_page: number
  last_page: number
  per_page: number
  total: number
}

export interface ErrorResponse {
  error: string
  message?: string
  details?: Record<string, any>
}

// API request types
export interface CreateRepositoryRequest {
  name: string
  url: string
  provider: 'github' | 'gitlab' | 'bitbucket'
  description?: string
}

export interface ScanRepositoryRequest {
  repository_id: string
  scan_type?: 'full' | 'incremental'
}

export interface GenerateAiFixRequest {
  vulnerability_id: string
  options?: {
    include_explanation?: boolean
    include_recommendations?: boolean
  }
}

export interface ApplyAiFixRequest {
  fix_id: string
  auto_commit?: boolean
}
