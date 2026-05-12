{
    'name': 'HR Hospital',
    'summary': 'Hospital management module',
    'author': 'Natika',
    'category': 'Customizations',
    'license': 'LGPL-3',
    'version': '19.0.1.0.0',

    'depends': ['base'],

    'external_dependencies': {
        'python': [],
    },

    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'data/disease_data.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'auto_install': False,

    'images': [
        'static/description/icon.png'
    ],
}