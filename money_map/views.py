import os

from colander import SchemaNode, MappingSchema
from deform import FileData, Form, ValidationFailure
from deform.widget import FileUploadWidget

from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from pyramid.view import view_config

# pages = {
#     '100': dict(uid='100', title='Page 100', body='<em>100</em>'),
#     '101': dict(uid='101', title='Page 101', body='<em>101</em>'),
#     '102': dict(uid='102', title='Page 102', body='<em>102</em>')
# }

# class WikiPage(colander.MappingSchema):
#     title = colander.SchemaNode(colander.String())
#     body = colander.SchemaNode(
#         colander.String(),
#         widget=deform.widget.RichTextWidget()
#     )

    # @view_config(renderer='templates/form.pt', name='file')
    # @demonstrate('File Upload Widget')
    # def file(self):
    #     class Schema(colander.Schema):
    #         upload = colander.SchemaNode(
    #             deform.FileData(),
    #             widget=deform.widget.FileUploadWidget(tmpstore)
    #         )
    #
    #     schema = Schema()
    #     form = deform.Form(schema, buttons=('submit',))
    #
    #     return self.render_form(form, success=tmpstore.clear)
from money_map.security import USERS, check_password


class AuthenticationViews:
    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='home')
    def home(self):
        return {'name': 'Home View'}

    @view_config(route_name='login', renderer='login.pt')
    def login(self):
        request = self.request
        login_url = request.route_url('login')
        referrer = request.url
        if referrer == login_url:
            referrer = '/'  # never use login form itself as came_from
        came_from = request.params.get('came_from', referrer)
        message = ''
        login = ''
        password = ''
        if 'form.submitted' in request.params:
            login = request.params['login']
            password = request.params['password']
            hashed_pw = USERS.get(login)
            if hashed_pw and check_password(password, hashed_pw):
                headers = remember(request, login)
                return HTTPFound(location=came_from,
                                 headers=headers)
            message = 'Failed login'

        return dict(
            name='Login',
            message=message,
            url=request.application_url + '/login',
            came_from=came_from,
            login=login,
            password=password,
        )

    @view_config(route_name='logout')
    def logout(self):
        request = self.request
        headers = forget(request)
        url = request.route_url('home')
        return HTTPFound(location=url,
                         headers=headers)

class BankAccountStatement(MappingSchema):
    class Store(dict):
        def preview_url(self, name):
            return ''

    file = SchemaNode(FileData(), widget=FileUploadWidget(Store(), accept='text/xml'))

class BankAccountStatementViews(object):
    def __init__(self, request):
        self.request = request

    @property
    def bank_account_statement_form(self):
        schema = BankAccountStatement()

        return Form(schema, buttons=('submit',))

    @property
    def reqts(self):
        return self.bank_account_statement_form.get_widget_resources()

    @view_config(route_name='bank_account_statement_upload', renderer='templates/bank_account_statement_upload.pt')
    def bank_account_statement_upload(self):
        form = self.bank_account_statement_form.render()

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.bank_account_statement_form.validate(controls)
            except ValidationFailure as e:
                return dict(form=e.render())

            # last_uid = int(sorted(pages.keys())[-1])
            # new_uid = str(last_uid + 1)
            # pages[new_uid] = dict(
            #     uid=new_uid, title=appstruct['title'],
            #     body=appstruct['body']
            # )

            f = appstruct['file']
            bank_account_statement_filename = f['filename']
            bank_account_statement_extension = os.path.splitext(bank_account_statement_filename)[1]
            bank_account_statement_file = f['fp']

            print (bank_account_statement_file)

            # Now visit new page
            #url = self.request.route_url('wikipage_view', uid=new_uid)
            url = self.request.route_url('home')

            return HTTPFound(url)

        return dict(form=form)


# class WikiViews(object):
#     def __init__(self, request):
#         self.request = request
#
#     @property
#     def wiki_form(self):
#         schema = WikiPage()
#         return deform.Form(schema, buttons=('submit',))
#
#     @property
#     def reqts(self):
#         return self.wiki_form.get_widget_resources()
#
#     @view_config(route_name='wiki_view', renderer='templates/wiki_view.pt')
#     def wiki_view(self):
#         return dict(pages=pages.values())
#
#     @view_config(route_name='wikipage_add',
#                  renderer='templates/wikipage_addedit.pt')
#     def wikipage_add(self):
#         form = self.wiki_form.render()
#
#         if 'submit' in self.request.params:
#             controls = self.request.POST.items()
#             try:
#                 appstruct = self.wiki_form.validate(controls)
#             except deform.ValidationFailure as e:
#                 # Form is NOT valid
#                 return dict(form=e.render())
#
#             # Form is valid, make a new identifier and add to list
#             last_uid = int(sorted(pages.keys())[-1])
#             new_uid = str(last_uid + 1)
#             pages[new_uid] = dict(
#                 uid=new_uid, title=appstruct['title'],
#                 body=appstruct['body']
#             )
#
#             # Now visit new page
#             url = self.request.route_url('wikipage_view', uid=new_uid)
#             return HTTPFound(url)
#
#         return dict(form=form)
#
#     @view_config(route_name='wikipage_view', renderer='templates/wikipage_view.pt')
#     def wikipage_view(self):
#         uid = self.request.matchdict['uid']
#         page = pages[uid]
#         return dict(page=page)
#
#     @view_config(route_name='wikipage_edit',
#                  renderer='templates/wikipage_addedit.pt')
#     def wikipage_edit(self):
#         uid = self.request.matchdict['uid']
#         page = pages[uid]
#
#         wiki_form = self.wiki_form
#
#         if 'submit' in self.request.params:
#             controls = self.request.POST.items()
#             try:
#                 appstruct = wiki_form.validate(controls)
#             except deform.ValidationFailure as e:
#                 return dict(page=page, form=e.render())
#
#             # Change the content and redirect to the view
#             page['title'] = appstruct['title']
#             page['body'] = appstruct['body']
#
#             url = self.request.route_url('wikipage_view',
#                                          uid=page['uid'])
#             return HTTPFound(url)
#
#         form = wiki_form.render(page)
#
#         return dict(page=page, form=form)