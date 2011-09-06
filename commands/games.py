# Copyright 2011 orabot Developers
#
# This file is part of orabot, which is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygeoip
import sqlite3
import re
import urllib.request
import time
import yaml

def get_map_info(self, cur, sha):
    sql = "SELECT title,players FROM maps WHERE hash = '%s'" % sha
    cur.execute(sql)
    records = cur.fetchall()
    if len(records):
        return (records[0][0], '/' + records[0][1])
    else:
        return ('unknown', '')

def games(self, user, channel):
    command = (self.command)
    command = command.split()
    url = 'http://master.open-ra.org/list.php'
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    flood_protection = 0
    if ( len(command) == 1 ):
        content = urllib.request.urlopen(url).read().decode('utf-8')
        y = yaml.load(content.replace('\t','    '))
        if (len(y.keys()) == 0):
            self.send_reply( ("No games found"), user, channel )
        else:
            count='0'
            for game in y.itervalues():
                if ( game['State'] == 1 ):
                    count='1'   # lock - there are games in State: 1
                    state = '(W)'
                    ### for location
                    ip = " ".join(game['Address'].split(':')[0:-1])    # ip address
                    gi = pygeoip.GeoIP('../GeoIP.dat')
                    country = gi.country_name_by_addr(ip).upper()   #got country name
                    ###
                    sname = game['Name']
                    if ( len(sname) == 0 ):
                        sname = 'noname'

                    map_name, max_players = self.get_map_info(cur, game['Map'])
                    players = str(game['Players'])
                    modinfo = game['Mods'].split('@')
                    games = '@ '+sname.strip().ljust(15)+' - '+state+' - Players: '+players+max_players+' - Map: '+map_name+' - '+(modinfo[0].upper()+'@'+ modinfo[1]).ljust(20)+' - '+country
                    time.sleep(0.5)
                    flood_protection = flood_protection + 1
                    if flood_protection == 7:
                        time.sleep(5)
                        flood_protection = 0
                    self.send_reply( (games), user, channel )
            flood_protection = 0
            if ( count == "0" ):    #appeared no games in State: 1
                self.send_reply( ("No games waiting for players found"), user, channel )           
    elif ( len(command) == 2 ):   # ]games with args
        content = urllib.request.urlopen(url).read().decode('utf-8')
        y = yaml.load(content.replace('\t','    '))
        keys_list = y.keys()
        if ( len(keys_list) == 0 ):
            self.send_reply( ("No games found"), user, channel )
        else:   # there are one or more games
            if ( command[1] == "-w" ):   #request games in State = 1
                count='0'
                for i in range(int(len(keys_list))):
                    if ( y['Game@'+str(i)]['State'] == 1 ):
                        count='1'   # lock - there are games in State: 1
                        state = '(W)'
                        ### for location
                        ip = " ".join(y['Game@'+str(i)]['Address'].split(':')[0:-1])    # ip address
                        gi = pygeoip.GeoIP('../GeoIP.dat')
                        country = gi.country_name_by_addr(ip).upper()   #got country name
                        ###
                        sname = y['Game@'+str(i)]['Name']
                        if ( len(sname) == 0 ):
                            sname = 'noname'
                        sql = """SELECT title,players FROM maps
                                WHERE hash = '"""+y['Game@'+str(i)]['Map']+"""'
                        """
                        cur.execute(sql)
                        records = cur.fetchall()
                        conn.commit()
                        if ( len(records) != 0 ):
                            map_name = records[0][0]
                            max_players = '/'+str(records[0][1])
                        else:
                            map_name = 'unknown'
                            max_players = ''
                        players = str(y['Game@'+str(i)]['Players'])
                        modinfo = y['Game@'+str(i)]['Mods'].split('@')
                        games = '@ '+sname.strip().ljust(15)+' - '+state+' - Players: '+players+max_players+' - Map: '+map_name+' - '+(modinfo[0].upper()+'@'+ modinfo[1]).ljust(20)+' - '+country
                        time.sleep(0.5)
                        flood_protection = flood_protection + 1
                        if flood_protection == 7:
                            time.sleep(5)
                            flood_protection = 0
                        self.send_reply( (games), user, channel )
                flood_protection = 0
                if ( count == "0" ):
                    self.send_reply( ("No games waiting for players found"), user, channel )
            elif ( command[1] == "-p" ):     # request games in State = 2
                count = '0'
                for i in range(int(len(keys_list))):
                    if ( y['Game@'+str(i)]['State'] == 2 ):
                        count='1'   # lock - there are games in State: 2
                        state = '(P)'
                        ### for location
                        ip = " ".join(y['Game@'+str(i)]['Address'].split(':')[0:-1])    # ip address
                        gi = pygeoip.GeoIP('../GeoIP.dat')
                        country = gi.country_name_by_addr(ip).upper()   #got country name
                        ###
                        sname = y['Game@'+str(i)]['Name']
                        if ( len(sname) == 0 ):
                            sname = 'noname'
                        sql = """SELECT title,players FROM maps
                                WHERE hash = '"""+y['Game@'+str(i)]['Map']+"""'
                        """
                        cur.execute(sql)
                        records = cur.fetchall()
                        conn.commit()
                        if ( len(records) != 0 ):
                            map_name = records[0][0]
                            max_players = '/'+str(records[0][1])
                        else:
                            map_name = 'unknown'
                            max_players = ''
                        players = str(y['Game@'+str(i)]['Players'])
                        modinfo = y['Game@'+str(i)]['Mods'].split('@')
                        games = '@ '+sname.strip().ljust(15)+' - '+state+' - Players: '+players+max_players+' - Map: '+map_name+' - '+(modinfo[0].upper()+'@'+ modinfo[1]).ljust(20)+' - '+country
                        time.sleep(0.5)
                        flood_protection = flood_protection + 1
                        if flood_protection == 7:
                            time.sleep(5)
                            flood_protection = 0
                        self.send_reply( (games), user, channel )
                flood_protection = 0
                if ( count == "0" ):    #appeared no games in State: 2
                    self.send_reply( ("No started games found"), user, channel )
            elif ( (command[1] == "--all") or (command[1] == "-wp") ): # request games in both states
                for i in range(int(len(keys_list))):
                    if ( y['Game@'+str(i)]['State'] == 1 ):
                        state = '(W)'
                    elif ( y['Game@'+str(i)]['State'] == 2 ):
                        state = '(P)'
                    ### for location
                    ip = " ".join(y['Game@'+str(i)]['Address'].split(':')[0:-1])    # ip address
                    gi = pygeoip.GeoIP('../GeoIP.dat')
                    country = gi.country_name_by_addr(ip).upper()   #got country name
                    ###
                    sname = y['Game@'+str(i)]['Name']
                    if ( len(sname) == 0 ):
                        sname = 'noname'
                    sql = """SELECT title,players FROM maps
                            WHERE hash = '"""+y['Game@'+str(i)]['Map']+"""'
                    """
                    cur.execute(sql)
                    records = cur.fetchall()
                    conn.commit()
                    if ( len(records) != 0 ):
                        map_name = records[0][0]
                        max_players = '/'+str(records[0][1])
                    else:
                        map_name = 'unknown'
                        max_players = ''
                    players = str(y['Game@'+str(i)]['Players'])
                    modinfo = y['Game@'+str(i)]['Mods'].split('@')
                    games = '@ '+sname.strip().ljust(15)+' - '+state+' - Players: '+players+max_players+' - Map: '+map_name+' - '+(modinfo[0].upper()+'@'+ modinfo[1]).ljust(20)+' - '+country
                    time.sleep(0.5)
                    flood_protection = flood_protection + 1
                    if flood_protection == 7:
                        time.sleep(5)
                        flood_protection = 0
                    self.send_reply( (games), user, channel )
                flood_protection = 0
            elif ( (command[1]) == "-s" ):
                games_state1 = ''
                games_state2 = ''
                for i in range(int(len(keys_list))):
                    if ( y['Game@'+str(i)]['State'] == 1 ):
                        state = 'W'
                    elif ( y['Game@'+str(i)]['State'] == 2 ):
                        state = 'P'
                    sname = y['Game@'+str(i)]['Name']
                    if ( len(sname) == 0 ):
                        sname = 'noname'
                    modinfo = y['Game@'+str(i)]['Mods'].split('@')
                    players = str(y['Game@'+str(i)]['Players'])
                    if ( state == 'W' ):
                        games_state1 = games_state1+'\t['+players+'] '+sname.strip()+' ('+(modinfo[0].upper()+'@'+ modinfo[1])+')||'
                    elif ( state == 'P' ):
                        games_state2 = games_state2+'\t['+players+'] '+sname.strip()+' ('+(modinfo[0].upper()+'@'+ modinfo[1])+')||'
                split_games_state1 = games_state1.split('||')
                split_games_state2 = games_state2.split('||')
                if ( len(split_games_state2) > 1 ):
                    self.send_reply( ('Playing:'), user, channel )
                    for i in range(int(len(split_games_state2) - 1)):
                        flood_protection = flood_protection + 1
                        if flood_protection == 7:
                            time.sleep(5)
                            flood_protection = 0
                        self.send_reply( (split_games_state2[i]), user, channel )
                        time.sleep(0.5)
                if ( len(split_games_state1) > 1 ):
                    self.send_reply( ('Waiting:'), user, channel )
                    for i in range(int(len(split_games_state1) - 1)):
                        flood_protection = flood_protection + 1
                        if flood_protection == 7:
                            time.sleep(5)
                            flood_protection = 0
                        self.send_reply( (split_games_state1[i]), user, channel )
                        time.sleep(0.5)
                flood_protection = 0
            elif ( (command[1]) == "-r" ):
                self.send_reply( ("A pattern required"), user, channel )
            else:
                self.send_reply( ("Incorrect option!"), user, channel )
    elif ( len(command) > 2 ):
        if ( command[1] == "-r" ):  #patter request
            content = urllib.request.urlopen(url).read().decode('utf-8')
            y = yaml.load(content.replace('\t','    '))
            keys_list = y.keys()
            if ( len(keys_list) == 0 ):
                self.send_reply( ("No games found"), user, channel )
            else:   # there are one or more games
                chars=['*','.','$','^','@','{','}','+','?'] # chars to ignore
                request_pattern = " ".join(command[2:])
                for i in range(int(len(chars))):
                    if chars[i] in request_pattern:
                        check = 'tru'
                        break
                    else:
                        check = 'fals'
                if ( check == 'fals' ):     #requested pattern does not contain any of 'forbidden' chars
                    p = re.compile(request_pattern, re.IGNORECASE)
                    count='0'
                    for i in range(int(len(keys_list))):
                        sname = y['Game@'+str(i)]['Name']
                        if p.search(sname):
                            count='1'   # lock
                            if ( y['Game@'+str(i)]['State'] == 1 ):
                                state = '(W)'
                            elif ( y['Game@'+str(i)]['State'] == 2 ):
                                state = '(P)'
                            ### for location
                            ip = " ".join(y['Game@'+str(i)]['Address'].split(':')[0:-1])    # ip address
                            gi = pygeoip.GeoIP('../GeoIP.dat')
                            country = gi.country_name_by_addr(ip).upper()   #got country name
                            ###
                            if ( len(sname) == 0 ):
                                sname = 'noname'
                            sql = """SELECT title,players FROM maps
                                    WHERE hash = '"""+y['Game@'+str(i)]['Map']+"""'
                            """
                            cur.execute(sql)
                            records = cur.fetchall()
                            conn.commit()
                            if ( len(records) != 0 ):
                                map_name = records[0][0]
                                max_players = '/'+str(records[0][1])
                            else:
                                map_name = 'unknown'
                                max_players = ''
                            players = str(y['Game@'+str(i)]['Players'])
                            modinfo = y['Game@'+str(i)]['Mods'].split('@')
                            games = '@ '+sname.strip().ljust(15)+' - '+state+' - Players: '+players+max_players+' - Map: '+map_name+' - '+(modinfo[0].upper()+'@'+ modinfo[1]).ljust(20)+' - '+country
                            time.sleep(0.5)
                            flood_protection = flood_protection + 1
                            if flood_protection == 7:
                                time.sleep(5)
                                flood_protection = 0
                            self.send_reply( (games), user, channel )
                    flood_protection = 0
                    if ( count == "0" ):    #appeared no matches
                        self.send_reply( ("No matches"), user, channel )
        else:
            self.send_reply( ("Error, wrong request"), user, channel )
    else:
        self.send_reply( ("Error, wrong request"), user, channel )
    cur.close()
