import { Link } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

export default function HomePage() {
  const { isAuthenticated } = useAuthStore()

  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">
        نظارت لحظه‌ای پروژه‌های ساختمانی
      </h1>
      <p className="text-xl text-gray-600 mb-8">
        پروژه‌های ساختمانی خود را به صورت لحظه‌ای با بینش‌های فوری و کنترل بهتر پروژه ردیابی کنید.
      </p>

      {isAuthenticated ? (
        <Link to="/dashboard" className="btn btn-primary text-lg px-8 py-3">
          رفتن به داشبورد
        </Link>
      ) : (
        <div className="flex justify-center gap-4">
          <Link to="/signup" className="btn btn-primary text-lg px-8 py-3">
            شروع کنید
          </Link>
          <Link to="/login" className="btn btn-secondary text-lg px-8 py-3">
            ورود
          </Link>
        </div>
      )}

      <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="card">
          <h3 className="text-xl font-semibold mb-2">ردیابی لحظه‌ای</h3>
          <p className="text-gray-600">
            پروژه‌های ساختمانی خود را با به‌روزرسانی‌های زنده و اعلان‌های فوری نظارت کنید.
          </p>
        </div>
        <div className="card">
          <h3 className="text-xl font-semibold mb-2">مدیریت تیم</h3>
          <p className="text-gray-600">
            نقش‌ها را اختصاص دهید، اعضای تیم را مدیریت کنید و وضعیت در محل را به صورت لحظه‌ای ردیابی کنید.
          </p>
        </div>
        <div className="card">
          <h3 className="text-xl font-semibold mb-2">کنترل پروژه</h3>
          <p className="text-gray-600">
            بینش‌های دقیق و زنده برای کنترل بهتر پروژه و تصمیم‌گیری دریافت کنید.
          </p>
        </div>
      </div>
    </div>
  )
}

