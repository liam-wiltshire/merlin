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
from Core.string import decode
from Core.maps import Channel
from Core.config import Config
from Core.loadable import system, loadable, route, require_user


class done(loadable):
    """Webulations ToDo list"""
    usage = ""

    @route(r"(.*)", access = "admin")
    @require_user
    def execute(self, message, user, params):
	comment = params.groups();        
	if (user.access < 500):
		message.reply("Only HCs (user level 500+) can boss Webulations around!");
	else:
		comments = "";
		comments = comments.join(comment).encode('ascii','replace')
		
		session.execute("UPDATE todo SET status = 'complete' WHERE comment LIKE '"+comments+"%'");
