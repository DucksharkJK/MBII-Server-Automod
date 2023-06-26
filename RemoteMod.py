# AUTOMATIC MOVIE BATTLES II RCON MODERATOR
# CONTACT "devoidjk" ON DISCORD WITH ISSUES, SUGGESTIONS, ETC
# COMPATIBLE WITH BOTH VANILLA MBII AND BULLY'S LOG SCHEMA
# LAST EDITED 6/25/23, v0.1

import discord
import datetime
from socket import (socket, AF_INET, SOCK_DGRAM, SHUT_RDWR, timeout as socketTimeout, error as socketError)

import time

from RemoteModParser import parser, modification

# Load bot permissions
intents = discord.Intents.default()
intents.message_content = True

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = intents)
        self.synced = False # prevent multiple syncs
        self.added = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync(guild = discord.Object(guild_id))
            self.synced = True
        if not self.added:
            self.added = True
        print(f"Remote Mod Online.")

current_date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

client = aclient()
tree = discord.app_commands.CommandTree(client)
guild_id = 902568491218002010 # ID of guild the bot will operate in
TOKEN = "MTA3NTA2NTI5NjkxMTU5NzY1MA.G7LXDp.tPIvcxNgkCCKqQK1wkj2InFhzRccqb-DQrIOl0" # Token of bot to use.
log_path = "C:\Program Files\Star Wars Jedi Knight - Jedi Academy\GameData\MBII\games.log" # Path of logging file to tail

# Making blank server slots. Template is serverslot:["in-game name", "IP address", "team", # of chat infractions, # of teamkills, rounds played]
server_slots = {}
for x in range(0, 32):
    server_slots[x]=["", "", "", 0, 0, 0]

def follow(log_file):
    log_file.seek(0,2)
    while True:
        line = log_file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def log_tailing():
    logfile = open(log_path)
    loglines = follow(logfile)
    for line in loglines:
        timestamp = line[:7]
        content = line[7:]
        line_content = parser(timestamp, content)
        modification(line_content)

log_tailing()

class Rcon(object):

    """Send commands to the server via rcon. Wrapper class."""

    def __init__(self, address, bindaddr, rcon_pwd):

        address_list = str.split(str.strip(address), ":")
        address_list[1] = int(address_list[1])
        self.address = tuple(address_list)
        self.bindaddr = bindaddr
        self.rcon_pwd = rcon_pwd

    def _send(self, payload, buffer_size=1024): # This method shouldn't be used outside the scope of this object's wrappers.
        sock = socket(AF_INET, SOCK_DGRAM) # Socket descriptor sending/receiving rcon commands to/from the server.
        sock.bind((self.bindaddr, 0)) # Setting port as 0 will let the OS pick an available port for us.
        sock.settimeout(1)
        sock.connect(self.address)
        send = sock.send
        recv = sock.recv

        while(True): # Make sure an infinite loop is placed until the command is successfully received.
            try:
                send(payload.encode('cp1252'))
                receive = recv(buffer_size)
                if not receive:
                    break

                unfiltered_response = receive.decode('cp1252')
                filtered_response = unfiltered_response.replace("\xFF\xFF\xFF\xFFprint", "")

                print(filtered_response)

            except socketTimeout:
                print("timeout")
                continue
            except socketError:
                print("error")
                break
        
        sock.shutdown(SHUT_RDWR)
        sock.close()

    def say(self, msg):
        self._send("\xff\xff\xff\xffrcon %s say %s" % (self.rcon_pwd, msg), 2048)

    def svsay(self, msg):
        self._send("\xff\xff\xff\xffrcon %s svsay %s" % (self.rcon_pwd, msg))

    def status(self):
        self._send("\xff\xff\xff\xffrcon %s status" % (self.rcon_pwd))

    def who(self):
        self._send("\xff\xff\xff\xffrcon %s who" % (self.rcon_pwd))

    def map(self, map_name):
        self._send("\xff\xff\xff\xffrcon %s map %f" % (self.rcon_pwd, map_name))

    def mbmode(self, cmd):
        self._send("\xff\xff\xff\xffrcon %s mbmode %s" % (self.rcon_pwd, cmd))

    def tempmute(self, player_id, duration):
        self._send("\xff\xff\xff\xffrcon %s mute %i %f" % (self.rcon_pwd, player_id, duration))

    def unmute(self, player_id):
        self._send("\xff\xff\xff\xffrcon %s unmute %i" % (self.rcon_pwd, player_id))

    def settk(self, player_id, tk_points):
        self._send("\xff\xff\xff\xffrcon %s settk %i %f" % (self.rcon_pwd, player_id, tk_points))

    def marktk(self, player_id, duration):
        self._send("\xff\xff\xff\xffrcon %s marktk %i %f" % (self.rcon_pwd, player_id, duration))    

    def clientkick(self, player_id):
        self._send("\xff\xff\xff\xffrcon %s clientkick %i" % (self.rcon_pwd, player_id))

    def tempban(self, player_id, rounds):
        self._send("\xff\xff\xff\xffrcon %s tempban %i %f" % (self.rcon_pwd, player_id, rounds))

rcon = Rcon("192.168.1.223:29071", "0.0.0.0", "operation")

@tree.command(description='Broadcasts message as server in game chat', guild=discord.Object(guild_id))
async def svsay(interaction: discord.Interaction, message: str):
    if len(message) < 142:
        rcon.svsay(f"{message}")
        await interaction.response.send_message(f'/rcon svsay **{message}** was sent by {interaction.user.mention} at {current_date_time}!', allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    else:
        await interaction.response.send_message('Your message must be 141 characters or shorter. Please try again!', ephemeral = True)

@tree.command(description='Kicks user from the server', guild=discord.Object(guild_id))
async def kick(interaction: discord.Interaction, client_id: str):
    rcon.clientkick(f"{client_id}")
    await interaction.response.send_message(f'/rcon clientkick **{client_id}** was sent by {interaction.user.mention} at {current_date_time}!', allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))

# client.run(TOKEN)