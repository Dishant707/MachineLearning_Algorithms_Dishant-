
import { getSession } from '@/lib/session';
import { redirect } from 'next/navigation';
import Dashboard from '@/components/Dashboard';

export default async function HomePage() {
  const session = await getSession();

  if (!session.user) {
    redirect('/login');
  }

  return (
    <div className="flex flex-col items-center min-h-screen">
      <nav className="w-full bg-white/10 backdrop-blur-md border-b border-white/20 shadow-lg">
        <div className="container flex items-center justify-between p-4 mx-auto max-w-7xl">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h1 className="text-2xl font-bold text-white">Password Manager</h1>
          </div>
          <div className="flex items-center space-x-4">
            <div className="hidden sm:flex items-center px-4 py-2 bg-white/20 rounded-lg backdrop-blur-sm">
              <svg className="w-5 h-5 text-white mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span className="text-white font-medium">{session.user.email}</span>
            </div>
            <a
              href="/api/auth/logout"
              className="px-5 py-2 font-semibold text-purple-600 bg-white rounded-lg hover:bg-gray-100 transition-all duration-200 transform hover:scale-105 shadow-md"
            >
              Logout
            </a>
          </div>
        </div>
      </nav>
      <main className="container flex-grow p-4 mx-auto flex items-start justify-center pt-8">
        <Dashboard />
      </main>
    </div>
  );
}
