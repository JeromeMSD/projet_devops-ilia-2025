import { Routes, Route } from 'react-router';

import { Navbar } from '@/components/Navbar';
import { Home } from '@/routes/Home';
import { About } from '@/routes/About';
import { LoginPage } from '@/routes/LoginPage';
import { NotFound } from '@/routes/NotFound';
import { ProtectedRoute } from '@/routes/ProtectedRoute';
import { RegisterPage } from '@/routes/RegisterPage';
import { ForgotPasswordPage } from '@/routes/ForgotPasswordPage';
import { ResetPasswordPage } from '@/routes/ResetPasswordPage';
import ProfilePage from '@/routes/ProfilePage.tsx';
import DashboardPage from '@/routes/DashboardPage';
import IncidentsPage from '@/routes/IncidentsPage';
import IncidentCreatePage from '@/routes/IncidentCreatePage.tsx';

export default function App() {
    return (
        <div
            className={`flex min-h-screen flex-col transition-colors duration-300 bg-gradient-to-b from-slate-50 via-white to-slate-100 text-slate-900 accent-[#2563eb]`}>
            <Navbar />

            <main className="flex-1 flex justify-center items-center px-4 py-10 md:px-8">
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/me" element={(<ProtectedRoute><ProfilePage /></ProtectedRoute>)} />
                    <Route path="/about" element={<About />} />
                    <Route path="/incidents" element={<IncidentsPage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/forgot-password" element={<ForgotPasswordPage />} />
                    <Route path="/reset-password" element={<ResetPasswordPage />} />
                    <Route path="/dashboard" element={(<ProtectedRoute><DashboardPage /></ProtectedRoute>)} />
                    <Route path="/admin/incidents/new" element={<IncidentCreatePage/>}/>
                    {/* catch-all for unknown routes */}
                    <Route path="*" element={<NotFound />} />
                </Routes>
            </main>
        </div>
    );
}
