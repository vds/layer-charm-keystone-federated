from charmhelpers.core.hookenv import (
    log,
    DEBUG,
)
from charmhelpers.core.templating import render


import charm.openstack.keystone_federated_backend as keystone_federated_backend

from charms.reactive import (
    set_flag,
    clear_flag,
    when,
    when_not,
)


@when('endpoint.keystone-federated-backend.joined')
@when_not('keystone-federated-backend-configured')
def setup_wsgi_config():
    # Generate the apache site include snippet
    # Change the wsgi tempalte to actually include the snippet
    # Restart the service

    log("Setup WSGI config", level=DEBUG)
    render(source='wsgi-openstack-api.conf',
           target='/etc/apache2/sites-enabled/wsgi-openstack-api.conf',
           owner='www-data',
           perms=0o775,
           context=keystone_federated_backend.OpenIDContext()())
    set_flag('endpoint.keystone-federated-backend.configured')


@when('endpoint.keystone-federated-backend.departed')
@when('endpoint.keystone-federated-backend.configured')
def remove_wsgi_config():
    # Remove the apache site include snippet
    # Change the wsgi tempalte to not including the snippet
    # Restart the service
    clear_flag('endpoint.keystone-federated-backend-configured')
