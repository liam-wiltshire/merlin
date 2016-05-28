# This file is part of Merlin.
# Merlin is the Copyright (C)2008,2009,2010 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 
import re
from sqlalchemy.sql import text, bindparam
from Core import Merlin
from Core.db import session
from Core.maps import Channel
from Core.config import Config
from Core.loadable import system, loadable, route


class todo(loadable):
    """Webulations ToDo list"""
    usage = ""
    
    @route(r"")
    def execute(self, message, user, params):
#	hash, chan = params.groups();        

	message.reply("Webulations' Todo List\n===========\npriority\tcomment\t\t(added by)");

        query = "SELECT * FROM todo WHERE status = 'pending' ORDER BY priority DESC";
        result = session.execute(query);
	for row in result:
		message.reply(str(row[3]) + " " + str(row[1]) + " ("+str(row[2])+")");

        result.close();


#	message.reply("Investigate how to disable bot for meetings");
#	message.reply("Check stability of WA/TG integrations");
#	message.reply("Allow bot commands to come from WA/TG");
#	message.reply("Add to other channels as needed");
#	message.reply("Work out how not to suck");
