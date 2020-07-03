import json
json_list = []
res = self.env['document.page'].search([('id', '=', 1)])
ojb = '{ "MESSAGE":"'+res.name+'", "RESPONSE":"'+res.content[3:len(res.content)-8]+'"}'
print(ojb)
json = json.loads(ojb)
json_list.append(json)
print(json_list)
print(res.content[3:len(res.content)-8])