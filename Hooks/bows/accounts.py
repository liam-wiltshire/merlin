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
import threading
from Core import Merlin
from Core.db import session
from Core.maps import Channel
from Core.config import Config
from Core.loadable import system, loadable, route


class accounts(loadable):
    """Show the current status of Bows accounts"""
    usage = ""

    @route()    
    def execute(self, message, user, params):

	# Download the Python helper library from twilio.com/docs/python/install	
	from twilio.rest import TwilioRestClient
	
	# Your Account Sid and Auth Token from twilio.com/user/account
	client = TwilioRestClient(Config.get("Twilio", "sid"), Config.get("Twilio", "auth_token"))
	
	# A list of record objects with the properties described above
	records = client.usage.records.list(category="totalprice")


	print records[0].price;
	



