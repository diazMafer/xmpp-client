import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
import xmpp, sys
import base64
import time
import threading
import binascii
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme
from rich.table import Table
from rich.measure import Measurement
from rich import box
from rich.text import Text
from rich.console import Console


class EmailHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""

    base_style = "example."
    highlights = [r"(?P<email>[\w-]+@([\w-]+\.)+[\w-]+)"]


theme = Theme({"example.email": "bold magenta"})
console = Console(highlighter=EmailHighlighter(), theme=theme)

#Clase base tomada de https://gist.github.com/deckerego/be1abbc079b206b793cf/revisions 
#Los métodos en que se difiere fueron agregados en base a la documentos y los xp e iq 
#a agregar con la clase sleekxmpp

def register(user, passw):
    usuario = user
    password = passw
    jid = xmpp.JID(usuario)
    cli = xmpp.Client(jid.getDomain(), debug=[])
    cli.connect()

    if xmpp.features.register(cli,jid.getDomain(),{'username':jid.getNode(),'password':password}):
        return 1
    else:
        return 0


class Client(sleekxmpp.ClientXMPP):
    def __init__(self, username, password, instance_name=None):
        jid = "%s/%s" % (username, instance_name) if instance_name else username
        super(Client, self).__init__(jid, password)

        self.instance_name = instance_name
        self.username = username
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.receive)
        self.add_event_handler("changed_subscription", self.alertFriend)
        self.add_event_handler("changed_status", self.wait_for_presences)

        self.received = set()
        self.contacts = []
        self.presences_received = threading.Event()
        
        self.register_plugin('xep_0077')
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0096') # Jabber Search
        self.register_plugin('xep_0065')
        self.register_plugin('xep_0047', {
            'auto_accept': True
        })

        if self.connect():
            console.print(":waving_hand:" + "You have succesfully sign in")
            self.process(block=False)
        else:
            raise Exception("Unable to connect to Redes Jabber server")

    def logout(self):
        self.disconnect(wait=False)

    def sendPresenceMessage(self, status, body):
        #conectar
        #ingresar a un room
        #actualizar manual 
        self.send_presence()

    def start(self, event):
        self.send_presence(pshow='chat', pstatus='Disponible')
        roster = self.get_roster()
        for r in roster['roster']['items'].keys():
            self.contacts.append(r)
        for jid in self.contacts:
            #to everyone in rooster send i just log in as an active notification
            self.sendNotification(jid, 'Im ready to start messaging', 'active')
        
                
    #example code to iterate all roster including groups took from rooster_browser https://github.com/fritzy/SleekXMPP/blob/develop/examples/roster_browser.py
    def listFriends(self):
        try:
            self.get_roster()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')
        self.send_presence()


        print('Waiting for presence updates...\n')
        self.presences_received.wait(5)

        print('Roster for %s' % self.boundjid.bare)
        groups = self.client_roster.groups()
        
        data = []
        for group in groups:
            print('\n%s' % group)
            print('-' * 72)
            
            for jid in groups[group]:
                temp = []
                self.contacts.append(jid)
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                connections = self.client_roster.presence(jid)
                show = 'available'
                status = ''
                for res, pres in connections.items():
                    if pres['show']:
                        show = pres['show']
                    
                    if pres['status']:
                        status = pres['status']
                

                temp.append(name)
                temp.append(jid)
                temp.append(sub)
                temp.append(status)
                temp.append(res+show)
                
                data.append(temp)
        return data

    
    def send_file(self, recipient, filename):
        message = ''
        with open(filename, "rb") as img_file:
            message = base64.b64encode(img_file.read()).decode('utf-8')
        try:
            self.send_message(mto=recipient,mbody=message,mtype="chat")
        except IqError as e:
            raise Exception("Unable to send image", e)
        except IqTimeout:
            raise Exception("Server not responding")


    #metodo tomado del ejemplo de rooster_browser de https://github.com/fritzy/SleekXMPP/blob/develop/examples/roster_browser.py
    def wait_for_presences(self, pres):
        """
        Track how many roster entries have received presence updates.
        """
        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

    def alertFriend(self):
        self.get_roster()
    
    def sendNotification(self, to, body, ntype):
        message = self.Message()
        message['to'] = to
        message['type'] = 'chat'
        message['body'] = body
        if (ntype == 'active'):
            itemXML = ET.fromstring("<active xmlns='http://jabber.org/protocol/chatstates'/>")
        elif (ntype == 'composing'):
            itemXML = ET.fromstring("<composing xmlns='http://jabber.org/protocol/chatstates'/>")
        elif (ntype == 'inactive'):
            itemXML = ET.fromstring("<inactive xmlns='http://jabber.org/protocol/chatstates'/>")
            #mandar notificacion a todos los contactos de notificacion

        message.append(itemXML)
        try:
            message.send()
        except IqError as e:
            raise Exception("Unable to send active notification", e)
            sys.exit(1)
        except IqTimeout:
            raise Exception("Server not responding")
        
    def listUsers(self):
        users = self.Iq()
        users['type'] = 'set'
        users['to'] = 'search.redes2020.xyz'
        users['from'] = self.boundjid.bare
        users['id'] = 'search_result'
        itemXML = ET.fromstring("<query xmlns='jabber:iq:search'>\
                                 <x xmlns='jabber:x:data' type='submit'>\
                                    <field type='hidden' var='FORM_TYPE'>\
                                        <value>jabber:iq:search</value>\
                                    </field>\
                                    <field var='Username'>\
                                        <value>1</value>\
                                    </field>\
                                    <field var='search'>\
                                        <value>*</value>\
                                    </field>\
                                </x>\
                                </query>")
        users.append(itemXML)
        try:
            x = users.send()
            print(x)
        except IqError as e:
            raise Exception("Unable list users", e)
            sys.exit(1)
        except IqTimeout:
            raise Exception("Server not responding")   
    

    def getUserInfo(self, jid):
        user = self.Iq()
        user['type'] = 'set'
        user['to'] = 'search.redes2020.xyz'
        user['from'] = self.boundjid.bare
        user['id'] = 'search_result'
        query = "<query xmlns='jabber:iq:search'>\
                                 <x xmlns='jabber:x:data' type='submit'>\
                                    <field type='hidden' var='FORM_TYPE'>\
                                        <value>jabber:iq:search</value>\
                                    </field>\
                                    <field var='Username'>\
                                        <value>1</value>\
                                    </field>\
                                    <field var='search'>\
                                        <value>" + jid + "</value>\
                                    </field>\
                                </x>\
                                </query>"
        itemXML = ET.fromstring(query)
        user.append(itemXML)
        try:
            x = user.send()
            print(x)
        except IqError as e:
            raise Exception("Unable to get user information", e)
        except IqTimeout:
            raise Exception("Server not responding")   
        

    def addRoster(self, jid, name):
        try:
            self.send_presence_subscription(pto=jid)
            return 1
        except IqError:
            raise Exception("Unable to add user to rooster")
            sys.exit(1)
        except IqTimeout:
            raise Exception("Server not responding") 

    def send_msg(self, recipient, body):
        self.sendNotification(recipient, 'Writing a message', 'composing')
        time.sleep(5)
        self.send_message(mto=recipient,mbody=body,mtype="chat")
    
    def send_msg_room(self, room, body):
        self.send_message(mto=room, mbody=body, mtype='groupchat')
    
    def join_create_room(self, room, nickname):
        try:
            self.plugin['xep_0045'].joinMUC(room, nickname)
            return 1
        except IqError as e:
            raise Exception("Unable to create room", e)
        except IqTimeout:
            raise Exception("Server not responding")


    def deleteUser(self, username):
        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = username
        itemXML = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        delete.append(itemXML)
        try:
            delete.send(now=True)
            print("Account deleted succesfuly", x)
        except IqError as e:
            raise Exception("Unable to delete username", e)
            sys.exit(1)
        except IqTimeout:
            raise Exception("Server not responding") 

    def receive(self, message):
        if len(message['body']) > 3000:
            print("You have received and image go check it out")
            received = message['body'].encode('utf-8')
            received = base64.decodebytes(received)
            with open("imageToSave.png", "wb") as fh:
                fh.write(received)
        else:
            #print("XMPP Message: %s" % message['body'])
            from_account = "%s@%s" % (message['from'].user, message['from'].domain)
            console.print(from_account, message['body'])
            #print("%s received message from %s" % (self.instance_name, from_account))

    
        
        #received falta que cuando alguien envia un 'active' responder que yo estoy active con un send notifcation type = active
            


#clientxmpp = Client('mafprueba@redes2020.xyz', 'mafer1234', 'redes2020.xyz')
#clientxmpp.listUsers()
#clientxmpp.send_file('fran@redes2020.xyz', 'prueba.jpg')

#clientxmpp.deleteUser('test1@redes2020.xyz')
