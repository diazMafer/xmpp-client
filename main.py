from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
from pprint import pprint
from examples import custom_style_2
import clientmethods
from rich.console import Console
from rich.table import Table
from rich.measure import Measurement
from rich import box
from rich.text import Text
from rich.console import Console

console = Console()


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


def getContacts(client):
    data = client.listFriends()
    print(data)
    table = Table(show_footer=False)
    table.add_column("Name", no_wrap=True)
    table.add_column("JID", no_wrap=True)
    table.add_column("Subscription", no_wrap=True)
    table.add_column("Status", no_wrap=True)
    table.add_column("Extra", no_wrap=True)
    table.title = (
    "[not italic]:popcorn:[/] Users In Rooster [not italic]:popcorn:[/]")
    for row in data:
        table.add_row(*row)

    console.print(table, justify="left")




login()

#registerAccount()