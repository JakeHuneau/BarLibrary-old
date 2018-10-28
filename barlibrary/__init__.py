from pyramid.config import Configurator


def main(global_config, **settings):
    """
    Main entrypoint for wsgi
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
