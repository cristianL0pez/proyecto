from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, CentroMedico, Especialista, Agenda, Cita

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('tipo_usuario',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('tipo_usuario',)}),
    )

admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(CentroMedico)
admin.site.register(Especialista)
admin.site.register(Agenda)
admin.site.register(Cita)