import { useAuthStore } from '../store/authStore'

export default function DashboardPage() {
  const { user } = useAuthStore()

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">داشبورد</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <div className="card">
          <h3 className="text-lg font-semibold mb-2">خوش آمدید!</h3>
          <p className="text-gray-600">
            {user?.first_name} {user?.last_name}
          </p>
        </div>
        
        <div className="card">
          <h3 className="text-lg font-semibold mb-2">پروژه‌ها</h3>
          <p className="text-3xl font-bold text-primary-600">۰</p>
          <p className="text-sm text-gray-500">پروژه‌های فعال</p>
        </div>
        
        <div className="card">
          <h3 className="text-lg font-semibold mb-2">اعضای تیم</h3>
          <p className="text-3xl font-bold text-primary-600">۰</p>
          <p className="text-sm text-gray-500">کل اعضا</p>
        </div>
      </div>

      <div className="card">
        <h2 className="text-xl font-semibold mb-4">اطلاعات کاربر</h2>
        <div className="space-y-2">
          <div className="flex justify-between">
            <span className="text-gray-600">شماره موبایل:</span>
            <span className="font-medium">{user?.mobile}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">کد ملی:</span>
            <span className="font-medium">{user?.national_code}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">وضعیت:</span>
            <span className={`font-medium ${user?.is_active ? 'text-green-600' : 'text-red-600'}`}>
              {user?.is_active ? 'فعال' : 'غیرفعال'}
            </span>
          </div>
        </div>
      </div>

      <div className="mt-8 card">
        <h2 className="text-xl font-semibold mb-4">به زودی</h2>
        <p className="text-gray-600">
          مدیریت پروژه، اختصاص تیم و ویژگی‌های نظارت لحظه‌ای به زودی در دسترس خواهد بود.
        </p>
      </div>
    </div>
  )
}

