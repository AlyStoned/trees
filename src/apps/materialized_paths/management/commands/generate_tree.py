import collections
from random import randint
from argparse import ArgumentTypeError
from django.db import connection
from django.core.management import BaseCommand
from ...models import Node


class Command(BaseCommand):

    help = 'Generate tree nodes, populate db'

    @staticmethod
    def check_positive(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise ArgumentTypeError("%s is an invalid positive int value" % value)
        return ivalue

    def add_arguments(self, parser):
        parser.add_argument('-nc', '--nodes-count', type=self.check_positive,
                            default=20, dest='nodes_count', help='Nodes count')
        # parser.add_argument('-d', '--depth', type=int, default=6, dest='depth', help='Depth')
        # parser.add_argument('-t', '--threads', type=int, default=4, dest='threads', help='Threads (roots)')
        parser.add_argument('-rn', '--root-name', action='store', dest='root_name',
                            default='base', help='Root name prefix')
        parser.add_argument('-cn', '--child-name', action='store', dest='child_name',
                            default='child', help='Child name prefix')

    def handle(self, *args, **options):
        nodes_count = options['nodes_count']
        # depth = options['depth']
        # threads = options['threads']
        root_name = options['root_name']
        child_name = options['child_name']

        # Node.objects.all().delete()
        with connection.cursor() as cursor:
            # cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE NAME='materialized_paths_node'")
            cursor.execute("DELETE FROM materialized_paths_node")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'materialized_paths_node'")

        nodes = []
        child_counter = collections.Counter()

        for i in range(nodes_count):
            d = {}

            parent_id = randint(0, i)
            d['parent_id'] = parent_id if parent_id else None

            if parent_id != 0:
                child_counter[parent_id] += 1
                d['name'] = f'{nodes[parent_id - 1]["name"]} {child_name} {child_counter[parent_id]}'
            else:
                child_counter['roots'] += 1
                d['name'] = f'{root_name} {child_counter["roots"]}'

            nodes.append(d)

        for node in nodes:
            n = Node(**node)
            n.save()
            self.stdout.write(self.style.SUCCESS(f'Create Node {n.pk}'))
