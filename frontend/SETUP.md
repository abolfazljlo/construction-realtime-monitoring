# Frontend Setup Guide

## Quick Start

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Set Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env and set VITE_API_BASE_URL if needed
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

4. **Open Browser**
   - Navigate to `http://localhost:3000`

## What's Included

### ✅ Complete Setup
- Vite + React + TypeScript
- Tailwind CSS configured
- React Router for navigation
- TanStack Query for API state
- Zustand for client state
- Axios HTTP client with interceptors
- Protected routes
- Authentication flow

### 📁 Project Structure
```
frontend/
├── src/
│   ├── api/              # API client & endpoints
│   │   ├── client.ts     # Axios instance with interceptors
│   │   └── auth.ts       # Authentication API calls
│   ├── components/        # Reusable components
│   │   └── Layout.tsx    # Main layout with navigation
│   ├── pages/            # Page components
│   │   ├── HomePage.tsx
│   │   ├── SignupPage.tsx
│   │   ├── LoginPage.tsx
│   │   └── DashboardPage.tsx
│   ├── store/            # State management
│   │   └── authStore.ts  # Auth state with Zustand
│   ├── types/            # TypeScript types
│   │   └── index.ts
│   ├── App.tsx           # Main app with routes
│   └── main.tsx         # Entry point
├── public/               # Static assets
└── ...
```

### 🎨 Features Implemented

1. **Authentication**
   - Signup with OTP verification
   - Login
   - Protected routes
   - Token management (localStorage)

2. **UI Components**
   - Responsive navigation
   - Form components
   - Card layouts
   - Tailwind CSS styling

3. **State Management**
   - TanStack Query for server state
   - Zustand for client state (auth)

### 🔧 Configuration

- **Port**: 3000 (configurable in `vite.config.ts`)
- **API Proxy**: `/api` routes proxy to `http://localhost:8000`
- **TypeScript**: Strict mode enabled
- **Tailwind**: Custom primary color scheme

### 📝 Next Steps

1. **Connect to Backend**
   - Ensure backend is running on port 8000
   - Update API endpoints if needed in `src/api/auth.ts`

2. **Add More Features**
   - Project management pages
   - Real-time monitoring components
   - Team management UI

3. **Customize**
   - Update colors in `tailwind.config.js`
   - Add more components in `src/components/`
   - Extend API client in `src/api/`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Troubleshooting

### Port Already in Use
Change port in `vite.config.ts`:
```typescript
server: {
  port: 3001, // Change to available port
}
```

### API Connection Issues
- Check backend is running on port 8000
- Verify `VITE_API_BASE_URL` in `.env`
- Check CORS settings in backend

### TypeScript Errors
- Run `npm install` to ensure all types are installed
- Check `tsconfig.json` for path aliases

