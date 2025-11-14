export type ServiceStatus = 'operational' | 'partial' | 'down';

export type Service = {
    id: string;
    name: string;
    description: string;
    status: ServiceStatus;
    icon: string;
    href?: string;
};

export const mockServices: Service[] = [
    {
        id: 'svc-users',
        name: 'User Service',
        description: 'Gestion des comptes, rôles et authentification',
        status: 'operational',
        icon: 'User',
        href: '/users',
    },
    {
        id: 'svc-incidents',
        name: 'Incident Service',
        description: 'Création, suivi, assignation et timeline des incidents',
        status: 'partial',
        icon: 'AlertTriangle',
        href: '/incidents',
    },
    {
        id: 'svc-comms',
        name: 'Communication Service',
        description: 'Annonces publiques, webhooks et abonnements email',
        status: 'down',
        icon: 'Megaphone',
        href: '/comms',
    },
    {
        id: 'svc-csp',
        name: 'CSP Ingestor',
        description: 'Surveillance des status pages de fournisseurs cloud',
        status: 'operational',
        icon: 'Cloud',
        href: '/csp',
    },
    {
        id: 'svc-flags',
        name: 'Flags Service',
        description: 'Feature flags et toggle pour fonctionnalités expérimentales',
        status: 'operational',
        icon: 'Flag',
        href: '/flags',
    },
];

// ✅ Ajout du mockUser pour le ProfilePage
export const mockUser = {
    firstname: 'Sebastien',
    lastname: 'Lacroix',
};
