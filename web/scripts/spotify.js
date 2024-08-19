document.addEventListener('DOMContentLoaded', async function() {
    const WEATHER_KEY = CONFIG.WEATHER_KEY;
    const clientId = CONFIG.CLIENT_ID;
    const redirectUrl = CONFIG.REDIRECT_URL;

    const tokenEndpoint = "https://accounts.spotify.com/api/token";
    const authorizationEndpoint = "https://accounts.spotify.com/authorize";
    const scope = 'user-top-read';

    // Data structure that manages the current active token, caching it in localStorage
    const currentToken = {
        get access_token() { return localStorage.getItem('spotify_access_token') || null; },
        get refresh_token() { return localStorage.getItem('spotify_refresh_token') || null; },
        get expires_in() { return localStorage.getItem('spotify_expires_in') || null },
        get expires() { return localStorage.getItem('spotify_expires') || null },
    
        save: function (response) {
        const { access_token, refresh_token, expires_in } = response;

        localStorage.setItem('spotify_access_token', access_token);
        localStorage.setItem('spotify_refresh_token', refresh_token);
        localStorage.setItem('spotify_expires_in', expires_in);

        const now = new Date();
        const expiry = new Date(now.getTime() + (expires_in * 1000));
        localStorage.setItem('spotify_expires', expiry);
        }
    };


    async function redirectToSpotifyAuthorize() {
        const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        const randomValues = crypto.getRandomValues(new Uint8Array(64));
        const randomString = randomValues.reduce((acc, x) => acc + possible[x % possible.length], "");
    
        const code_verifier = randomString;
        const data = new TextEncoder().encode(code_verifier);
        const hashed = await crypto.subtle.digest('SHA-256', data);
    
        const code_challenge_base64 = btoa(String.fromCharCode(...new Uint8Array(hashed)))
        .replace(/=/g, '')
        .replace(/\+/g, '-')
        .replace(/\//g, '_');
    
        window.localStorage.setItem('code_verifier', code_verifier);
    
        const authUrl = new URL(authorizationEndpoint)
        const params = {
            response_type: 'code',
            client_id: clientId,
            scope: scope,
            code_challenge_method: 'S256',
            code_challenge: code_challenge_base64,
            redirect_uri: redirectUrl,
        };
    
        authUrl.search = new URLSearchParams(params).toString();
        window.location.href = authUrl.toString();
    }


    // On page load, try to fetch auth code from current browser search URL
    const args = new URLSearchParams(window.location.search);
    const code = args.get('code');

    if (code) {
        try {
            const token = await getToken(code);
            currentToken.save(token);
        } catch (error) {
            console.error(error);
        }
    
        // Remove code from URL so we can refresh correctly.
        const url = new URL(window.location.href);
        url.searchParams.delete("code");
    
        const updatedUrl = url.search ? url.href : url.href.replace('?', '');
        window.history.replaceState({}, document.title, updatedUrl);
    }
    
    async function getToken(code) {
        const code_verifier = window.localStorage.getItem('code_verifier');
        // window.localStorage.removeItem('code_verifier');
    
        const response = await fetch(tokenEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                client_id: clientId,
                grant_type: 'authorization_code',
                code: code,
                redirect_uri: redirectUrl,
                code_verifier: code_verifier,
            }),
        });
    
        let token = await response.json();
        console.log(token);
        return token;
    }

    async function refreshToken() {
        const response = await fetch(tokenEndpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: new URLSearchParams({
            client_id: clientId,
            grant_type: 'refresh_token',
            refresh_token: currentToken.refresh_token
          }),
        });
      
        return await response.json();
    }

    const isTokenExpired = () => {
        const expiry = currentToken.expires;
      
        const now = new Date();
        const expiryDate = new Date(expiry);
      
        return now >= expiryDate;
    }

    document.getElementById('flow').addEventListener('click', async (event) => {
        event.preventDefault();

        if (currentToken.access_token == 'undefined' || !currentToken.access_token) {
            try {
                await redirectToSpotifyAuthorize();
            } catch (error) {
                console.error(error);
            }
        }

        if (isTokenExpired()) {
            try {
                const newToken = await refreshToken();
                currentToken.save(newToken);
            } catch (error) {
                console.error(error);
            }
        }

        fetch('https://api.spotify.com/v1/me/top/tracks/?limit=1', {
            headers: { 'Authorization': 'Bearer ' + currentToken.access_token },
        })
        .then(response => response.json())
        .then(data => {
            // console.log(data);
            window.open(data.items[0].external_urls.spotify);
        })
        .catch(error => {
            console.error(error);
        });
    });
});