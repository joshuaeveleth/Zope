##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from zope.deferredimport import deprecated

# BBB Zope 5.0
deprecated(
    'Please import from ZServer.Zope2.Startup.run',
    run='ZServer.Zope2.Startup.run:run',
)


def configure(configfile):
    """ Provide an API which allows scripts like zopectl to configure
    Zope before attempting to do 'app = Zope2.app(). Should be used as
    follows:  from Zope2.Startup.run import configure;
    configure('/path/to/configfile'); import Zope2; app = Zope2.app() """
    import Zope2.Startup
    starter = Zope2.Startup.get_starter(wsgi=True)
    opts = _setconfig(configfile)
    starter.setConfiguration(opts.configroot)
    starter.setupSecurityOptions()
    return starter


def _setconfig(configfile=None):
    """ Configure a Zope instance based on ZopeOptions.  Optionally
    accept a configfile argument (string path) in order to specify
    where the configuration file exists. """
    from Zope2.Startup import options, handlers
    opts = options.ZopeOptions()
    if configfile:
        opts.configfile = configfile
        opts.realize(raise_getopt_errs=0)
    else:
        opts.realize()

    handlers.handleConfig(opts.configroot, opts.confighandlers)
    import App.config
    App.config.setConfiguration(opts.configroot)
    return opts


def make_wsgi_app(global_config, zope_conf):
    from App.config import setConfiguration
    from Zope2.Startup import get_starter
    from Zope2.Startup.handlers import handleConfig
    from Zope2.Startup.options import ZopeOptions
    from ZPublisher.WSGIPublisher import publish_module
    starter = get_starter(wsgi=True)
    opts = ZopeOptions()
    opts.configfile = zope_conf
    if opts.schemafile == 'zopeschema.xml':
        opts.schemafile = 'wsgischema.xml'
    opts.realize(args=(), progname='Zope2WSGI', raise_getopt_errs=False)
    handleConfig(opts.configroot, opts.confighandlers)
    setConfiguration(opts.configroot)
    starter.setConfiguration(opts.configroot)
    starter.prepare()
    return publish_module
