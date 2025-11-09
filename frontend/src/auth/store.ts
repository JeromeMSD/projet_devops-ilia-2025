import createAuthStore from 'react-auth-kit/store/createAuthStore';

const store = createAuthStore('localstorage', {
    authName: '_auth',
    cookieDomain: window.location.hostname,
    cookieSecure: window.location.protocol === 'https:',
});

export default store;
