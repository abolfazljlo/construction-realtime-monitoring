import { useState, useRef, useEffect } from 'react'

interface PersianDatePickerProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
  className?: string
}

export default function PersianDatePicker({
  value,
  onChange,
  placeholder = '1371/01/01',
  className = '',
}: PersianDatePickerProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [selectedYear, setSelectedYear] = useState<number | null>(null)
  const [selectedMonth, setSelectedMonth] = useState<number | null>(null)
  const [selectedDay, setSelectedDay] = useState<number | null>(null)
  const wrapperRef = useRef<HTMLDivElement>(null)

  const persianMonths = [
    'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
    'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
  ]

  useEffect(() => {
    if (value) {
      const parts = value.split('/')
      if (parts.length === 3) {
        setSelectedYear(parseInt(parts[0]))
        setSelectedMonth(parseInt(parts[1]))
        setSelectedDay(parseInt(parts[2]))
      }
    }
  }, [value])

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const getDaysInMonth = (year: number, month: number): number => {
    if (month <= 6) return 31
    if (month <= 11) return 30
    // Check if it's a leap year (سال کبیسه) - Algorithm 33
    const remainder = year % 33
    const isLeap = remainder === 1 || remainder === 5 || remainder === 9 || remainder === 13 || 
                   remainder === 17 || remainder === 22 || remainder === 26 || remainder === 30
    return isLeap ? 30 : 29
  }

  const handleDateSelect = (year: number, month: number, day: number) => {
    const formatted = `${year}/${month.toString().padStart(2, '0')}/${day.toString().padStart(2, '0')}`
    onChange(formatted)
    setIsOpen(false)
  }

  const currentYear = 1403
  const years = Array.from({ length: 100 }, (_, i) => currentYear - i)
  const days = selectedYear && selectedMonth
    ? Array.from({ length: getDaysInMonth(selectedYear, selectedMonth) }, (_, i) => i + 1)
    : []

  return (
    <div className="relative" ref={wrapperRef}>
      <input
        type="text"
        value={value}
        readOnly
        onClick={() => setIsOpen(!isOpen)}
        className={`input cursor-pointer ${className}`}
        placeholder={placeholder}
        required
      />
      
      {isOpen && (
        <div className="absolute z-50 mt-2 bg-white border border-gray-300 rounded-lg shadow-lg p-4 w-80 max-h-96 overflow-y-auto">
          <div className="space-y-4">
            {/* Year Selector */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">سال</label>
              <select
                value={selectedYear || ''}
                onChange={(e) => {
                  setSelectedYear(parseInt(e.target.value))
                  setSelectedMonth(null)
                  setSelectedDay(null)
                }}
                className="input text-sm"
              >
                <option value="">انتخاب سال</option>
                {years.map((year) => (
                  <option key={year} value={year}>
                    {year}
                  </option>
                ))}
              </select>
            </div>

            {/* Month Selector */}
            {selectedYear && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">ماه</label>
                <select
                  value={selectedMonth || ''}
                  onChange={(e) => {
                    setSelectedMonth(parseInt(e.target.value))
                    setSelectedDay(null)
                  }}
                  className="input text-sm"
                >
                  <option value="">انتخاب ماه</option>
                  {persianMonths.map((month, index) => (
                    <option key={index + 1} value={index + 1}>
                      {month}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* Day Selector */}
            {selectedYear && selectedMonth && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">روز</label>
                <div className="grid grid-cols-7 gap-2">
                  {days.map((day) => (
                    <button
                      key={day}
                      type="button"
                      onClick={() => handleDateSelect(selectedYear!, selectedMonth!, day)}
                      className={`p-2 text-sm rounded hover:bg-primary-100 ${
                        selectedDay === day ? 'bg-primary-600 text-white' : 'bg-gray-100'
                      }`}
                    >
                      {day}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

