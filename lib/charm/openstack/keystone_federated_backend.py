from subprocess import check_call, CalledProcessError

from charmhelpers.core.hookenv import (
    config,
    log,
    DEBUG,
    status_set,
)

from charmhelpers.contrib.openstack import context


class OpenIDContext(context.OSContextGenerator):

    def enable_modules(self):
        cmd = ['a2enmod', 'auth_openidc']
        try:
            check_call(cmd)
        except CalledProcessError as e:
            status_set(
                'blocked',
                'Failed to emable libapache2-mod-auth-openidc: {}'.format(e))
            raise e

    def __call__(self):
        self.enable_modules()
        ctxt = {}
        log("Creating proper OpenIDContext", level=DEBUG)
        # Although other context run commands like this, this is strongly
        # discouraged and would almost certainly get a -1 if proposed.
        ctxt = {
            'oidc_metadata_url': config('oidc-metadata-url'),
            'oidc_client_id': config('oidc-client-id'),
            'oidc_client_secret': config('oidc-client-secret'),
            'oidc_crypto_passphrase': config('oidc-crypto-passphrase'),
            'oidc_remote_user-claim': config('oidc-remote-user-claim'),
            'oidc_http_iss': config('oidc-http-iss'),
            'oidc_ssl_validate-server': config('oidc-ssl-validate-server'),
            'oidc_redirect_admin_uri': config('oidc-redirect-admin-uri'),
            'oidc_redirect_public_uri': config('oidc-redirect-public-uri'),
        }
        return ctxt
