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
        'message': 'Select toppings',
        'name': 'choice',
        'choices': [ 
            Separator('= The Meats ='),
            {
                'name': 'Ham'
            },
            {
                'name': 'Ground Meat'
            },
            {
                'name': 'Bacon'
            },
            
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    }
]

answers = prompt(questions, style=custom_style_2)
pprint(answers)