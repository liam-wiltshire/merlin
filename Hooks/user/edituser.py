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
 
from Core.config import Config
from Core.db import session
from Core.maps import User
from Core.chanusertracker import CUT
from Core.loadable import loadable, route, require_user

class edituser(loadable):
    """Used to change a user's access or (de)activate them"""
    usage = " <user> (<access>|true|false)"
    
    @route(r"(.+)\s+(\S+)", access = "hc")
    @require_user
    def execute(self, message, user, params):
        
        usernames = params.group(1)
        access = params.group(2).lower()
        if access.isdigit():
            access = int(access)
        elif access in self.true:
            access = True
        elif access in self.false:
            access = False
        else:
            try:
                access = Config.getint("Access",access)
            except Exception:
                message.reply("Invalid access level '%s'" % (access,))
                return

        addnicks = []
        remnicks = []
        changed = []
        mbraxx = Config.getint("Access","member")
        home = Config.get("Channels","home")
            
        for username in usernames.split():
            member = User.load(name=username, active=False)
            if member is None:
                message.alert("No such user '%s'" % (username,))
                return
            
            if type(access) is int and not member.active:
                message.reply("You should first re-activate user %s" %(member.name,))
                return
            
            if access > user.access or member.access > user.access:
                message.reply("You may not change access higher than your own")
                return

            changed.append(username)

            if type(access) == int:
                if member.active == True and member.access < mbraxx and access >= mbraxx:
                    addnicks.append(member.name)
                if member.active == True and member.access >= mbraxx and access < mbraxx:
                    message.privmsg("remuser %s %s"%(home, member.name,), Config.get("Services", "nick"))
                    remnicks.append(member.name)
    #                message.privmsg("ban %s *!*@%s.%s GTFO, EAAD"%(home, member.name, Config.get("Services", "usermask"),), Config.get("Services", "nick"))
                member.access = access
            else:
                if member.active != access and access == True and member.access >= mbraxx:
                    addnicks.append(member.name)
                if member.active != access and access == False and member.access >= mbraxx:
                    message.privmsg("remuser %s %s"%(home, member.name,), Config.get("Services", "nick"))
                    remnicks.append(member.name)
     #               message.privmsg("ban %s *!*@%s.%s GTFO, EAAD"%(home, member.name, Config.get("Services", "usermask"),), Config.get("Services", "nick"))
                member.active = access
            if not member.active:
                CUT.untrack_user(member.name)
        session.commit()
        if addnicks:
            message.privmsg("adduser %s %s 24" %(home, ",".join(addnicks),), Config.get("Services", "nick"))
            message.reply("%s ha%s been added to %s"%(", ".join(addnicks), "ve" if len(addnicks) > 1 else "s", home,))
        if remnicks:
            message.reply("%s ha%s been removed from %s"%(", ".join(remnicks), "ve" if len(remnicks) > 1 else "s", home,))
        if changed:
            message.reply("Editted user%s %s access to %s" % ("s" if len(changed) > 1 else "", ", ".join(changed), access,))
