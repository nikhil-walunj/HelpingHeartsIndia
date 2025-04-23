from django.contrib import admin
from .models import Banner,VisionMission,Statistic,Initiative,User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'full_name', 'role', 'status', 'created_at', 'is_admin', 'is_superuser')
    search_fields = ('email', 'full_name')
    ordering = ('created_at',)
    list_filter = ('is_admin', 'is_superuser', 'status', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'role', 'status')}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)

class BannerAdmin(admin.ModelAdmin):
    list_display = ['title','description','order', 'status']
admin.site.register(Banner, BannerAdmin)

class VisionMissionAdmin(admin.ModelAdmin):
    list_display = ('vision_title','vision_description','mission_title','mission_description','last_updated')
admin.site.register(VisionMission, VisionMissionAdmin)

class StatisticAdmin(admin.ModelAdmin):
    list_display = ('label','value','icon','description','order','status','last_updated')
admin.site.register(Statistic, StatisticAdmin)

class InitiativeAdmin(admin.ModelAdmin):
    list_display = ('title','description','image','location','start_date','end_date','status')
admin.site.register(Initiative, InitiativeAdmin)