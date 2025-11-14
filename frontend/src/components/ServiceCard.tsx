import React from 'react';
import type { SVGProps } from 'react';
import { User, AlertTriangle, Megaphone, Cloud, Flag } from 'lucide-react';
import StatusBadge from './StatusBadge';
import type { Service } from '../utils/mockData';
import { Link } from 'react-router';

const iconMap: Record<string, React.ComponentType<SVGProps<SVGSVGElement>>> = {
    User,
    AlertTriangle,
    Megaphone,
    Cloud,
    Flag,
};

const ServiceCard: React.FC<{ service: Service }> = ({ service }) => {
    const Icon = iconMap[service.icon] ?? User;
    return (
        <article className="bg-white/80 border border-slate-200 rounded-xl shadow p-4 flex flex-col justify-between">
            <div className="flex items-start gap-4">
                <div className="p-2 rounded-md bg-slate-100">
                    <Icon className="w-6 h-6 text-slate-800" />
                </div>
                <div className="flex-1">
                    <h3 className="text-lg font-semibold">{service.name}</h3>
                    <p className="text-sm text-slate-600 mt-1">{service.description}</p>
                </div>
            </div>

            <div className="mt-4 flex items-center justify-between">
                <StatusBadge status={service.status} />
                {service.href ? (
                    <Link to={service.href} className="text-sm font-medium text-sky-600 hover:underline">
                        Voir
                    </Link>
                ) : null}
            </div>
        </article>
    );
};

export default ServiceCard;
