import { Profile } from "./schema";

const authConfig: NextAuthConfig = {
    providers: [{
        id: 'shib',
        name: 'RPI SSO',
        type: 'oauth',
        clientId: process.env.CLIENT_ID,
        clientSecret: process.env.CLIENT_SECRET,
        authorization: {
            url: 'https://shib.auth.rpi.edu/idp/profile/oidc/authorize',
            params: { scope: 'openid email profile' }
        },
        checks: ['pkce', 'state'],
        token: {
            url: 'https://shib.auth.rpi.edu/idp/profile/oidc/token',
            params: { grant_type: 'authorization_code' }
        },
        issuer: 'https://shib.auth.rpi.edu',
        jwks_endpoint: 'https://shib.auth.rpi.edu/idp/profile/oidc/keyset',
        userinfo: {
            url: 'https://shib.auth.rpi.edu/idp/profile/oidc/userinfo',
            params: { grant_type: 'authorization_code' }
        },
        profile(profile: Profile) {
            console.log(profile);
            return {
                // return a subset of the variables that you want
                id: profile.sub,
                name: profile.name,
                email: profile.email,
            };
        },
    }]
}