import React from 'react';

export const StatusBadge: React.FC<{ status: 'operational' | 'partial' | 'down' }> = ({ status }) => {
    const map = {
        operational: { text: 'Operational', className: 'bg-green-600 text-white' },
        partial: { text: 'Partial', className: 'bg-yellow-500 text-black' },
        down: { text: 'Down', className: 'bg-red-600 text-white' },
    } as const;

    const info = map[status];

    return (
        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${info.className}`}>
            {info.text}
        </span>
    );
};

export default StatusBadge;
