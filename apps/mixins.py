from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View


class GetObjectMixins(LoginRequiredMixin, View):

    def get_object(self, queryset=None):
        return self.request.user
#
#
# class IsAuthOperatorMixins(LoginRequiredMixin, UserPassesTestMixin):
#     #
#     # def test_func(self):
#     #     return self.request.user.type == 'Operator'
#     #
#     # def handle_no_permission(self):
#     #     redirect('login_page')
#     #     return super().handle_no_permission()
#     pass


def switch_lang_code(path, language):
    lang_codes = [c for (c, name) in settings.LANGUAGES]

    if path == '':
        raise Exception('URL path for language switch is empty')
    elif path[0] != '/':
        raise Exception('URL path for language switch does not start with "/"')
    elif language not in lang_codes:
        raise Exception('%s is not a supported language code' % language)

    parts = path.split('/')

    if parts[1] in lang_codes:
        parts[1] = language
    else:
        parts[0] = "/" + language

    return '/'.join(parts)
