{'name': 'QLD Application',
 'description': 'Quản lý điểm',
 'author': 'Nguyen Minh Man',
 'depends': [
     'base',
     'mail',
 ],
 'data': [
     'views/utc2_menu.xml',
     'views/utc2_qld_view.xml',
     'views/utc2_qld_scores_view.xml',
     'views/utc2_qld_subjects_view.xml',
     'wizard/utc2_sync_score_views.xml',
     'security/utc2_security.xml',
     'security/ir.model.access.csv',
 ],

 'application': True,
 'installable': True,
 }
