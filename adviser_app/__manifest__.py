{'name': 'Adviser Application',
 'description': 'Question And Answer',
 'author': 'Nguyen Minh Man',
 'depends': [
     'base',
     'qa_app',
     'qld_app'

 ],
 'data': [
     'views/utc2_menu.xml',
     'security/utc2_security.xml',
     'security/ir.model.access.csv',

 ],

 'application': True,
 'installable': True,
 }
