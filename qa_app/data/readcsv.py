import csv

data = []
with open('import_data_q.csv', encoding='utf8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if row[3] == 'admin':
            row[3]= 'qa_app.utc2_tags_0'
        elif row[3] == 'ban quản lý ký túc xá':
            row[3]= 'qa_app.utc2_tags_1'
        elif row[3] == 'ban thanh tra đào tạo':
            row[3]= 'qa_app.utc2_tags_2'
        elif row[3] == 'ban thông tin thư viện':
            row[3]= 'qa_app.utc2_tags_3'
        elif row[3] == 'ban công tác chính trị và sinh viên':
            row[3]= 'qa_app.utc2_tags_4'
        elif row[3] == 'ban khảo thí & đảm bảo chất lượng':
            row[3]= 'qa_app.utc2_tags_5'
        elif row[3] == 'ban đào tạo':
            row[3]= 'qa_app.utc2_tags_6'
        elif row[3] == 'ban thiết bị quản trị':
            row[3]= 'qa_app.utc2_tags_7'
        elif row[3] == 'ban tổ chức hành chính':
            row[3]= 'qa_app.utc2_tags_8'
        elif row[3] == 'trung tâm đào tạo thực hành':
            row[3]= 'qa_app.utc2_tags_9'
        elif row[3] == 'giảng viên':
            row[3]= 'qa_app.utc2_tags_10'
        elif row[3] == 'cố vấn':
            row[3]= 'qa_app.utc2_tags_11'
        elif row[3] == 'khác':
            row[3]= 'qa_app.utc2_tags_12'
        elif row[3] == 'null' or row[3] == 'null2':
            row[3]= ''
        data.append(row)
with open('employee_file2.csv', mode='w', encoding='utf8') as employee_file:
    employee_writer = csv.writer(employee_file, dialect='excel')
    for row in data:
        employee_writer.writerow(row)


