from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Node


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    fields = ('parent', 'name', 'tree_path',)
    list_display = ('parent', 'name_fmt', 'tree_path',)
    readonly_fields = ('tree_path',)

    def name_fmt(self, obj):
        return '–' * obj.level + ' ' + obj.name

    name_fmt.short_description = _('Name')
    name_fmt.admin_order_field = 'name'
