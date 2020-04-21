from django.views.generic import View
from django.http import JsonResponse


class TreeView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'tree': [{'test': 100}]})


class BranchView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('node_id')
        return JsonResponse({'tree': [{'test': pk}]})
