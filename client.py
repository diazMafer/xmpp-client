import xmpp, sys
usuario = 'test1@redes2020.xyz'
password = 'mafer1234'
jid = xmpp.JID(usuario)
cli = xmpp.Client(jid.getDomain(), debug=[])
cli.connect()

if xmpp.features.register(cli,jid.getDomain(),{'username':jid.getNode(),'password':password}):
    sys.stderr.write('Success\n')
    sys.exit(0)
else:
    sys.stderr.write('Error\n')
    sys.exit(1)
