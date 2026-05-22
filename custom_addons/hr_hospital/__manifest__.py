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

        'data/doctor_category_data.xml',
        'data/disease_data.xml',
        'views/hr_hospital_patient_views.xml',
        'wizards/visit_report_wizard_views.xml',
        'wizards/mass_reassign_doctor_wizard.xml',
        'wizards/server_actions.xml',
        'views/menu.xml',
    ],

    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,

    'images': [
        'static/description/icon.png'
    ],
}