import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { authApi } from '../api/auth'
import { useAuthStore } from '../store/authStore'
import { validateNationalCode } from '../utils/validation'
import type { LoginRequest } from '../types'

export default function LoginPage() {
  const navigate = useNavigate()
  const { setUser } = useAuthStore()
  const [formData, setFormData] = useState<LoginRequest>({
    national_code: '',
    password: '',
  })
  const [errors, setErrors] = useState<{
    national_code?: string
    password?: string
  }>({})

  const loginMutation = useMutation({
    mutationFn: (data: LoginRequest) => authApi.login(data),
    onSuccess: (response) => {
      setUser(response.user)
      navigate('/dashboard')
    },
    onError: (error: any) => {
      alert(error.response?.data?.detail || 'ورود با خطا مواجه شد. لطفاً اطلاعات خود را بررسی کنید.')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    // Validate fields
    const newErrors: typeof errors = {}
    
    const nationalCodeValidation = validateNationalCode(formData.national_code)
    if (!nationalCodeValidation.valid) {
      newErrors.national_code = nationalCodeValidation.message
    }
    
    if (!formData.password) {
      newErrors.password = 'رمز عبور الزامی است'
    }
    
    setErrors(newErrors)
    
    // If there are errors, don't submit
    if (Object.keys(newErrors).length > 0) {
      return
    }
    
    loginMutation.mutate(formData)
  }

  const handleNationalCodeChange = (value: string) => {
    setFormData({ ...formData, national_code: value })
    if (errors.national_code) {
      const validation = validateNationalCode(value)
      if (validation.valid) {
        setErrors({ ...errors, national_code: undefined })
      } else {
        setErrors({ ...errors, national_code: validation.message })
      }
    }
  }

  return (
    <div className="max-w-md mx-auto">
      <div className="card">
        <h2 className="text-2xl font-bold mb-6">ورود</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="national_code" className="block text-sm font-medium text-gray-700 mb-2">
              کد ملی
            </label>
            <input
              id="national_code"
              type="text"
              value={formData.national_code}
              onChange={(e) => handleNationalCodeChange(e.target.value)}
              onBlur={() => {
                const validation = validateNationalCode(formData.national_code)
                if (!validation.valid) {
                  setErrors({ ...errors, national_code: validation.message })
                }
              }}
              className={`input ${errors.national_code ? 'border-red-500 focus:ring-red-500' : ''}`}
              placeholder="کد ملی ۱۰ رقمی"
              maxLength={10}
              required
            />
            {errors.national_code && (
              <p className="text-red-500 text-xs mt-1">{errors.national_code}</p>
            )}
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
              رمز عبور
            </label>
            <input
              id="password"
              type="password"
              value={formData.password}
              onChange={(e) => {
                setFormData({ ...formData, password: e.target.value })
                if (errors.password && e.target.value) {
                  setErrors({ ...errors, password: undefined })
                }
              }}
              onBlur={() => {
                if (!formData.password) {
                  setErrors({ ...errors, password: 'رمز عبور الزامی است' })
                }
              }}
              className={`input ${errors.password ? 'border-red-500 focus:ring-red-500' : ''}`}
              placeholder="رمز عبور خود را وارد کنید"
              required
            />
            {errors.password && (
              <p className="text-red-500 text-xs mt-1">{errors.password}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={loginMutation.isPending}
            className="btn btn-primary w-full"
          >
            {loginMutation.isPending ? 'در حال ورود...' : 'ورود'}
          </button>
        </form>
      </div>
    </div>
  )
}

