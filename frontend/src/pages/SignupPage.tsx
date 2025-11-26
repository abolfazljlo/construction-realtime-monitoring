import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { authApi } from '../api/auth'
import PersianDatePicker from '../components/PersianDatePicker'
import { validateNationalCode, validateMobile, validatePassword, formatMobile } from '../utils/validation'
import type { SignupRequest, SignupVerifyOTP } from '../types'

export default function SignupPage() {
  const navigate = useNavigate()
  const [step, setStep] = useState<'request' | 'verify'>('request')
  const [signupKey, setSignupKey] = useState<string>('')
  const [formData, setFormData] = useState<SignupRequest>({
    mobile: '',
    password: '',
    national_code: '',
    birthday_jalali: '',
  })
  const [otp, setOtp] = useState('')
  const [errors, setErrors] = useState<{
    national_code?: string
    password?: string
    mobile?: string
    birthday_jalali?: string
  }>({})

  // Request OTP mutation
  const requestOtpMutation = useMutation({
    mutationFn: (data: SignupRequest) => authApi.signupRequest(data),
    onSuccess: (response) => {
      setSignupKey(response.key)
      setStep('verify')
    },
    onError: (error: any) => {
      alert(error.response?.data?.detail || 'ثبت‌نام با خطا مواجه شد. لطفاً دوباره تلاش کنید.')
    },
  })

  // Verify OTP mutation
  const verifyOtpMutation = useMutation({
    mutationFn: (data: SignupVerifyOTP) => authApi.signupVerify(data),
    onSuccess: () => {
      navigate('/dashboard')
    },
    onError: (error: any) => {
      alert(error.response?.data?.detail || 'تایید کد یکبار مصرف با خطا مواجه شد.')
    },
  })

  const handleRequestSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    // Validate all fields
    const newErrors: typeof errors = {}
    
    const nationalCodeValidation = validateNationalCode(formData.national_code)
    if (!nationalCodeValidation.valid) {
      newErrors.national_code = nationalCodeValidation.message
    }
    
    const passwordValidation = validatePassword(formData.password)
    if (!passwordValidation.valid) {
      newErrors.password = passwordValidation.message
    }
    
    const mobileValidation = validateMobile(formData.mobile)
    if (!mobileValidation.valid) {
      newErrors.mobile = mobileValidation.message
    }
    
    if (!formData.birthday_jalali) {
      newErrors.birthday_jalali = 'تاریخ تولد الزامی است'
    }
    
    setErrors(newErrors)
    
    // If there are errors, don't submit
    if (Object.keys(newErrors).length > 0) {
      return
    }
    
    // Format mobile before sending
    const formattedData = {
      ...formData,
      mobile: formatMobile(formData.mobile)
    }
    
    requestOtpMutation.mutate(formattedData)
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

  const handlePasswordChange = (value: string) => {
    setFormData({ ...formData, password: value })
    if (errors.password) {
      const validation = validatePassword(value)
      if (validation.valid) {
        setErrors({ ...errors, password: undefined })
      } else {
        setErrors({ ...errors, password: validation.message })
      }
    }
  }

  const handleMobileChange = (value: string) => {
    setFormData({ ...formData, mobile: value })
    if (errors.mobile) {
      const validation = validateMobile(value)
      if (validation.valid) {
        setErrors({ ...errors, mobile: undefined })
      } else {
        setErrors({ ...errors, mobile: validation.message })
      }
    }
  }

  const handleVerifySubmit = (e: React.FormEvent) => {
    e.preventDefault()
    verifyOtpMutation.mutate({ key: signupKey, otp })
  }

  if (step === 'verify') {
    return (
      <div className="max-w-md mx-auto">
        <div className="card">
          <h2 className="text-2xl font-bold mb-6">تایید کد یکبار مصرف</h2>
          <p className="text-gray-600 mb-4">
            کد یکبار مصرف به شماره موبایل شما ارسال شد. لطفاً آن را وارد کنید.
          </p>
          <form onSubmit={handleVerifySubmit} className="space-y-4">
            <div>
              <label htmlFor="otp" className="block text-sm font-medium text-gray-700 mb-2">
                کد یکبار مصرف
              </label>
              <input
                id="otp"
                type="text"
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                className="input"
                placeholder="کد ۶ رقمی را وارد کنید"
                maxLength={6}
                required
              />
            </div>
            <button
              type="submit"
              disabled={verifyOtpMutation.isPending}
              className="btn btn-primary w-full"
            >
              {verifyOtpMutation.isPending ? 'در حال تایید...' : 'تایید کد'}
            </button>
            <button
              type="button"
              onClick={() => setStep('request')}
              className="btn btn-secondary w-full"
            >
              بازگشت
            </button>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-md mx-auto">
      <div className="card">
        <h2 className="text-2xl font-bold mb-6">ایجاد حساب کاربری</h2>
        <form onSubmit={handleRequestSubmit} className="space-y-4">
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
              onChange={(e) => handlePasswordChange(e.target.value)}
              onBlur={() => {
                const validation = validatePassword(formData.password)
                if (!validation.valid) {
                  setErrors({ ...errors, password: validation.message })
                }
              }}
              className={`input ${errors.password ? 'border-red-500 focus:ring-red-500' : ''}`}
              placeholder="رمز عبور خود را وارد کنید"
              required
            />
            {errors.password && (
              <p className="text-red-500 text-xs mt-1">{errors.password}</p>
            )}
            {!errors.password && formData.password && (
              <p className="text-gray-500 text-xs mt-1">
                حداقل ۸ کاراکتر، شامل حرف و عدد
              </p>
            )}
          </div>

          <div>
            <label htmlFor="mobile" className="block text-sm font-medium text-gray-700 mb-2">
              شماره موبایل
            </label>
            <input
              id="mobile"
              type="tel"
              value={formData.mobile}
              onChange={(e) => handleMobileChange(e.target.value)}
              onBlur={() => {
                const validation = validateMobile(formData.mobile)
                if (!validation.valid) {
                  setErrors({ ...errors, mobile: validation.message })
                }
              }}
              className={`input ${errors.mobile ? 'border-red-500 focus:ring-red-500' : ''}`}
              placeholder="09123456789"
              required
            />
            {errors.mobile && (
              <p className="text-red-500 text-xs mt-1">{errors.mobile}</p>
            )}
          </div>

          <div>
            <label htmlFor="birthday_jalali" className="block text-sm font-medium text-gray-700 mb-2">
              تاریخ تولد (شمسی)
            </label>
            <PersianDatePicker
              value={formData.birthday_jalali}
              onChange={(value) => {
                setFormData({ ...formData, birthday_jalali: value })
                if (errors.birthday_jalali && value) {
                  setErrors({ ...errors, birthday_jalali: undefined })
                }
              }}
              placeholder="1371/01/01"
              className={errors.birthday_jalali ? 'border-red-500 focus:ring-red-500' : ''}
            />
            {errors.birthday_jalali && (
              <p className="text-red-500 text-xs mt-1">{errors.birthday_jalali}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={requestOtpMutation.isPending}
            className="btn btn-primary w-full"
          >
            {requestOtpMutation.isPending ? 'در حال ارسال کد...' : 'ثبت‌نام'}
          </button>
        </form>
      </div>
    </div>
  )
}

