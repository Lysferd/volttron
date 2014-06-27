# -*- coding: utf-8 -*- {{{
# vim: set fenc=utf-8 ft=python sw=4 ts=4 sts=4 et:

# Copyright (c) 2013, Battelle Memorial Institute
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met: 
# 
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# The views and conclusions contained in the software and documentation
# are those of the authors and should not be interpreted as representing
# official policies, either expressed or implied, of the FreeBSD
# Project.
#
# This material was prepared as an account of work sponsored by an
# agency of the United States Government.  Neither the United States
# Government nor the United States Department of Energy, nor Battelle,
# nor any of their employees, nor any jurisdiction or organization that
# has cooperated in the development of these materials, makes any
# warranty, express or implied, or assumes any legal liability or
# responsibility for the accuracy, completeness, or usefulness or any
# information, apparatus, product, software, or process disclosed, or
# represents that its use would not infringe privately owned rights.
# 
# Reference herein to any specific commercial product, process, or
# service by trade name, trademark, manufacturer, or otherwise does not
# necessarily constitute or imply its endorsement, recommendation, or
# favoring by the United States Government or any agency thereof, or
# Battelle Memorial Institute. The views and opinions of authors
# expressed herein do not necessarily state or reflect those of the
# United States Government or any agency thereof.
# 
# PACIFIC NORTHWEST NATIONAL LABORATORY
# operated by BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY
# under Contract DE-AC05-76RL01830

# pylint: disable=W0142,W0403
#}}}


import os
import sys

from command import *
from environment import get_environment


commands = []


def command(command=None, aliases=None):
    def decorator(cls, direct=False):
        cls.name = name = not direct and command or cls.__name__
        cls.aliases = aliases
        commands.append((name, cls))
        return cls
    if command is None or isinstance(command, basestring):
        return decorator
    return decorator(command, True)


@command('install', ['add'])
class install_agent(object):
    @staticmethod
    def handler(agent_wheel):
        get_environment().aip.install_agent(agent_wheel)

    @staticmethod
    def execute(env, parser, args):
        ControlConnector(env.config).call.install_agent(
                os.path.abspath(args.agent_wheel))

    @classmethod
    def parser(cls):
        parser = CommandParser(help='install agent',
                               handler=cls.execute, aliases=cls.aliases)
        parser.add_argument('agent_wheel', help='path to agent wheel file')
        return parser


@command('remove', ['rm'])
class remove_agent(object):
    @staticmethod
    def handler(agent_name):
        get_environment().aip.remove_agent(agent_name)

    @staticmethod
    def execute(env, parser, args):
        ControlConnector(env.config).call.remove_agent(args.agent_name)

    @classmethod
    def parser(cls):
        parser = CommandParser(help='remove agent',
                               handler=cls.execute, aliases=cls.aliases)
        parser.add_argument('agent_name', help='name of agent')
        return parser


@command('list', ['ls'])
class list_agents(object):
    @staticmethod
    def handler():
        return get_environment().aip.list_agents()

    @staticmethod
    def execute(env, parser, args):
        agents = ControlConnector(env.config).call.list_agents()
        if not agents:
            return
        agents.sort()
        width = max(5, min(60, max(len(x[0]) for x in agents)))
        fmt = '{:{}}  {:>9}  {:>6}\n'
        sys.stderr.write(fmt.format('AGENT', width, 'AUTOSTART', 'STATUS'))
        for name, enabled, (pid, status) in agents:
            if enabled is None:
                enabled = 'n/a'
            elif enabled:
                enabled = 'enabled '
            else:
                enabled = 'disabled '
            sys.stdout.write(fmt.format(name, width, enabled,
                ('running [{}]'.format(pid) if status is None else str(status))
                 if pid else ''))

    @classmethod
    def parser(cls):
        return CommandParser(help='list agents',
                             handler=cls.execute, aliases=cls.aliases)


@command('enable')
class enable_agent(object):
    @staticmethod
    def handler(agent_name):
        get_environment().aip.enable_agent(agent_name)

    @staticmethod
    def execute(env, parser, args):
        ControlConnector(env.config).call.enable_agent(args.agent_name)

    @classmethod
    def parser(cls):
        parser = CommandParser(help='enable agent to start automatically',
                               handler=cls.execute, aliases=cls.aliases)
        parser.add_argument('agent_name', help='name of agent to enable')
        return parser


@command('disable')
class disable_agent(object):
    @staticmethod
    def handler(agent_name):
        get_environment().aip.disable_agent(agent_name)

    @staticmethod
    def execute(env, parser, args):
        ControlConnector(env.config).call.disable_agent(args.agent_name)

    @classmethod
    def parser(cls):
        parser = CommandParser(help='prevent agent from starting automatically',
                               handler=cls.execute, aliases=cls.aliases)
        parser.add_argument('agent_name', help='name of agent to disable')
        return parser


@command('start')
class start_agent(object):
    @staticmethod
    def handler(agent_name):
        get_environment().aip.start_agent(agent_name)

    @staticmethod
    def execute(env, parser, args):
        ControlConnector(env.config).call.start_agent(args.agent_name)

    @classmethod
    def parser(cls):
        parser = CommandParser(help='start installed agent',
                               handler=cls.execute, aliases=cls.aliases)
        parser.add_argument('agent_name', help='name of agent to start')
        return parser


@command('stop')
class stop_agent(object):
    @staticmethod
    def handler(agent_name):
        get_environment().aip.stop_agent(agent_name)

    @staticmethod
    def execute(env, parser, args):
        ControlConnector(env.config).call.stop_agent(args.agent_name)

    @classmethod
    def parser(cls):
        parser = CommandParser(help='stop running agent',
                               handler=cls.execute, aliases=cls.aliases)
        parser.add_argument('agent_name', help='name of agent to stop')
        return parser


@command('run')
class run_agent(object):
    @staticmethod
    def handler(config_path):
        get_environment().aip.launch_agent(config_path)

    @staticmethod
    def execute(env, parser, args):
        conn = ControlConnector(env.config)
        for config in args.agent_config:
            conn.call.run_agent(os.path.abspath(os.path.expanduser(config)))

    @classmethod
    def parser(cls):
        #XXX: run_agent alias may be removed after a period of time (2013-08-21)
        parser = CommandParser(help='run agent(s) defined in config file(s)',
                               handler=cls.execute, aliases=cls.aliases)
        parser.add_argument('agent_config', nargs='+')
        return parser


@command
class shutdown(object):
    @staticmethod
    def handler():
        get_environment().aip.shutdown()

    @staticmethod
    def execute(env, parser, args):
        ControlConnector(env.config).call.shutdown()

    @classmethod
    def parser(cls):
        return CommandParser(help='stop all agents', handler=cls.execute)

