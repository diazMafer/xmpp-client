"""
Universidad del Valle de guatemala 
Maria Fernanda Lopez - 17160
Client xmpp
Clase base tomada de https://gist.github.com/deckerego/be1abbc079b206b793cf/revisions 
Los métodos en que se difiere fueron agregados en base a la documentos y los xp e iq 
a agregar con la clase sleekxmpp
"""
import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
import xmpp, sys
import base64
import time
import threading
import binascii
import easygui
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
        self.add_event_handler("presence_subscribe", self.add_to_roster_notifcation)
        self.add_event_handler("presence_unsubscribe", self.remove_to_roster_notifcation)
        self.add_event_handler("got_offline", self.user_isoffline)
        self.add_event_handler("got_online", self.user_isonline)

        self.received = set()
        self.contacts = []
        self.presences_received = threading.Event()
        
        self.register_plugin('xep_0077')
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0096') # Send file 
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

    def sendPresenceMessage(self, status, show):
        #conectar
        #ingresar a un room
        #actualizar manual 
        self.send_presence(pshow=show, pstatus=status)

    def start(self, event):
        self.send_presence(pshow='chat', pstatus='Disponible')
        roster = self.get_roster()
        for r in roster['roster']['items'].keys():
            self.contacts.append(r)
        for jid in self.contacts:
            #to everyone in rooster send i just log in as an active notification
            self.sendNotification(jid, 'Im ready to start messaging', 'active')
    
    # Trigger when someone got offline
    def user_isoffline(self, presence):        
        if presence['from'].bare != self.boundjid.bare:
            table = Table()
            table.add_column("Disconected User Notification", no_wrap=True)
            table.columns[0].header_style = "cyan"
            table.border_style = "yellow"
            msg = presence['from'].bare + " is offline"
            table.add_row(msg)

            console = Console()
            console.print(table, justify="center")
            print('\n')

    def add_to_roster_notifcation(self, presence):
        if presence['from'].bare != self.boundjid.bare:
            table = Table()
            table.add_column("Added to Roster Notification", no_wrap=True)
            table.columns[0].header_style = "cyan"
            table.border_style = "yellow"
            msg = presence['from'].bare + " added you to their roster"
            table.add_row(msg)

            console = Console()
            console.print(table, justify="center")
            print('\n')
    
    def remove_to_roster_notifcation(self, presence):
        if presence['from'].bare != self.boundjid.bare:
            table = Table()
            table.add_column("Remove from Roster Notification", no_wrap=True)
            table.columns[0].header_style = "cyan"
            table.border_style = "yellow"
            msg = presence['from'].bare + " removed you from their roster"
            table.add_row(msg)

            console = Console()
            console.print(table, justify="center")
            print('\n')

    # Trigger when someone got online
    def user_isonline(self, presence):
        if presence['from'].bare != self.boundjid.bare:
            table = Table()
            table.add_column("Conected User Notification", no_wrap=True)
            table.columns[0].header_style = "cyan"
            table.border_style = "yellow"
            msg = presence['from'].bare + " is online"
            table.add_row(msg)

            console = Console()
            console.print(table, justify="center")
            print('\n')
        
    #example code to iterate all roster including groups took from rooster_browser https://github.com/fritzy/SleekXMPP/blob/develop/examples/roster_browser.py
    def listFriends(self):
        try:
            self.get_roster()
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')


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
                temp.append(show)
                temp.append(status)
                
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
        if pres['show'] != "" and pres['from'].bare != self.boundjid.bare:
            table = Table()
            table.add_column("Change Status Notification", no_wrap=True)
            table.columns[0].header_style = "cyan"
            table.border_style = "yellow"
            msg = pres['from'].bare + " changed status to:  " + pres['show']
            table.add_row(msg)

            console = Console()
            console.print(table, justify="center")
            print('\n')
        

        self.received.add(pres['from'].bare)
        if len(self.received) >= len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

    def alertFriend(self):
        self.get_roster()
    
    #send chat notifications,examples of stanzas where took from https://xmpp.org/extensions/xep-0085.html
    def sendNotification(self, to, body, ntype):
        message = self.Message()
        message['to'] = to
        message['type'] = 'chat'
        if (ntype == 'active'):
            message['body'] = body
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
            data = []
            temp = []
            cont = 0
            for i in x.findall('.//{jabber:x:data}value'):
                cont += 1
                txt = ''
                if i.text != None:
                    txt = i.text

                temp.append(txt)
                #contador hasta 4 porque el servidor solo retorna 4 values field por usuario
                #email, jid, username y name
                if cont == 4:
                    cont = 0
                    data.append(temp)
                    temp = []

            return data
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
            data = []
            temp = []
            cont = 0
            print(x)
            for i in x.findall('.//{jabber:x:data}value'):
                cont += 1
                txt = ''
                if i.text != None:
                    txt = i.text

                temp.append(txt)
                #contador hasta 4 porque el servidor solo retorna 4 values field por usuario
                #email, jid, username y name
                if cont == 4:
                    cont = 0
                    data.append(temp)
                    temp = []

            return data
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
        try:
            self.send_message(mto=recipient,mbody=body,mtype="chat")
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')
    
    # method took from example of SleekXMPP https://github.com/fritzy/SleekXMPP/blob/develop/examples/muc.py
    def send_msg_room(self, room, body):
        try:
            self.send_message(mto=room, mbody=body, mtype='groupchat')
        except IqError as err:
            print('Error: %s' % err.iq['error']['condition'])
        except IqTimeout:
            print('Error: Request timed out')

    # Method to create a room using plugin xep0045
    # method took from example of SleekXMPP https://github.com/fritzy/SleekXMPP/blob/develop/examples/muc.py
    def create_room(self, room, nickname):
        try:
            self.plugin['xep_0045'].joinMUC(room, nickname, pstatus="Conferencia Creada", pfrom=self.boundjid.bare, wait=True)
            self.plugin['xep_0045'].setAffiliation(room, self.boundjid.bare, affiliation='owner')
            self.plugin['xep_0045'].configureRoom(room, ifrom=self.boundjid.bare)
            return 1
        except IqError as e:
            raise Exception("Unable to create room", e)
        except IqTimeout:
            raise Exception("Server not responding")

    
    # method took from example of SleekXMPP https://github.com/fritzy/SleekXMPP/blob/develop/examples/muc.py
    def join_create_room(self, room, nickname):
        try:
            self.plugin['xep_0045'].joinMUC(room, nickname)
            return 1
        except IqError as e:
            raise Exception("Unable to create room", e)
        except IqTimeout:
            raise Exception("Server not responding")


    def sendBytestreamStanza(self, filename, to):
        offer = self.Iq()
        offer['type'] = 'set'
        offer['id'] = 'offer1'
        offer['to'] = to
        siXML = ET.fromstring("<si xmlns='http://jabber.org/protocol/si'\
                                id='a0'\
                                mime-type='text/plain'\
                                profile='http://jabber.org/protocol/si/profile/file-transfer'>\
                                    <file xmlns='http://jabber.org/protocol/si/profile/file-transfer'\
          name='test.txt'\
          size='4066'/>\
              <feature xmlns='http://jabber.org/protocol/feature-neg'>\
                                    <x xmlns='jabber:x:data' type='form'>\
                                        <field var='stream-method' type='list-single'>\
                                        <option><value>http://jabber.org/protocol/bytestreams</value></option>\
                                        <option><value>http://jabber.org/protocol/ibb</value></option>\
                                        </field>\
                                    </x>\
                                    </feature>\
                                </si>")

        offer.append(siXML)
        try:
            offer.send()
        except IqError as e:
            raise Exception("Unable to delete username", e)
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
            self.disconnect()
            print("Account deleted succesfuly")
            print('\n')
        except IqError as e:
            raise Exception("Unable to delete username", e)
            sys.exit(1)
        except IqTimeout:
            raise Exception("Server not responding") 

    def receive(self, message):
        if len(message['body']) > 3000:
            print('\n')
            print("You have received and image go check it out")
            received = message['body'].encode('utf-8')
            received = base64.decodebytes(received)
            with open("imageToSave.png", "wb") as fh:
                fh.write(received)
        else:
            from_account = "%s@%s" % (message['from'].user, message['from'].domain)
            console.print(from_account, message['body'])