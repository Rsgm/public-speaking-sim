from django.contrib import admin
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from userena.admin import UserenaSignupInline, UserenaAdmin

from speakeazy.users.models import UserProfile


class UserAdmin(UserenaAdmin):
    inlines = [UserenaSignupInline, ]
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff', 'is_active', 'date_joined', 'hijack_field')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    def hijack_field(self, obj):
        template = get_template('users/hijack_button.html')

        context = {
            'user_pk': obj.pk,
            'username': str(obj),
        }

        return template.render(context)

    hijack_field.short_description = _('Hijack user')


admin.site.register(UserProfile)
admin.site.register(get_user_model(), UserAdmin)
