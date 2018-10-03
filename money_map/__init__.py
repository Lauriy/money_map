from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from money_map.security import group_finder
from .models import DBSession, Base


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings, root_factory='money_map.models.Root')

    config.include('pyramid_chameleon')

    authn_policy = AuthTktAuthenticationPolicy(settings['money_map.secret'], callback=group_finder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_translation_dirs('money_map:locale/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('home', '/')
    config.add_route('hello', '/hello')
    config.add_route('bank_account_statement_upload', '/bank-account-statement-upload')
    # config.add_route('wiki_view', '/')
    # config.add_route('wikipage_add', '/add')
    # config.add_route('wikipage_view', '/{uid}')
    # config.add_route('wikipage_edit', '/{uid}/edit')
    config.add_static_view('deform_static', 'deform:static/')
    config.scan()
    return config.make_wsgi_app()
