import { apiClient } from './client'
import type { SignupRequest, SignupVerifyOTP, AuthResponse, LoginRequest } from '../types'

export const authApi = {
  // Signup - Request OTP
  signupRequest: async (data: SignupRequest): Promise<{ key: string }> => {
    return apiClient.post('/api/v1/signup', data)
  },

  // Signup - Verify OTP
  signupVerify: async (data: SignupVerifyOTP): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/api/v1/signup/verify-otp', data)
    
    // Store tokens
    if (response.access_token) {
      apiClient.setAccessToken(response.access_token)
    }
    if (response.refresh_token) {
      apiClient.setRefreshToken(response.refresh_token)
    }
    
    return response
  },

  // Login
  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/api/v1/auth/login', data)
    
    // Store tokens
    if (response.access_token) {
      apiClient.setAccessToken(response.access_token)
    }
    if (response.refresh_token) {
      apiClient.setRefreshToken(response.refresh_token)
    }
    
    return response
  },

  // Logout
  logout: (): void => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  },

  // Get current user
  getCurrentUser: async (): Promise<any> => {
    return apiClient.get('/api/v1/auth/me')
  },
}

