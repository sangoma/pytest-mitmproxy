# -*- coding: utf-8 -*-
import re
import os
import shutil
import pytest
from contextlib import contextmanager
from subprocess import Popen, PIPE, SubprocessError

# clean the dumps each run
if os.path.isdir("traffic_dumps"):
    shutil.rmtree("traffic_dumps")


@contextmanager
def new_proxy(name: str, scope: str, flt: str=None):
    ''' Start a new mitmdump process and
    return the address for clients to connect

    The captured content will be written to
    ./<dump_dir>/<scope>/<name>
    '''
    dump_dir = "traffic_dumps"

    os.makedirs("{}/{}".format(dump_dir, scope), mode=0o755, exist_ok=True)
    dump_file = "{}/{}/{}".format(dump_dir, scope, name)

    args = ["mitmdump", "--port=0", "--wfile={}".format(dump_file)]
    args.append(flt) if flt else None

    ps = Popen(
        args,
        stdout=PIPE,
        stderr=PIPE,
        universal_newlines=True,
        bufsize=1
    )
    if ps.poll() is not None:
        raise SubprocessError("mitmdump was unable to run")
    status = ps.stdout.readline()
    addr = re.search(".*http://([^\n]+)\n", status).group(1)
    yield addr
    ps.terminate()


@pytest.fixture
def proxy(request):
    mark = request.node.get_marker("dump_filter")
    flt = mark.args[0] if mark else None
    with new_proxy(request.node.name, request.scope, flt) as addr:
        ip, port = addr.split(":")
        yield ip, port
