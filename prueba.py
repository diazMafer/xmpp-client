# -*- coding: utf-8 -*-
"""
* Checkbox question example
* run example by typing `python example/checkbox.py` in your console
"""
from pprint import pprint

from PyInquirer import prompt, Separator

from examples import custom_style_2


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
    }
]

answers = prompt(questions, style=custom_style_2)
pprint(answers)