{
    'name': 'Qualification',
    'version': '0.0.0900',
    'author':'Lucas Chagas Lima do Carmo',
    'category': 'Technical',
    'summary': 'Product, Supplier and Equipment Qualification',
    'description': """Module for creating a Qualification Process for products, equipment and suppliers""",
    'depends': ['mail','product','maintenance'],
    'sequence': 1,
    'data': [
        'views/qualification_process_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
