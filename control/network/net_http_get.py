#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
net_http_get

DOCUMENT ME!

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

revision 0.3  2015/nov  mlabru
pep8 style conventions

revision 0.2  2014/nov  mlabru
desmembramento do NetManager
inclusão do config_manager e event_manager

revision 0.1  2014/nov  mlabru
initial release (Linux/Python)
---------------------------------------------------------------------------------------------------
"""
__version__ = "$revision: 0.3$"
__author__ = "Milton Abrunhosa"
__date__ = "2015/11"

# < imports >--------------------------------------------------------------------------------------

# python library
import logging
import urllib.request, urllib.error, urllib.parse

# < class CNetHttpGet >----------------------------------------------------------------------------

class CNetHttpGet(object):
    """
    DOCUMENT ME!
    """
    # ---------------------------------------------------------------------------------------------
    def __init__(self, f_event, f_config):
        """
        initializes the network http sender
        """
        # check input
        assert f_event
        assert f_config

        # init super class
        super(CNetHttpGet, self).__init__()

        # event manager
        # self.__event = f_event

        # config manager
        # self.__config = f_config

    # ---------------------------------------------------------------------------------------------
    def get_data(self, fs_srv, fs_msg):
        """
        @param fs_srv: DOCUMENT ME!
        @param fs_msg: DOCUMENT ME!
        """
        try:
            # send request
            l_resp = urllib.request.urlopen("http://{}/{}".format(fs_srv, fs_msg))

        # em caso de error...
        except Exception as ls_err:
            # logger
            l_log = logging.getLogger("CNetHttpGet::get_data")
            l_log.setLevel(logging.WARNING)
            l_log.warning("<E01: server {} reports {} for request {}.".format(fs_srv, ls_err, fs_msg))

            # return
            return None

        # data
        return l_resp.read()

# < the end >--------------------------------------------------------------------------------------
