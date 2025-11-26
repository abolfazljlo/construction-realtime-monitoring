// Iranian National Code Validation
export function validateNationalCode(nationalCode: string): { valid: boolean; message?: string } {
  if (!nationalCode) {
    return { valid: false, message: 'کد ملی الزامی است' }
  }

  if (!/^\d{10}$/.test(nationalCode)) {
    return { valid: false, message: 'کد ملی باید ۱۰ رقم باشد' }
  }

  // Check if all digits are the same (invalid)
  if (/^(\d)\1{9}$/.test(nationalCode)) {
    return { valid: false, message: 'کد ملی معتبر نیست' }
  }

  // Validate check digit
  const check = parseInt(nationalCode[9])
  let sum = 0

  for (let i = 0; i < 9; i++) {
    sum += parseInt(nationalCode[i]) * (10 - i)
  }

  const remainder = sum % 11
  const isValid = remainder < 2 ? check === remainder : check === 11 - remainder

  if (!isValid) {
    return { valid: false, message: 'کد ملی معتبر نیست' }
  }

  return { valid: true }
}

// Iranian Mobile Number Validation
export function validateMobile(mobile: string): { valid: boolean; message?: string } {
  if (!mobile) {
    return { valid: false, message: 'شماره موبایل الزامی است' }
  }

  // Remove any spaces or dashes
  const cleaned = mobile.replace(/[\s-]/g, '')

  // Check if it starts with 09 (Iranian mobile format)
  if (/^09\d{9}$/.test(cleaned)) {
    return { valid: true }
  }

  // Check if it's in normalized format (9XXXXXXXXX)
  if (/^9\d{9}$/.test(cleaned)) {
    return { valid: true }
  }

  return { valid: false, message: 'شماره موبایل باید با ۰۹ شروع شود و ۱۱ رقم باشد' }
}

// Password Validation
export function validatePassword(password: string): { valid: boolean; message?: string } {
  if (!password) {
    return { valid: false, message: 'رمز عبور الزامی است' }
  }

  if (password.length < 8) {
    return { valid: false, message: 'رمز عبور باید حداقل ۸ کاراکتر باشد' }
  }

  if (!/[a-zA-Z]/.test(password) && !/[آ-ی]/.test(password)) {
    return { valid: false, message: 'رمز عبور باید حداقل یک حرف داشته باشد' }
  }

  if (!/\d/.test(password)) {
    return { valid: false, message: 'رمز عبور باید حداقل یک عدد داشته باشد' }
  }

  return { valid: true }
}

// Format mobile number for display/input
export function formatMobile(mobile: string): string {
  const cleaned = mobile.replace(/[\s-]/g, '')
  if (cleaned.startsWith('9') && cleaned.length === 10) {
    return `0${cleaned}`
  }
  return cleaned
}

