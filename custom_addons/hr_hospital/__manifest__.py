{
    'name': 'HR Hospital',
    'version': '19.0.1.0.0',
    'summary': 'Hospital management module',
    'author': 'Natika',
    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'data/disease_data.xml',
    ],

    'demo': [
        'demo/demo_data.xml',
    ],

    'application': True,
}