# -*- coding: utf-8 -*-
import re
import os
import shutil
import pytest
import urllib
from contextlib import contextmanager
from subprocess import Popen, SubprocessError, CalledProcessError
from tempfile import TemporaryFile
from urllib.parse import urlparse

# clean the dumps each run
if os.path.isdir("traffic_dumps"):
    shutil.rmtree("traffic_dumps")


@contextmanager
def new_proxy(name: str, scope: str, flt: str=None) -> urllib.parse.ParseResult:
    ''' Start a new mitmdump process and
    return the address for clients to connect

    The captured content will be written to
    ./<dump_dir>/<scope>/<name>
    '''
    dump_dir = "traffic_dumps"

    os.makedirs(os.path.join(dump_dir, scope), mode=0o755, exist_ok=True)
    dump_file = os.path.join(dump_dir, scope, name)

    args = ["mitmdump", "--port=0", "--wfile={}".format(dump_file)]
    args.append(flt) if flt else None

    with TemporaryFile() as fp:

        ps = Popen(
            args,
            stdout=fp,
            universal_newlines=True,
            bufsize=1
        )
        if ps.poll() is not None:
            raise SubprocessError("mitmdump was unable to run")
        fp.seek(0)
        status = fp.read().decode("utf-8")
        url = urlparse(re.search(".*(http://[^\n]+)\n", status).group(1))
        yield url

    try:
        ps.terminate()
        retcode = ps.wait(timeout=5)
    except TimeoutExpired:
        ps.kill()
        retcode = ps.wait()

    if retcode != 0:
        raise CalledProcessError(retcode, ps.args)


@pytest.fixture
def proxy(request) -> urllib.parse.ParseResult:
    mark = request.node.get_marker("dump_filter")
    flt = mark.args[0] if mark else None
    with new_proxy(request.node.name, request.scope, flt) as url:
        yield url
