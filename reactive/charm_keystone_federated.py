from charmhelpers.core.templating import render

import charm.openstack.keystone_federated as keystone_federated

from charms.reactive import (
    set_flag,
    clear_flag,
    when,
    when_not,
)


@when('federated-backend.joined')
@when_not('federated-backend-configured')
def setup_wsgi_config():
    # Generate the apache site include snippet
    # Change the wsgi tempalte to actually include the snippet
    # Restart the service

    render(source='wsgi-openstack-api.conf',
           target='/etc/apache2/sites-enabled/wsgi-openstack-api.conf',
           owner='www-data',
           perms=0o775,
           context=keystone_federated.OpenIDContext())
    set_flag('federated-backend-configured')


@when('federated-backend.departed')
@when('federated-backend-configured')
def remove_wsgi_config():
    # Remove the apache site include snippet
    # Change the wsgi tempalte to not including the snippet
    # Restart the service
    clear_flag('federated-backend-configured')
