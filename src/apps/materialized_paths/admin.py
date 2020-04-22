from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import Node


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    fields = ('parent', 'name', 'tree_path',)
    readonly_fields = ('tree_path',)
    list_display = ('name_fmt', 'tree_path', 'parent_link',)
    list_display_links = ('name_fmt',)

    def name_fmt(self, obj):
        return '–' * obj.level + ' ' + obj.name

    name_fmt.short_description = _('Name')
    name_fmt.admin_order_field = 'name'

    def parent_link(self, obj):
        if obj.parent is not None:
            return mark_safe('<a href="{0}">{1}</a>'.format(
                reverse(
                    'admin:{}_{}_change'.format(self.opts.app_label, self.opts.model_name),
                    args=(obj.parent.pk,)
                ),
                obj.parent
            ))
    parent_link.short_description = _('Parent')
