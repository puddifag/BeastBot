#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   BeastBot.py - A custom, from scratch IRC bot
#   Copyright (C) 2015 Spacecow99
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import sys
import socket
import os.path
import logging
import argparse
import ConfigParser
import re
import urllib
import json
import time

def main():
    irc = CreateSocket()
    conf = getConfig()
    while True:
        try:
            line = irc.recv(2048)
        except:
            print "IRC Socket Disconnected"
            wait = input('Press enter to continue')
            exit()
        if line:
            print line
        splitline = line.split(" :")
        try:
            message = splitline[1]
            messagechars = message
            message = message.split(" ")
            username = line.split("!")[0].replace(':', '')
            msgto = line.split(" ")[2]
            command = message[0]
        except IndexError:
            command = ""
            #error handling goes here
            pass
        except Exception:
            #error handling goes here
            print "Shit just got real"
            pass
        if splitline[0] == "PING":
            pong = "PONG %s" % splitline[1]
            irc.send(pong)
        elif messagechars[0] == conf['cominit']:
            command = command[1:]
            command = command.strip()
            if command == "about":
                ircSay(username, conf['aboutmessage'], irc)
            elif command == "help":
                ircSay(username, "Still in construction", irc)
            elif command == "nick":
                if username in conf['admins'].split(" "):
                    if (isRegged(username, irc)):
                        ircNick(message[1], irc)
            elif command == "join":
                if username in conf['admins'].split(" "):
                    if (isRegged(username, irc)):
                        ircJoin(message[1], irc)
            elif command == "part":
                if username in conf['admins'].split(" "):
                    if (isRegged(username, irc)):
                        ircPart(message[1], irc)
            elif command == "joinmain":
                if username in conf['admins'].split(" "):
                    if (isRegged(username, irc)):
                        splitchannels = conf['channels'].split(" ")
                        for chan in splitchannels:
                            ircJoin(chan, irc)
            elif command == "reload":
                if username in conf['admins'].split(" "):
                    if (isRegged(username, irc)):
                        conf = getConfig()
                        ircSay(msgto, "Configuration Reloaded...", irc)
            elif command == "quit":
                if username in conf['admins'].split(" "):
                    if (isRegged(username, irc)):
                        ircSay(msgto, "Shutting Down....", irc)
                        time.sleep(4)
                        irc.close()
                        exit()
            elif command == "urban":
                try:
                    if message[1]:
                        url = 'http://api.urbandictionary.com/v0/define?term='+message[1]
                        info = urllib.urlopen(url)
                        data = json.loads(info.read())
                        try:
                            definition = data['list'][0]['definition']
                            thumbsup = data['list'][0]['thumbs_up']
                            thumbsdown = data['list'][0]['thumbs_down']
                            thumbsdown = str(thumbsdown)
                            thumbsup = str(thumbsup)
                            msg = message[1].strip()
                            output = msg+": "+definition+" Up:"+thumbsup+" Down: "+thumbsdown
                            ircSay(msgto, output, irc)
                        except IndexError:
                            #need error handling
                            ircSay(msgto, "No definition for: "+message[1], irc)
                        except Exception:
                            #need error handling
                            print "Shit just got real"
                except IndexError:
                    #need error handling
                    ircSay(msgto, username+" is a dumbass and didn't enter a term to search for....", irc)
                except Exception:
                    #need error handling
                    print "Shit just got real"
        elif re.match(":r2d2.evilzone.org 001 "+conf['nick']+" :Welcome", line):
            splitchannels = conf['channels'].split(" ")
            for chan in splitchannels:
                irc.send("JOIN %s\n" % (chan))

def CreateSocket():
    conf = getConfig()
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((conf['server'], int(conf['port'])))
    irc.send('NICK '+conf['nick']+'\r\n')
    irc.send('USER test test test :test\r\n')
    return irc


def getConfig():
    config = ConfigParser.RawConfigParser()
    config.read('conf/beastbot.conf')
    conf = dict(config.items('Main'))
    return conf

###############
#IRC Functions#
###############

def ircMode(chan, args, irc):
    irc.send("MODE args, irc")

def ircSay(to, msg, irc):
#to=message to, msg=message to send, irc=socket
    irc.send("PRIVMSG %s :%s\n" % (to, msg))


def ircJoin(channel, irc):
#channel=channel to join, irc=socket
    irc.send("JOIN %s\n" % (channel))


def ircPart(channel, irc):
#channel=channel to part, irc=socket
    irc.send("PART %s\n" % (channel))


def ircNick(newnick, irc):
#newnick=New nickname for the bot, irc=socket
    irc.send("NICK %s\n" % (newnick))


def isRegged(nick, irc):
    #true if Nickserv says he's registered
    ircSay("NickServ","STATUS %s " % (nick),irc)
    line = ""
    while line is "":
        line = irc.recv(2048)
        print "REG TEST" + line
        if line.find("STATUS %s 3" % (nick)) != -1:
            return True
        else:
            return False


if __name__ == "__main__":
    main()