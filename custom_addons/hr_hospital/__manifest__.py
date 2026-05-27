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

    # SECURITY
    'security/ir.model.access.csv',

    # DATA
    'data/doctor_category_data.xml',
    'data/disease_data.xml',

    # ACTIONS
    'views/actions.xml',

    # VIEWS
    'views/patient_views.xml',
    'views/doctor_views.xml',
    'views/visit_views.xml',

    # WIZARDS
    'wizards/visit_report_wizard_views.xml',
    'wizards/server_actions.xml',
    'wizards/disease_report_wizard_views.xml',

    # MENU
    'views/menu.xml',

    'reports/doctor_report.xml',
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