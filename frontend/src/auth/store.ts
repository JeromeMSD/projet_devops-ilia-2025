import createAuthStore from 'react-auth-kit/store/createAuthStore';

const store = createAuthStore('localstorage', {
    authName: '_auth',
});

export default store;
