# -*- coding: utf-8 -*-
import re
import os
import six
import errno
import shutil
import pytest
from contextlib import contextmanager
from tempfile import TemporaryFile
if six.PY3:
    from urllib.parse import urlparse
    from subprocess import Popen, CalledProcessError, TimeoutExpired
elif six.PY2:
    from urlparse import urlparse
    from subprocess32 import Popen, CalledProcessError, TimeoutExpired

# clean the dumps each run
if os.path.isdir("traffic_dumps"):
    shutil.rmtree("traffic_dumps")


def pytest_addoption(parser):
    parser.addoption(
        "--mitmproxy-filter",
        action="store",
        default=None,
        help="filter specification for mitmproxy"
    )


@contextmanager
def new_proxy(name, scope, flt=None):
    ''' Start a new mitmdump process and
    return the address for clients to connect

    The captured content will be written to
    ./<dump_dir>/<scope>/<name>
    '''
    dump_dir = "traffic_dumps"

    try:
        os.makedirs(os.path.join(dump_dir, scope), mode=0o755)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise

    dump_file = os.path.join(dump_dir, scope, name)

    args = ["mitmdump", "--port=0", "--wfile={}".format(dump_file)]
    if flt:
        args.append(flt)

    def read(fp):
        fp.seek(0)
        return fp.read().decode("utf-8")

    with TemporaryFile() as stdout, TemporaryFile() as stderr:
        ps = Popen(args, stdout=stdout, stderr=stderr)
        if ps.poll() is not None:
            raise CalledProcessError(
                ps.returncode,
                ps.args,
                output=read(stderr)
            )
        status = read(stdout)
        url = urlparse(re.search(".*(http://[^\n]+)\n", status).group(1))
        yield url

        ps.terminate()
        try:
            ps.wait(timeout=5)
        except TimeoutExpired:
            ps.kill()
            ps.wait()

        if ps.returncode != 0:
            raise CalledProcessError(
                ps.returncode,
                ps.args,
                output=read(stderr)
            )


@pytest.fixture
def proxy(request):
    flt = request.config.getoption("--mitmproxy-filter")
    with new_proxy(request.node.name, request.scope, flt) as url:
        yield url


@pytest.fixture(scope="session")
def session_proxy(request):
    flt = request.config.getoption("--mitmproxy-filter")
    with new_proxy(request.node.name, request.scope, flt) as url:
        yield url
