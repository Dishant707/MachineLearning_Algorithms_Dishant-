
'use client';

import { useState, useEffect } from 'react';

interface Credential {
  id: number;
  service: string;
  username: string;
  password: string;
}

export default function Dashboard() {
  const [credentials, setCredentials] = useState<Credential[]>([]);
  const [service, setService] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [visiblePasswords, setVisiblePasswords] = useState<Set<number>>(new Set());
  const [copiedId, setCopiedId] = useState<number | null>(null);

  useEffect(() => {
    fetchCredentials();
  }, []);

  const fetchCredentials = async () => {
    const res = await fetch('/api/credentials');
    if (res.ok) {
      const data = await res.json();
      setCredentials(data);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    const res = await fetch('/api/credentials', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ service, username, password }),
    });

    if (res.ok) {
      fetchCredentials();
      setService('');
      setUsername('');
      setPassword('');
    } else {
      const { error } = await res.json();
      setError(error);
    }
  };

  const handleDelete = async (id: number) => {
    const res = await fetch(`/api/credentials/${id}`, {
      method: 'DELETE',
    });

    if (res.ok) {
      fetchCredentials();
    } else {
      const { error } = await res.json();
      alert(`Error deleting credential: ${error}`);
    }
  };

  const generatePassword = () => {
    const length = 16;
    const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+~`|}{[]:;?><,./-=";
    let newPassword = "";
    for (let i = 0, n = charset.length; i < length; ++i) {
      newPassword += charset.charAt(Math.floor(Math.random() * n));
    }
    setPassword(newPassword);
  };

  const togglePasswordVisibility = (id: number) => {
    const newVisible = new Set(visiblePasswords);
    if (newVisible.has(id)) {
      newVisible.delete(id);
    } else {
      newVisible.add(id);
    }
    setVisiblePasswords(newVisible);
  };

  const copyToClipboard = async (text: string, id: number) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedId(id);
      setTimeout(() => setCopiedId(null), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    <div className="w-full max-w-5xl p-4 sm:p-8 space-y-8">
      {/* Header */}
      <div className="text-center mb-2">
        <div className="inline-flex items-center justify-center mb-4">
          <div className="p-4 bg-white rounded-2xl shadow-2xl">
            <svg className="w-12 h-12 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
        </div>
        <h1 className="text-5xl font-extrabold text-white mb-3 drop-shadow-lg">
          🔐 Password Vault
        </h1>
        <p className="text-white/90 text-lg font-medium">Manage your credentials securely</p>
      </div>

      {/* Credentials List */}
      <div className="bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-6 border border-white/20">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-800 flex items-center">
            <svg className="w-6 h-6 mr-2 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            Your Credentials
          </h2>
          <span className="px-3 py-1 text-sm font-semibold text-purple-600 bg-purple-100 rounded-full">
            {credentials.length} {credentials.length === 1 ? 'item' : 'items'}
          </span>
        </div>
        
        {credentials.length === 0 ? (
          <div className="text-center py-12">
            <svg className="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
            </svg>
            <p className="text-gray-500 text-lg">No credentials yet</p>
            <p className="text-gray-400 text-sm mt-1">Add your first credential below</p>
          </div>
        ) : (
          <div className="space-y-4">
            {credentials.map((cred) => (
              <div key={cred.id} className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl border-2 border-purple-200 hover:shadow-lg transition-all duration-200 overflow-hidden">
                <div className="p-5">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center space-x-4 flex-1">
                      <div className="w-14 h-14 bg-gradient-to-br from-purple-500 to-blue-500 rounded-xl flex items-center justify-center shadow-md flex-shrink-0">
                        <span className="text-white font-bold text-xl">{cred.service.charAt(0).toUpperCase()}</span>
                      </div>
                      <div className="flex-1">
                        <p className="font-bold text-gray-900 text-xl mb-1">{cred.service}</p>
                        <div className="flex items-center text-sm text-gray-600">
                          <svg className="w-4 h-4 mr-1.5 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                          </svg>
                          <span className="font-medium">{cred.username}</span>
                        </div>
                      </div>
                    </div>
                    <button
                      onClick={() => handleDelete(cred.id)}
                      className="px-4 py-2 text-sm font-semibold text-white bg-gradient-to-r from-red-500 to-pink-500 rounded-lg hover:from-red-600 hover:to-pink-600 transition-all duration-200 transform hover:scale-105 shadow-md flex-shrink-0"
                    >
                      🗑️ Delete
                    </button>
                  </div>
                  
                  {/* Password Section */}
                  <div className="bg-white/80 rounded-lg p-4 border border-purple-200">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3 flex-1">
                        <svg className="w-5 h-5 text-purple-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                        </svg>
                        <div className="flex-1 min-w-0">
                          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Password</p>
                          <p className="font-mono text-lg font-bold text-gray-900 break-all">
                            {visiblePasswords.has(cred.id) ? cred.password : '••••••••••••'}
                          </p>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-2 ml-4">
                        <button
                          onClick={() => togglePasswordVisibility(cred.id)}
                          className="p-2.5 bg-gradient-to-r from-purple-100 to-blue-100 rounded-lg hover:from-purple-200 hover:to-blue-200 transition-all duration-200 transform hover:scale-110"
                          title={visiblePasswords.has(cred.id) ? "Hide password" : "Show password"}
                        >
                          {visiblePasswords.has(cred.id) ? (
                            <svg className="w-5 h-5 text-purple-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                            </svg>
                          ) : (
                            <svg className="w-5 h-5 text-purple-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                            </svg>
                          )}
                        </button>
                        
                        <button
                          onClick={() => copyToClipboard(cred.password, cred.id)}
                          className={`p-2.5 rounded-lg transition-all duration-200 transform hover:scale-110 ${
                            copiedId === cred.id 
                              ? 'bg-gradient-to-r from-green-400 to-emerald-500' 
                              : 'bg-gradient-to-r from-blue-100 to-purple-100 hover:from-blue-200 hover:to-purple-200'
                          }`}
                          title="Copy password"
                        >
                          {copiedId === cred.id ? (
                            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                            </svg>
                          ) : (
                            <svg className="w-5 h-5 text-blue-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                            </svg>
                          )}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Add New Credential Form */}
      <div className="bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-6 border border-white/20">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center">
          <svg className="w-6 h-6 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Add New Credential
        </h2>
        
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label htmlFor="service" className="block text-sm font-semibold text-gray-700 mb-2">
              Service Name
            </label>
            <input 
              id="service" 
              type="text" 
              value={service} 
              onChange={(e) => setService(e.target.value)} 
              required 
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 outline-none text-gray-900"
              placeholder="e.g., Gmail, GitHub, Netflix"
            />
          </div>
          
          <div>
            <label htmlFor="username" className="block text-sm font-semibold text-gray-700 mb-2">
              Username or Email
            </label>
            <input 
              id="username" 
              type="text" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
              required 
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 outline-none text-gray-900"
              placeholder="your@email.com"
            />
          </div>
          
          <div>
            <label htmlFor="password" className="block text-sm font-semibold text-gray-700 mb-2">
              Password
            </label>
            <div className="flex gap-2">
              <input 
                id="password" 
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
                required 
                className="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 outline-none text-gray-900"
                placeholder="••••••••"
              />
              <button 
                type="button" 
                onClick={generatePassword} 
                className="px-4 py-3 font-semibold text-white bg-gradient-to-r from-green-500 to-emerald-600 rounded-xl hover:from-green-600 hover:to-emerald-700 transition-all duration-200 transform hover:scale-105 shadow-md whitespace-nowrap"
              >
                🎲 Generate
              </button>
            </div>
          </div>
          
          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-600 flex items-center">
                <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                {error}
              </p>
            </div>
          )}
          
          <button 
            type="submit" 
            className="w-full px-6 py-3 font-semibold text-white bg-gradient-to-r from-purple-600 to-blue-500 rounded-xl hover:from-purple-700 hover:to-blue-600 focus:outline-none focus:ring-4 focus:ring-purple-300 transition-all duration-200 transform hover:scale-[1.02] shadow-lg"
          >
            Add Credential
          </button>
        </form>
      </div>
    </div>
  );
}
