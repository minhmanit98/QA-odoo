{'name': 'QA Application',
 'description': 'Question And Answer',
 'author': 'Nguyen Minh Man',
 'depends': [
        'base',
        'mail',
    ],
 'data': [
    'views/utc2_menu.xml',
    'views/qa_view.xml',
    'views/utc2_qa_category_view.xml',
    'security/utc2_security.xml',
    'security/ir.model.access.csv',
 ],

 'application': True,
 'installable': True,
 }
