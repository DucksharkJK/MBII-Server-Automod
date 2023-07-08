# AUTOMATIC MOVIE BATTLES II RCON MODERATOR
# CONTACT "devoidjk" ON DISCORD WITH ISSUES, SUGGESTIONS, ETC
# THEORETICALLY COMPATIBLE WITH BOTH VANILLA MBII AND BULLY'S LOG SCHEMA
# LAST EDITED 7/2/23, v0.1

from socket import (socket, AF_INET, SOCK_DGRAM, SHUT_RDWR, timeout as socketTimeout, error as socketError)

# Send commands to the server via rcon. Wrapper class.
class Rcon(object):

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
        output = ''

        while(True): # Make sure an infinite loop is placed until the command is successfully received.
            try:
                send(payload.encode('cp1252'))
                receive = recv(buffer_size)
                if not receive:
                    break

                unfiltered_response = receive.decode('cp1252')
                filtered_response = unfiltered_response.replace("\xFF\xFF\xFF\xFFprint", "")

                output += filtered_response

            except socketTimeout:
                print("timeout")
                return output

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

    def newround(self):
        self._send("\xff\xff\xff\xffrcon %s newround" % (self.rcon_pwd))

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
