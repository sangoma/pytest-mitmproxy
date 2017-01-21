pytest-mitmproxy
===================================

.. image:: https://travis-ci.org/sangoma/pytest-mitmproxy.svg?branch=master
    :target: https://travis-ci.org/sangoma/pytest-mitmproxy
    :alt: See Build Status on Travis CI

.. image:: https://ci.appveyor.com/api/projects/status/github/sangoma/pytest-mitmproxy?branch=master
    :target: https://ci.appveyor.com/project/sangoma/pytest-mitmproxy/branch/master
    :alt: See Build Status on AppVeyor

Pytest fixtures for creating mitmproxy instances as-needed with filterable captures for later analysis

Features
--------

Currently pytest-mitmproxy is not considered stable/release and
has quite afew TODOs to wrap up before being promoted to 'stable'

* Fixtures to create new mitmproxy instances


Requirements
------------

* mitmproxy (python3 only, so must be installed seperately for python2 use)
* subprocess32 for python2


TODO
-----

* Don't hardcode the traffic dump's save location
* Fixtures for more than just the function and session scopes
* Don't clobber the previously-saved traffic dumps at plugin load time
* Write some tests
* More cleanliness in process management (catch all possible hangs/fails)
* Capture `mitmdumps` stdout in a seperate thread


License
-------

Distributed under the terms of the `MIT`_ license, "pytest-mitmproxy" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/sangoma/pytest-mitmproxy/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
