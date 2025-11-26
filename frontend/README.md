# Construction Realtime Monitoring - Frontend

React-based frontend application for the Construction Realtime Monitoring system.

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **TanStack Query** - Server state management
- **React Router** - Routing
- **Zustand** - Client state management
- **Axios** - HTTP client

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── api/           # API client and endpoints
│   ├── components/    # Reusable UI components
│   ├── pages/         # Page components
│   ├── store/         # State management (Zustand)
│   ├── types/         # TypeScript type definitions
│   ├── App.tsx        # Main app component
│   ├── main.tsx       # Entry point
│   └── index.css      # Global styles
├── public/            # Static assets
└── ...
```

## Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Features

- ✅ User authentication (Signup/Login)
- ✅ Protected routes
- ✅ Responsive design
- ✅ Type-safe API calls
- ✅ State management
- 🚧 Project management (coming soon)
- 🚧 Real-time monitoring (coming soon)
- 🚧 Team management (coming soon)

## Development

The app runs on `http://localhost:3000` by default. The Vite dev server proxies API requests to `http://localhost:8000`.

## Building for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

