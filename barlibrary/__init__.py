from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator

from .security import groupfinder


def main(global_config, **settings):
    """
    Main entrypoint for wsgi
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')

    authn_policy = AuthTktAuthenticationPolicy(
        settings['BarLibrary.secret'], callback=groupfinder,
        hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
