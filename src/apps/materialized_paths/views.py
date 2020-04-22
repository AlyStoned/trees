from django.views.generic import View
from django.http import JsonResponse, Http404
from .models import Node


class TreeView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'tree': Node.get_tree()})


class BranchView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('node_id')
        try:
            node = Node.objects.get(pk=pk)
        except Node.DoesNotExist:
            raise Http404
        return JsonResponse({'tree': node.get_branch()})
