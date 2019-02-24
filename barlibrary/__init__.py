from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory
from pyramid.config import Configurator


def main(global_config, **settings):
    """
    Main entrypoint for wsgi
    """
    my_session_factory = SignedCookieSessionFactory('itsaseekreet')

    config = Configurator(settings=settings,
                          session_factory=my_session_factory)
    config.include('pyramid_jinja2')

    authn_policy = AuthTktAuthenticationPolicy(
        settings['BarLibrary.secret'], callback=None,
        hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
