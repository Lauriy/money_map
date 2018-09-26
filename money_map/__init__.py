from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('bank_account_statement_upload', '/bank-account-statement-upload')
    # config.add_route('wiki_view', '/')
    # config.add_route('wikipage_add', '/add')
    # config.add_route('wikipage_view', '/{uid}')
    # config.add_route('wikipage_edit', '/{uid}/edit')
    config.add_static_view('deform_static', 'deform:static/')
    config.scan()
    return config.make_wsgi_app()
