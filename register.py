import xmpp, sys

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


