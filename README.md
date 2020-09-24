# xmpp-client


## Introduction
Client of XMPP using XMPP-Protocol on python. The Client connects to a server named redes2020.xyz. The client was developed for a college project of computational network.

## Functionalities
1. Register a user with a jid and password. This functionalitie was implemented with xmpppy.
2. Login to server with jid and password.
3. Logout from server.
4. Delete an account from server. You **MUST** be logged in for the server to accomplish task correctly.
5. Get All users from server. The server returns the email, jid, username and name for all users.
6. Get Contacts information. The server return jid username and status from all your roster.
7. Add user to contacts list. With de jid you can add someone to your Roster. When someone else is trying to add you to their Roster the client responds automatically with an accept to the request. 
8. Show a user information. With the username the server returns email, jid username and name if the username exists.
9. Send Message to a User. You can send a message to anyone by typing the jid and the message you want to send.
10. Create Room. You can create a room by entering the name of the room as 'nameroom@conference.redes2020.xyz' and the alias you want to have inside the room.
11. Join Room. You can enter to a room by entering the name of the room as 'nameroom@conference.redes2020.xyz' and the alias you want to have inside the room.
12. Send Message to a room. You can send a message to a room you haved join by entering the room and the message you want to send.
13. Presence Stanza. A presence stanza is send when you just logged in to show a status of available. Also you change your status by sendig a presence stanza.
14. Notifications:
     * You received a notification when someone of your roster logged in
     * You received a notification when someone of your roster logged out
     * You received a notification when someone added you to their roster
     * You received a notification when someone remove you from ther roster
     * You send an active chat notification when you just logged in
     * You send a composing chat notification when you are typing the message you want to send 
15. Send Files. You can send **ONLY** .png and .jpg files to another client that has the same configuration to received it.
16. Received Files. You can received .png and .jpg and them will be storage in a new file on the directory where you downloaded the project.
17. Received messages. You can received private and room messages.
  
## Requirements
Run the following commands to get the dependencies of the project.

- `pip install pyasn1==0.3.6` 

- `pip install pyasn1-modules==0.1.5` 

- `pip install sleekxmpp==1.3.3`  

- `pip install PyInquirer==1.0.3` 

- `pip install rich==6.1.2` 

- `pip install xmpppy==0.6.1` 


## Run the program 
The client is divided in two the file clientmethods.py is the one in charge to handle or request to server, each functionallity has its own method that implements the protocol as the documentation said. The file main.py is the one in charge to ask the user for information and print the output of the server responses in a user friendly way. 

To start executing the program after downloading dependencies run:

```sh
python main.py or python3 main.py
```

## Usage

When the main.py is already running a menu is going to be displayed with several options.

#### Register
Choose option 1 and enter the jid and the password for the new account

#### Login 
Choose option 2 and enter your jid and the password of your account

#### Logout
Choose option 3 to logout

#### Delete account
Choose option 4 and enter jid to be deleted

#### Show contacts
Choose option 5

#### Show all users in server
Choose option 6

#### Add Contact to Roster
Choose option 7

#### Get user info
Choose option 8 and enter the username which you want to see all info

#### Send Message
Choose option 9 and enter de jid and the message

#### Send Files - Limited functionality
Choose option 10 and enter jid to send file and enter the path of the file

#### Create Room
Choose option 11 and enter room name and your nickname 

#### Join Room
Choose option 12 and enter room name and your nickname

#### Send Room Message
Choose option 13 and enter room name and your message

#### Send Presence Stanza
Choose option 14, and choose new show status and enter message

#### Exit
Choose option 15


## Develop with
- 🛠 **Python 3.x** 
- 🚀 **SleekXMPP**  — Hot Reloading, Code Splitting, Optimized Build
- 💅 **Rich** — Styled Consoles
- 💖  **PyInquirer** — Styled Consoles

## Authors
* **María Fernanda López Díaz** - *Initial work* - [diazMafer](https://github.com/diazMafer)
