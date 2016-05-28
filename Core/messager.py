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
 
# The generic objects used to send messages to callbacks and such.

import sys
import re, time
import os.path
import commands
from Core import Merlin
from Core.exceptions_ import ParseError, ChanParseError, MsgParseError, PNickParseError
from Core.config import Config
from Core.string import encode
from Core.actions import Action
import threading
from threading import Timer
from Core.maps import User
from pytg.sender import Sender
from pytg.receiver import Receiver
from pytg.utils import coroutine
from Core.messages import Message
from Core.exceptions_ import Quit, Reboot, Reload



class Messager():
    lastcheck = 0;
    tg = None;
    sender = None
    receiver = None
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
	if (self.sender != None and self.receiver != None):
		print "TG is already running";
	else:
		print "TG isn't running, start";
		self.startTelegram();


    def strip_non_ascii(self,string):	
        ''' Returns the string without non ASCII characters'''
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)

    def startTelegram(self):
	self.receiver = Receiver(host="localhost",port=4458);
	self.sender = Sender(host="localhost",port=4458);
	

    def sendToTG(self,group,msg):
#	print "Skip";
#	if (os.path.isfile("/tmp/meetingmode")):
#		return
#	
	print "SendToTG";
	self.sender.send_msg(unicode(group),unicode(msg));
	print "Done";

    def executeCommand(self,msg,channel,tguser):
	from Core.callbacks import Callbacks
	from Core.actions import Action

	user = User.byTguser(tguser);
	if (msg[0:1] == '%'):
		if (msg == '%whoami'):

			if (tguser == 'nouser'):

				message = Action();
				message.privmsg("You don't have a TG username you donut! Read https://telegram.org/faq#q-what-are-usernames-how-do-i-get-one before you bother me again!",channel);
	                        if (channel == Config.get('gateway','ircchan1')):
        	                        self.sendToTG(Config.get('gateway','tggroup1'),"You don't have a TG username you donut! Read https://telegram.org/faq#q-what-are-usernames-how-do-i-get-one before you bother me again!");
                	        if (channel == Config.get('gateway','ircchan2')):
                        	        self.sendToTG(Config.get('gateway','tggroup2'),"You don't have a TG username you donut! Read https://telegram.org/faq#q-what-are-usernames-how-do-i-get-one before you bother me again!");
	                        if (channel == Config.get('gateway','ircchan3')):
        	                        self.sendToTG(Config.get('gateway','tggroup3'),"You don't have a TG username you donut! Read https://telegram.org/faq#q-what-are-usernames-how-do-i-get-one before you bother me again!");

			else:
				message = Action();
				message.privmsg("Your TG username is "+tguser+". If you havn't already, you need to add this to the bot using .pref tguser="+tguser+"");
	                        if (channel == Config.get('gateway','ircchan1')):
	                                self.sendToTG(Config.get('gateway','tggroup1'),"Your TG username is "+tguser+". If you havn't already, you need to add this to the bot using .pref tguser="+tguser+"");
	                        if (channel == Config.get('gateway','ircchan2')):
	                                self.sendToTG(Config.get('gateway','tggroup2'),"Your TG username is "+tguser+". If you havn't already, you need to add this to the bot using .pref tguser="+tguser+"");
	                        if (channel == Config.get('gateway','ircchan3')):
	                                self.sendToTG(Config.get('gateway','tggroup3'),"Your TG username is "+tguser+". If you havn't already, you need to add this to the bot using .pref tguser="+tguser+"");
				


		elif (user is None):
			message = Action();
			message.privmsg("You must be registered with BowBot and have your TG user set to send commands from TG",channel);
			if (channel == Config.get('gateway','ircchan1')):
				self.sendToTG(Config.get('gateway','tggroup1'),"You must be registered with BowBot and have your TG user set to send commands from TG");
			if (channel == Config.get('gateway','ircchan2')):
                                self.sendToTG(Config.get('gateway','tggroup2'),"You must be registered with BowBot and have your TG user set to send commands from TG");
			if (channel == Config.get('gateway','ircchan3')):
                                self.sendToTG(Config.get('gateway','tggroup3'),"You must be registered with BowBot and have your TG user set to send commands from TG");

			
		else:
			msg = '!' + msg.lstrip("%");
			line = ":"+str(user.name)+"!~"+str(user.name)+"@"+str(user.name)+".users.netgamers.org PRIVMSG "+channel+" :"+msg+"";
			message = Action()
			message.parse(line);
			callback = Callbacks.callback(message);

    def sendExternal(self,message):
        if (message._command == "PART" or message._command == "QUIT" or message._command == "KICK" or message._command == "KILL"):
                #Do we have a group for this channel
                if (message._channel == Config.get('gateway','ircchan1')):
                        if (Config.get('gateway','tggroup1') != ""):
                                self.sendToTG(Config.get('gateway','tggroup1'),'[IRC:'+message._nick+'@'+message._channel+'] '+message._nick+' has left '+message._channel);

                if (message._channel == Config.get('gateway','ircchan2')):
                        if (Config.get('gateway','tggroup2') != ""):
                                self.sendToTG(Config.get('gateway','tggroup2'),'[IRC:'+message._nick+'@'+message._channel+'] '+message._nick+' has left '+message._channel);


                if (message._channel == Config.get('gateway','ircchan3')):
                        if (Config.get('gateway','tggroup3') != ""):
                                self.sendToTG(Config.get('gateway','tggroup3'),'[IRC:'+message._nick+'@'+message._channel+'] '+message._nick+' has left '+message._channel);

	if (message._command == "JOIN"):
                #Do we have a group for this channel
                if (message._channel == Config.get('gateway','ircchan1')):
                        if (Config.get('gateway','tggroup1') != ""):
                                self.sendToTG(Config.get('gateway','tggroup1'),'[IRC:'+message._nick+'@'+message._channel+'] '+message._nick+' has joined '+message._channel);

                if (message._channel == Config.get('gateway','ircchan2')):
                        if (Config.get('gateway','tggroup2') != ""):
                                self.sendToTG(Config.get('gateway','tggroup2'),'[IRC:'+message._nick+'@'+message._channel+'] '+message._nick+' has joined '+message._channel);


                if (message._channel == Config.get('gateway','ircchan3')):
                        if (Config.get('gateway','tggroup3') != ""):
                                self.sendToTG(Config.get('gateway','tggroup3'),'[IRC:'+message._nick+'@'+message._channel+'] '+message._nick+' has joined '+message._channel);
	
	if (message._command == "PRIVMSG" and message._msg[0:5] != '[IRC:' and message._msg[0:4] != '[WA:' and message._msg[0:4] != '[TG:' ):
		#Do we have a group for this channel
		if (message._channel == Config.get('gateway','ircchan1')):
			if (Config.get('gateway','tggroup1') != ""):
				self.sendToTG(Config.get('gateway','tggroup1'),'[IRC:'+message._nick+'@'+message._channel+'] '+message._msg+'');

		if (message._channel == Config.get('gateway','ircchan2')):
			if (Config.get('gateway','tggroup2') != ""):
				self.sendToTG(Config.get('gateway','tggroup2'),'[IRC:'+message._nick+'@'+message._channel+'] '+message._msg+'');


		if (message._channel == Config.get('gateway','ircchan3')):
			if (Config.get('gateway','tggroup3') != ""):
				self.sendToTG(Config.get('gateway','tggroup3'),'[IRC:'+message._nick+'@'+message._channel+'] '+message._msg+'');


    def startTGCheck(self):
	t = Timer(5.0,self.checkTG).start();
	

    def checkTG(self):
	print "CheckTG Started";
	print "Running Threads: "+str(threading.activeCount());
	t = Timer(2400.0,self.checkTG).start();
	#print "Stop Old Receviver";
	if (self.receiver):
		try:
			self.receiver.stop();
			print "Receiver stopped ok";
		except:
			print "Unexpected error:", sys.exc_info()[0];
	try:
		print "Start TG Checker";
		self.receiver = Receiver(host="localhost",port=4458);
		self.receiver.start();
		self.receiver.message(self.example_function(self.receiver));
		self.receiver.stop();
		print "TG CHeck has stopped....";
		self.checkTG();
	except TypeError:
		print "Should really figure out where these type-errors come from";
	except:
		print sys.exc_info();
		print "Unexpected error 2:", sys.exc_info()[0];
		self.checkTG();
	return;

    @coroutine
    def example_function(self,receiver):
	try:
		while True:
                        print "Check";
                        msg = (yield)
                        act = Action();
                        print('Full dump: {array}'.format(array=str( msg )))
		
			if (msg.event == 'message'):
				if (hasattr(msg.sender,'username')):
					user = User.byTguser(msg.sender.username);
	
			                if user is not None:
		        	                displayUser = str(user.name);
					else:
						displayUser = str(msg.sender.name);
				else:
					displayUser = str(msg.sender.name);
					msg.sender.username = 'nouser';
	
	
	
				msg.text = self.strip_non_ascii(msg.text);
				if (msg.receiver and str(msg.receiver.name) == Config.get("gateway","tggroup1") and msg.text[0:5] != '[IRC:' and msg.text[0:4] != '[WA:' and msg.text[0:4] != '[TG:' ):
					print "Send message to " + Config.get("gateway","ircchan1");
					self.actions = Action.privmsg(act,"[TG:"+displayUser+"] " + (msg.text.encode('utf_8','ignore')) , Config.get("gateway","ircchan1"))
					self.executeCommand(msg.text.encode('utf_8','ignore'),Config.get("gateway","ircchan1"),str(msg.sender.username));
	
				if (msg.receiver and str(msg.receiver.name) == Config.get("gateway","tggroup2") and msg.text[0:5] != '[IRC:' and msg.text[0:4] != '[WA:' and msg.text[0:4] != '[TG:' ):
					print "Send message to " + Config.get("gateway","ircchan2");
					self.actions = Action.privmsg(act,"[TG:"+displayUser+"] " + (msg.text.encode('utf_8','ignore')) , Config.get("gateway","ircchan2"))
					self.executeCommand(msg.text.encode('utf_8','ignore'),Config.get("gateway","ircchan2"),str(msg.sender.username));
	
				if (msg.receiver and str(msg.receiver.name) == Config.get("gateway","tggroup3") and msg.text[0:5] != '[IRC:' and msg.text[0:4] != '[WA:' and msg.text[0:4] != '[TG:' ):
					print "Send message to " + Config.get("gateway","ircchan3");
					self.actions = Action.privmsg(act,"[TG:"+displayUser+"] " + (msg.text.encode('utf_8','ignore')) , Config.get("gateway","ircchan3"))
					self.executeCommand(msg.text.encode('utf_8','ignore'),Config.get("gateway","ircchan3"),str(msg.sender.username));
			else:
				print "Not A Message";

	except AttributeError:
		print sys.exc_info();
		print "Nothing we need to worry about...";
		receiver.stop();
		self.checkTG();
	except UnicodeEncodeError:
		print "Characters we can't deal with!";
	except KeyboardInterrupt:
		receiver.stop()
		print("Exiting")




