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
import os
from Core import Merlin
from Core.db import session
from Core.maps import Channel
from Core.config import Config
from Core.loadable import system, loadable, route, require_user

class meetingmode(loadable):
    """Control the bot's meeting mode (temporarily disable it)"""
    usage = "[on|off]"
    
    @route(r"(on|off)")
    @require_user
    def execute(self, message, user, params):
	act = params.groups();        
	act = str(act[0]);
        if (user.access < 500):
                message.reply("Only HCs (user level 500+) can boss Webulations around!");
        else:
		if (act == "on"):
			message.reply("Night night.");
			os.system("touch /tmp/meetingmode");
		if (act == "off"):
			os.system("rm /tmp/meetingmode");
			message.reply("Morning!");
