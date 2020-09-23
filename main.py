from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json, Separator
from pprint import pprint
from examples import custom_style_2
import clientmethods
from rich.console import Console
from rich.table import Table
from rich.highlighter import RegexHighlighter
from rich.theme import Theme
from rich.measure import Measurement
from rich import box
from rich.text import Text


class EmailHighlighter(RegexHighlighter):
    """Apply style to anything that looks like an email."""

    base_style = "example."
    highlights = [r"(?P<email>[\w-]+@([\w-]+\.)+[\w-]+)"]


theme = Theme({"example.email": "bold magenta"})
console = Console(highlighter=EmailHighlighter(), theme=theme)


def registerAccount():
    questions = [
        {
            'type': 'input',
            'message': 'Enter your username',
            'name': 'username'

        },
        {
            'type': 'password',
            'message': 'Enter your git password',
            'name': 'password'
        }

    ]
    answers = prompt(questions, style=custom_style_2)
    x = clientmethods.register(answers['username'], answers['password'])
    if (x == 1):
        console.print(":heavy_check_mark:" + " Account created succesfully")
    else:
        console.print("Fail")

def login():
    questions = [
        {
            'type': 'input',
            'message': 'Enter your jid',
            'name': 'username'

        },
        {
            'type': 'password',
            'message': 'Enter your password',
            'name': 'password'
        }

    ]
    answers = prompt(questions, style=custom_style_2)
    clientxmpp = clientmethods.Client(answers['username'], answers['password'], 'redes2020.xyz')
    return clientxmpp

def logout(client):
    questions = [
        {
            'type': 'confirm',
            'message': 'Do you want to logout?',
            'name': 'logout',
            'default': True,
        }
    ]
    answers = prompt(questions, style=custom_style_2)
    if answers['logout']:
        client.logout()
        console.print(":waving_hand:" + "You have succesfully sign out from your account")
    else:
        return

def deleteUserAccount(client):
    questions = [
        {
            'type': 'input',
            'message': 'Enter jid to delete',
            'name': 'username'

        },
        {
            'type': 'confirm',
            'message': 'Are you sure you want to delete this user?',
            'name': 'delete'
        }

    ]
    answers = prompt(questions, style=custom_style_2)
    if answers['delete']:
        client.deleteUser(answers['username'])
        console.print(":heavy_check_mark:" + "Account deleted")
    else:
        return



def getContacts(client):
    data = client.listFriends()
    table = Table(show_footer=False)
    table.add_column("Name", no_wrap=True)
    table.add_column("JID", no_wrap=True)
    table.add_column("Subscription", no_wrap=True)
    table.add_column("Status", no_wrap=True)
    table.add_column("Extra", no_wrap=True)
    table.title = (
    "[not italic]:girl_light_skin_tone: Users In Rooster [not italic]:boy_light_skin_tone:")
    for row in data:
        table.add_row(*row)

    table.columns[4].header_style = "bold red"
    table.columns[3].header_style = "bold green"
    table.columns[2].header_style = "bold blue"
    table.columns[1].header_style = "red"
    table.columns[0].header_style = "cyan"
    table.row_styles = ["none", "dim"]
    table.border_style = "bright_yellow"
    for x in [
        box.SQUARE,
        box.MINIMAL,
        box.SIMPLE,
        box.SIMPLE_HEAD,
    ]:
        table.box = x
    console.print(table, justify="left")

def getUsers(client):
    data = client.listUsers()
    table = Table(show_footer=False)
    table.add_column("Email", no_wrap=True)
    table.add_column("JID", no_wrap=True)
    table.add_column("Username", no_wrap=True)
    table.add_column("Name", no_wrap=True)
    table.title = (
    "[not italic]:girl_light_skin_tone: Users In Server [not italic]:boy_light_skin_tone:")
    for row in data:
        table.add_row(*row)

    table.columns[3].header_style = "bold red"
    table.columns[2].header_style = "bold green"
    table.columns[1].header_style = "bold blue"
    table.columns[0].header_style = "cyan"
    table.row_styles = ["none", "dim"]
    table.border_style = "bright_yellow"
    for x in [
        box.SQUARE,
        box.MINIMAL,
        box.SIMPLE,
        box.SIMPLE_HEAD,
    ]:
        table.box = x
    console.print(table, justify="left")

def addToRoster(client):
    questions = [
        {
            'type': 'input',
            'message': 'Enter jid to add to Rooster',
            'name': 'username'

        },
        {
            'type': 'input',
            'message': 'Enter Nam or Nickname',
            'name': 'name'

        }

    ]
    answers = prompt(questions, style=custom_style_2)
    res = client.addRoster(answers['username'], answers['name'])
    if res == 1:
        console.print(":heavy_check_mark:" + "User added to Roster")
    else:
        return

def getInfoUser(client):
    questions = [
        {
            'type': 'input',
            'message': 'Enter username to get info',
            'name': 'username'

        }

    ]
    answers = prompt(questions, style=custom_style_2)
    data = client.getUserInfo(answers['username'])
    table = Table(show_footer=False)
    table.add_column("Email", no_wrap=True)
    table.add_column("JID", no_wrap=True)
    table.add_column("Username", no_wrap=True)
    table.add_column("Name", no_wrap=True)
    table.title = (
    "[not italic]:girl_light_skin_tone: Username Information [not italic]:boy_light_skin_tone:")
    for row in data:
        table.add_row(*row)

    table.columns[3].header_style = "bold red"
    table.columns[2].header_style = "bold green"
    table.columns[1].header_style = "bold blue"
    table.columns[0].header_style = "cyan"
    table.row_styles = ["none", "dim"]
    table.border_style = "bright_yellow"
    for x in [
        box.SQUARE,
        box.MINIMAL,
        box.SIMPLE,
        box.SIMPLE_HEAD,
    ]:
        table.box = x
    console.print(table, justify="left")

