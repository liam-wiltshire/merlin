# Bitches

# This file is part of Merlin.
 
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
 
# This work is Copyright (C)2008 of Robin K. Hansen, Elliot Rosemarine.
# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

import re
from .variables import nick, access
from .Core.modules import M
loadable = M.loadable.loadable

class bitches(loadable):
    """List of booked targets by galaxy and alliance"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"bitches(?:\s(\d+))?")
        self.usage += " [minimum eta]"
    
    @loadable.run_with_access(access.get('hc',0) | access.get('bc',access['member']))
    def execute(self, message, user, params):
        
        tick = M.DB.Maps.Updates.current_tick() + (params.group(1) or 1)
        session = M.DB.Session()
        replies = []
        
        Q = session.query(M.DB.Maps.Galaxy, M.DB.SQL.f.count())
        Q = Q.join(M.DB.Maps.Target.planet)
        Q = Q.join(M.DB.Maps.Planet.galaxy)
        Q = Q.filter(M.DB.Maps.Target.tick >= tick)
        Q = Q.group_by(M.DB.Maps.Galaxy.x, M.DB.Maps.Galaxy.y)
        result = Q.all()
        prev = []
        for galaxy, bitches in result:
            prev.append("%s:%s(%s)"%(galaxy.x,galaxy.y,bitches))
        replies.append("Active bookings: " + ", ".join(prev))
        
        Q = session.query(M.DB.Maps.Alliance, M.DB.SQL.f.count())
        Q = Q.select_from(M.DB.Maps.Target)
        Q = Q.outerjoin(M.DB.Maps.Target.planet)
        Q = Q.outerjoin(M.DB.Maps.Planet.alliance)
        Q = Q.filter(M.DB.Maps.Target.tick >= tick)
        Q = Q.group_by(M.DB.Maps.Alliance.name)
        result = Q.all()
        prev = []
        for alliance, bitches in result:
            prev.append("%s (%s)"%(alliance.name if alliance else "Unknown", bitches))
        replies.append("Active bitches: " + ", ".join(prev))
        
        session.close()
        
        if len(replies) < 1:
            replies.append("No active bookings. This makes %s sad. Please don't make %s sad." %(nick,nick))
        message.reply("\n".join(replies))