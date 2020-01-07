# -*- coding: utf-8 -*-
'''
Module to provide Saptune functionality to Salt

.. versionadded:: pending

:maintainer:    Dario Maiocchi <dmaiocchi@suse.com>
:maturity:      alpha
:depends:       ``saptune`` Python module
:platform:      all

:configuration: This module requires the saptune python module and uses the
    following defaults which may be overridden in the minion configuration:

.. code-block:: yaml
 TODO
'''

# Import Python libs
from __future__ import absolute_import, unicode_literals, print_function
import logging

from salt import exceptions
import salt.utils.path


__virtualname__ = 'saptune'

SAPTUNE_BIN = '/usr/sbin/saptune'
SAPTUNE_CONF = '/etc/sysconfig/saptune'

LOGGER = logging.getLogger(__name__)

def __virtual__():
    '''
    Only load this module if saptune package is installed
    '''
    if bool(salt.utils.path.which(SAPTUNE_BIN)):
        return __virtualname__

    else:
        return (
            False,
            'The saptune execution module failed to load: the saptune package'
            ' is not available.')

def is_solution_applied(solution_name):
    '''
    check if the saptune solution is applied or not
    '''

    solution_to_search = "TUNE_FOR_SOLUTIONS=\"{}\"".format(solution_name)

    # open the config file and search if the solution is enabled
    with open(SAPTUNE_CONF) as conf:
        if solution_to_search in conf.read():
           return True
    return False

def apply_solution(solution_name):
    '''
    Tune system for all notes applicable to your SAP solution:


    CLI Example:

    .. code-block:: bash

        salt '*' saptune.apply_solution solution-name
    '''
    cmd = '{} solution apply {}'.format(SAPTUNE_BIN, solution_name)
    retcode = __salt__['cmd.retcode'](cmd)

    if is_solution_applied(solution_name) and retcode == 0:
        LOGGER.info("solution {} applied sucessfully")
        return 0

    if is_solution_applied(solution_name) == False:
        LOGGER.error("solution {} was not applied. Check if another one is already applied and revert it before apply a new one")
        return 1
