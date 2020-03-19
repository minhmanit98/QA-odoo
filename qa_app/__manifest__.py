{'name': 'QA Application',
 'description': 'Question And Answer',
 'author': 'Nguyen Minh Man',
 'depends': [
        'base',
        'mail',
        'website_livechat',
        'website_forum',
        'backend_theme_v13',
        'theme_nice_bootstrap',

    ],
 'data': [
    'views/utc2_menu.xml',
    'views/qa_view.xml',
    'views/utc2_qa_category_view.xml',
    'security/utc2_security.xml',
    'security/ir.model.access.csv',
     'data/im_livechat_data.xml',
 ],

 'application': True,
 'installable': True,
 }
