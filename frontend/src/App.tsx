import { Routes, Route } from 'react-router';

import { Navbar } from '@/components/Navbar';
import { Home } from '@/routes/Home';
import { About } from '@/routes/About';
import { LoginPage } from '@/routes/LoginPage';
import { NotFound } from '@/routes/NotFound';
import { Dashboard } from '@/routes/Dashboard';
import { ProtectedRoute } from '@/routes/ProtectedRoute';

export default function App() {
    return (
        <div
            className={`flex min-h-screen flex-col transition-colors duration-300 bg-gradient-to-b from-slate-50 via-white to-slate-100 text-slate-900 accent-[#2563eb]`}>
            <Navbar/>

            <main className="flex-1 flex justify-center items-center px-4 py-10 md:px-8">
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/login" element={<LoginPage/>}/>
                    <Route
                        path="/dashboard"
                        element={(
                            <ProtectedRoute>
                                <Dashboard/>
                            </ProtectedRoute>
                        )}
                    />

                    <Route path="/about" element={<About/>}/>
                    {/* catch-all for unknown routes */}
                    <Route path="*" element={<NotFound/>}/>
                </Routes>
            </main>
        </div>
    );
}
