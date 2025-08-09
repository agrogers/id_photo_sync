{
    'name': 'Image Sync Between User, Employee, Partner',
    'version': '18.0.1.0.0',
    "author": "Andrew Rogers",
    'category': 'Tools',
    'summary': 'Enables synching of images between Users, Employees, and Contacts',
    'depends': ['base','hr'],
    'installable': True,
    'application': False,
    'data': [
        'data/actions.xml',
        'views/res_users_views.xml',
    ],
    'description': '''
        This module adds a server action to sync the image attached to a User, Employee, or Partner.
        It will look for a photo in the user, partner and employee records and sync the first found image to all linked records
        that don't have an image.
    ''',
    'website': '',
    'contributors': [
        'Andrew Rogers <rogers.ag@gmail.com>',
    ],    
    "license": "LGPL-3"

}
