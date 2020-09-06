import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout

#Clase base tomada de https://gist.github.com/deckerego/be1abbc079b206b793cf/revisions 
#Los métodos en que se difiere fueron agregados en base a la documentos y los xp e iq 
#a agregar con la clase sleekxmpp

class Client(sleekxmpp.ClientXMPP):
    def __init__(self, username, password, instance_name=None):
        jid = "%s/%s" % (username, instance_name) if instance_name else username
        super(Client, self).__init__(jid, password)

        self.instance_name = instance_name
        self.add_event_handler('session_start', self.start, threaded=False, disposable=True)
        self.add_event_handler('message', self.receive, threaded=True, disposable=False)

        if self.connect((instance_name, '5222')):
            print("Opened XMPP Connection")
            self.process(block=False)
        else:
            raise Exception("Unable to connect to Redes Jabber server")

    def logout(self):
        print("Closing XMPP Connection")
        self.disconnect(wait=False)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def send_msg(self, recipient, body):
        message = self.Message()
        message['to'] = recipient
        message['type'] = 'chat'
        message['body'] = body

        print("Sending message: %s" % message)
        message.send()

    def deleteUser(self, username):
        delete = self.Iq()
        delete['type'] = 'set'
        delete['from'] = username
        delete['register'] = ''
        delete['register']['unregistered_user'] = ''
        try:
            delete.send(now=True)
            print("Account deleted succesfuly")
        except IqError:
            raise Exception("Unable to delete username")
        except IqTimeout:
            raise Exception("Server not responding")

    def receive(self, message):
        if message['type'] in ('chat', 'normal'):
            print("XMPP Message: %s" % message)
            from_account = "%s@%s" % (message['from'].user, message['from'].domain)
            print("%s received message from %s" % (self.instance_name, from_account))

            if self.instance_name in message['body'].lower():
                print ("Caught test message: %s" % message)
                message.reply("%s was listening!" % self.instance_name).send()
            else:
                print ("Uncaught command from %s: %s" % (from_account, message['body']))

clientxmpp = Client('test1@redes2020.xyz', 'mafer1234', 'redes2020.xyz')
clientxmpp.start()
clientxmpp.logout()