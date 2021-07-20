***************
Useful Commands
***************

For developers, there are a set of useful commands that might be useful to use
on a regular basis.

PyPI Mirrors
============

To install a package using Tsinghua tuna PyPI mirrors::

    $ pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

Configure Proxy
===============

Set a http proxy::

    $ git config --global http.proxy http://proxyaddress:port

Reset proxy::

    $ git config --global --unset http.proxy

Check the current proxy::

    $ git config --global --get http.proxy

Pip install with proxy::

    $ https_proxy='http://address:port' pip install some_package

Or alternatively::

    $ export https_proxy='http://address:port'
    $ pip install some_package

Upload a package
================
