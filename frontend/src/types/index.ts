// User types
export interface User {
  id: number
  mobile: string
  national_code: string
  birthday_date: string
  first_name: string
  last_name: string
  is_active: boolean
  created_at: string
  updated_at: string
}

// Auth types
export interface SignupRequest {
  mobile: string
  password: string
  national_code: string
  birthday_jalali: string
}

export interface SignupVerifyOTP {
  key: string
  otp: string
}

export interface AuthResponse {
  user: User
  access_token: string
  refresh_token: string
}

export interface LoginRequest {
  national_code: string
  password: string
}

// API Response types
export interface ApiResponse<T> {
  data?: T
  message?: string
  error?: string
}

// Project types (for future implementation)
export interface Project {
  id: number
  name: string
  description?: string
  status: 'active' | 'completed' | 'on_hold'
  created_at: string
  updated_at: string
}

