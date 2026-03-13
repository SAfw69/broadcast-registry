from django.contrib import admin
from django.utils.html import format_html
from .models import Department, Team, TeamMember, Repository, AuditLog


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1
    fields = ['user', 'role', 'joined_at']


class RepositoryInline(admin.TabularInline):
    model = Repository
    extra = 1
    fields = ['name', 'url', 'description']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'team_count', 'created_at']
    search_fields = ['name']

    def team_count(self, obj):
        return obj.teams.count()
    team_count.short_description = 'Teams'


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'manager', 'status', 'member_count', 'updated_at']
    list_filter = ['status', 'department']
    search_fields = ['name', 'description', 'department__name']
    filter_horizontal = ['upstream_dependencies']
    inlines = [TeamMemberInline, RepositoryInline]
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'department', 'manager', 'status')
        }),
        ('Details', {
            'fields': ('description', 'mission', 'responsibilities')
        }),
        ('Contact', {
            'fields': ('slack_channel', 'email')
        }),
        ('Dependencies', {
            'fields': ('upstream_dependencies',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def member_count(self, obj):
        count = obj.members.count()
        color = 'green' if count >= 5 else 'red'
        return format_html('<span style="color:{}">{}</span>', color, count)
    member_count.short_description = 'Members'


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'team', 'role', 'joined_at']
    list_filter = ['role', 'team__department']
    search_fields = ['user__username', 'user__first_name', 'team__name']


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'team', 'url']
    search_fields = ['name', 'team__name']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action', 'model_name', 'object_repr']
    list_filter = ['action', 'model_name']
    search_fields = ['user__username', 'object_repr']
    readonly_fields = ['timestamp', 'user', 'action', 'model_name', 'object_id', 'object_repr', 'changes', 'ip_address']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
