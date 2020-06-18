{'name': 'QLD Application',
 'description': 'Quản lý dự đoán điểm UTC2',
 'author': 'Nguyen Minh Man',
 'depends': [
     'base',
     'mail',
 ],
 'data': [
     'views/utc2_menu.xml',
     'views/utc2_qld_students_view.xml',
     'views/utc2_qld_scores_view.xml',
     'views/utc2_qld_subjects_view.xml',
     'views/utc2_sync_scores_views.xml',
     'views/utc2_qld_class_view.xml',
     'views/utc2_qld_group_view.xml',
     'views/utc2_qld_predict_view.xml',
     'views/utc2_qld_predict_scores_view.xml',
     'views/utc2_qld_predict_subjects_view.xml',
     'security/utc2_security.xml',
     'security/ir.model.access.csv',
     'data/ir_sequence_data.xml',
 ],

 'application': True,
 'installable': True,
 }
