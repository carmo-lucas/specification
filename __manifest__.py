{
    'name': 'Specification',
    'version': '0.0.0900',
    'author':'Lucas Chagas Lima do Carmo',
    'category': 'Technical',
    'summary': 'Product Technical Specifications',
    'description': "Module for registering products technical specifications",
    'depends': ['mail','product'],
    'sequence': 1,
    'data': [
        'security/ir.model.access.csv',
        'wizard/validate_spec_sheet_view.xml', # wizard tem que ser antes das views
        'views/specification_main.xml',
        'views/specification_parameter_form_view.xml',
        'views/specification_parameter_tree_view.xml',
        'views/specification_sheet_tree_view.xml',
        'views/specification_sheet_form_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