def sendMes(client):
    questions = [
        {
            'type': 'input',
            'message': 'Enter jid to send message to',
            'name': 'username'

        },
        {
            'type': 'input',
            'message': 'Enter message to send',
            'name': 'msg'

        }
    ]
    answers = prompt(questions, style=custom_style_2)
    client.send_msg(answers['username'], answers['msg'])
    console.print(answers['username'], ': ', answers['msg'])

def joinRoom(client):
    questions = [
        {
            'type': 'input',
            'message': 'Enter room',
            'name': 'room'

        },
        {
            'type': 'input',
            'message': 'Enter room alias',
            'name': 'alias'

        }
    ]

    incorrect = True
    while incorrect:
        answers = prompt(questions, style=custom_style_2)
        if ('conference' in answers['room']):
            res = client.join_create_room(answers['room'], answers['alias'])
            if (res == 1):
                console.print(":heavy_check_mark:" + "You have join to room " + answers['room'])
                incorrect = False
            else:
                print("fail")
        else:
            console.print(":warning:" + "Room name has to be something like:" + "roomname@conference.redes2020.xyz")

def createRoom(client):
    questions = [
        {
            'type': 'input',
            'message': 'Enter room',
            'name': 'room'

        },
        {
            'type': 'input',
            'message': 'Enter room alias',
            'name': 'alias'

        }
    ]

    incorrect = True
    while incorrect:
        answers = prompt(questions, style=custom_style_2)
        if ('conference' in answers['room']):
            res = client.join_create_room(answers['room'], answers['alias'])
            if (res == 1):
                console.print(":heavy_check_mark:" + "You have join to room " + answers['room'])
                incorrect = False
            else:
                print("fail")
        else:
            console.print(":warning:" + "Room name has to be something like:" + "roomname@conference.redes2020.xyz")

def sendRoomMesg(client):
    questions = [
        {
            'type': 'input',
            'message': 'Enter room to send message to',
            'name': 'room'

        },
        {
            'type': 'input',
            'message': 'Enter message to send',
            'name': 'msg'

        }
    ]
    incorrect = True
    while incorrect:
        answers = prompt(questions, style=custom_style_2)
        if ('conference' in answers['room']):
            client.send_msg_room(answers['room'], answers['msg'])
            console.print(answers['room'], ': ', answers['msg'])
            incorrect = False
        else:
            console.print(":warning:" + "Room name has to be something like:" + "roomname@conference.redes2020.xyz")

def sendFile(client):
    questions = [
        {
            'type': 'input',
            'message': 'Enter jid to send image to',
            'name': 'username'

        },
        {
            'type': 'input',
            'message': 'Enter image path',
            'name': 'file'

        }
    ]
    answers = prompt(questions, style=custom_style_2)
    client.send_filte(answers['username'], answers['file'])
    console.print(answers['username'], ': ', answers['file'])

def sendPresenceStanza(client):
    questions = [
    {
        'type': 'checkbox',
        'qmark': '😃',
        'message': 'Select Presence Stanza Options',
        'name': 'show',
        'choices': [ 
            Separator('= Show ='),
            {
                'name': 'away'
            },
            {
                'name': 'chat'
            },
            {
                'name': 'dnd'
            },
            {
                'name': 'xa'
            },
            
        ],
        'validate': lambda answer: 'You must choose at least one option on show.' \
            if len(answer) == 0 else True
        },
        {
            'type': 'input',
            'message': 'Enter status',
            'name': 'status'

        }
    ]

    answers = prompt(questions, style=custom_style_2)
    client.sendPresenceMessage(answers['status'], answers['show'][0], )
    
ans=True
client = None
while ans:
    print ("""
    1. Register Account
    2. LogIn
    3. Log Out
    4. Delete Account from Server
    5. Show Contacts
    6. Show All Users in Server
    7. Add Contact to Roster
    8. Get User Info
    9. Send Message
    10. Send Files
    11. Send Presence Message
    12. Join Room
    13. Send Room Message
    14. Send Presence Stanza
    15. Exit/Quit
    """)
    ans=input("What would you like to do? ") 
    if ans=="1": 
        registerAccount()
    elif ans=="2":
        client = login()
    elif ans=="3":
        logout(client)
    elif ans=="4":
        deleteUserAccount(client)
    elif ans=="5":
        getContacts(client)
    elif ans=="6":
        getUsers(client)
    elif ans=="7":
        addToRoster(client)
    elif ans=="8":
        getInfoUser(client)
    elif ans=="9":
        sendMes(client)
    elif ans=="10":
        sendFile(client)
    elif ans=="11":
        print("mandar mensajes de presencia")
    elif ans=="12":
        joinRoom(client)
    elif ans=="13":
        sendRoomMesg(client)
    elif ans=="14":
        sendPresenceStanza(client)
    elif ans=="15":
        exit()
    





