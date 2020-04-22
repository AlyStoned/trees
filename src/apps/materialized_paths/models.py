from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.urls import reverse
from . import conf


class Node(models.Model):
    parent = models.ForeignKey('self', verbose_name=_('parent'), null=True, blank=True,
                               on_delete=models.CASCADE, related_name='children')

    name = models.CharField('name', max_length=255, blank=True)
    sequent = models.PositiveSmallIntegerField(_('sequent'), default=0, editable=False)
    tree_path = models.CharField(_('path'), max_length=255, editable=False, db_index=True)
    created_at = models.DateTimeField(_('created date'), default=None, editable=False)

    class Meta:
        verbose_name = _('node')
        verbose_name_plural = _('nodes')
        ordering = ['tree_path', 'created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if is_new:
            self.created_at = now()

            sequent = Node.objects.filter(
                parent=self.parent if self.parent else None
            ).aggregate(models.Max('sequent'))['sequent__max']

            if sequent is None:  # create first obj in db
                sequent = 0

            self.sequent = sequent + 1

            if self.parent:
                self.tree_path = f'{self.parent.tree_path}{conf.PATH_SEPARATOR}{self.sequent:06}'
            else:
                self.tree_path = f'{self.sequent:06}'

        super().save(self, *args, **kwargs)

    def get_absolute_url(self):
        return reverse('materialized_paths:branch', args=[str(self.id)])

    @property
    def is_root(self):
        return self.parent is None

    @property
    def thread(self):
        return self.tree_path.rsplit(conf.PATH_SEPARATOR, 1)[0]

    @property
    def level(self):
        return len(self.tree_path.split(conf.PATH_SEPARATOR)) - 1

    @staticmethod
    def _add_children(children, node):
        for item in children:
            if item['id'] == node.parent_id:
                child_dict = Node._build_new_dict(node)
                item['children'].append(child_dict)
                return True
            elif item['children']:
                if Node._add_children(item['children'], node):
                    return True
        return False

    @staticmethod
    def _build_new_dict(node):
        return {
            'id': node.id,
            'name': node.name,
            # 'tree_path': node.tree_path,
            # 'url': node.get_absolute_url(),
            'children': [],
        }

    @classmethod
    def get_tree(cls):
        result = []
        parent = None

        for node in cls.objects.all():
            if parent and node.is_root:
                result.append(parent)
                parent = None

            if not parent:
                parent = cls._build_new_dict(node)
                continue

            if node.parent_id == parent['id']:
                child_dict = cls._build_new_dict(node)
                parent['children'].append(child_dict)
            else:
                cls._add_children(parent['children'], node)

        if parent:
            result.append(parent)

        return result

    def get_branch(self):
        nodes = type(self).objects.filter(tree_path__startswith=self.tree_path + conf.PATH_SEPARATOR)
        parent = self._build_new_dict(self)

        for node in nodes:
            if node.parent_id == parent['id']:
                child_dict = self._build_new_dict(node)
                parent['children'].append(child_dict)
            else:
                self._add_children(parent['children'], node)

        return parent
