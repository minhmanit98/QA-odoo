{'name': 'QA Application',
 'description': 'Question And Answer',
 'author': 'Nguyen Minh Man',
 'depends': [
     'base',
     'mail',
     'website_livechat',
     'website_forum',
     'backend_theme_v13',
     'auth_oauth',
     'google_calendar',
     'google_drive',

 ],
 'data': [
     'views/utc2_menu.xml',
     'views/qa_view.xml',
     'views/utc2_qa_category_view.xml',
     'views/res_config_settings_views.xml',
     'views/website_templates.xml',
     'views/assets.xml',
     'security/utc2_security.xml',
     'security/ir.model.access.csv',
     'data/im_livechat_data.xml',
     'data/ir_default_data.xml',
     'data/install_vn_data.xml',
     'data/website_data.xml',
 ],

 'application': True,
 'installable': True,
 }
