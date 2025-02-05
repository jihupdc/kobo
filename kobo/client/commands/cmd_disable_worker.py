# -*- coding: utf-8 -*-


import sys
from six.moves.xmlrpc_client import Fault

from kobo.client import ClientCommand


class Disable_Worker(ClientCommand):
    """disable worker"""
    enabled = True
    admin = True


    def options(self):
        self.parser.usage = "%%prog %s [--all] [worker_name]" % self.normalized_name

        self.parser.add_option(
            "--all",
            default=False,
            action="store_true",
            help="Disable all enabled workers"
        )

    def run(self, *args, **kwargs):
        if len(args) == 0 and not kwargs['all']:
            self.parser.error("No worker (or --all) specified.")
        if len(args) and kwargs['all']:
            self.parser.error("Specify worker name or --all. From safety reasons both are not allowed.")

        username = kwargs.pop("username", None)
        password = kwargs.pop("password", None)
        hub = kwargs.pop("hub", None)

        self.set_hub(username, password, hub)
        if kwargs['all']:
            try:
                workers = self.hub.client.list_workers(True)
            except Fault as ex:
                sys.stderr.write("%s\n" % ex.faultString)
                sys.exit(1)
        else:
            workers = args
        for worker in workers:
            try:
                self.hub.client.disable_worker(worker)
            except Fault as ex:
                sys.stderr.write("%s\n" % ex.faultString)
