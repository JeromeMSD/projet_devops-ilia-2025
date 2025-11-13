import { Routes, Route } from 'react-router';
import { Home } from './routes/Home';
import { Navbar } from './components/Navbar';
import { NotFound } from './routes/NotFound';
import { About } from './routes/About';
import IncidentCreatePage from '/Users/air/FrontendDevops/projet_devops-ilia-2025/frontend/src/routes/IncidentCreatePage.tsx';

export default function App() {
    return (
        <div
            className={`flex min-h-screen flex-col transition-colors duration-300 bg-gradient-to-b from-slate-50 via-white to-slate-100 text-slate-900 accent-[#2563eb]`}>
            <Navbar/>

            <main className="flex-1 px-4 py-10 md:px-8">
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/about" element={<About/>}/>
                    <Route path="/admin/incidents/new" element={<IncidentCreatePage/>}/>
                    <Route path="*" element={<NotFound/>}/>
                </Routes>
            </main>
        </div>
    );
}
