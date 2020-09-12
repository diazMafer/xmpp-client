import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
import xmpp, sys



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
        sys.stderr.write('Success\n')
        sys.exit(0)
    else:
        sys.stderr.write('Error\n')
        sys.exit(1)


class Client(sleekxmpp.ClientXMPP):
    def __init__(self, username, password, instance_name=None):
        jid = "%s/%s" % (username, instance_name) if instance_name else username
        super(Client, self).__init__(jid, password)

        self.instance_name = instance_name
        self.username = username
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.receive)
        self.add_event_handler("changed_subscription", self.alertFriend)
        
        self.register_plugin('xep_0077')
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0047', {
            'auto_accept': True
        })

        if self.connect():
            print("Opened XMPP Connection")
            self.process(block=False)

        else:
            raise Exception("Unable to connect to Redes Jabber server")

    def logout(self):
        print("Closing XMPP Connection")
        self.disconnect(wait=False)

    def start(self, event):
        self.send_presence(pshow='chat', pstatus='Disponible')
    
    #needs admin priviledges
    def listFriends(self):
        print(self.get_roster())

    def alertFriend(self):
        self.get_roster()

    def addRoster(self, jid, name):
        try:
            self.send_presence_subscription(pto=jid)
            print("User added to roster")
        except IqError:
            raise Exception("Unable to add user to rooster")
        except IqTimeout:
            raise Exception("Server not responding") 

    def send_msg(self, recipient, body):
        self.send_message(mto=recipient,mbody=body,mtype="chat")
    
    def send_msg_room(self, room, body):
        self.send_message(mto=room, mbody=body, mtype='groupchat')
    
    def join_create_room(self, room, name):
        self.plugin['xep_0045'].joinMUC(room, name, wait=True)

    def deleteUser(self, username):
        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = username
        itemXML = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        delete.append(itemXML)
        print(delete)
        try:
            delete.send(now=True)
            print("Account deleted succesfuly")
        except IqError as e:
            raise Exception("Unable to delete username", e)
        except IqTimeout:
            raise Exception("Server not responding") 

    def receive(self, message):
        print("XMPP Message: %s" % message)
        from_account = "%s@%s" % (message['from'].user, message['from'].domain)
        print("%s received message from %s" % (self.instance_name, from_account))

        if self.instance_name in message['body'].lower():
            print ("Caught test message: %s" % message)
            message.reply("%s was listening!" % self.instance_name).send()
        else:
            print ("Uncaught command from %s: %s" % (from_account, message['body']))

clientxmpp = Client('mafprueba@redes2020.xyz', 'mafer1234', 'redes2020.xyz')
clientxmpp.join_create_room('vacacio@conference.redes2020.xyz', 'prueba')
clientxmpp.send_msg_room('vacacio@conference.redes2020.xyz', 'prueba participacion')

#clientxmpp.deleteUser('test1@redes2020.xyz')
