import urllib.request
from html_table_parser import HTMLTableParser
from pprint import pprint

def url_get_contents(url):
    """ Opens a website and read its binary contents (HTTP Response Body) """
    req = urllib.request.Request(url=url)
    f = urllib.request.urlopen(req)
    return f.read()

def request_diem(msv):
    request = 'http://xemdiem.utc2.edu.vn/svxemdiem.aspx?ID='+msv+'&m_lopID=C%C3%B4ng%20ngh%E1%BB%87%20th%C3%B4ng%20tin%20%20K57&m_lopID_ID=4363&istinchi=1'
    xhtml = url_get_contents(request).decode('utf-8')
    p = HTMLTableParser()
    p.feed(xhtml)
    csvData = p.tables
    data_info = csvData[2]
    # return data_info[3][0][5:len(data_info[3][0])]
    return csvData[2]


def xuly(diem):
    diem_clean = []
    for mon in range(1,len(diem)):
        if len(diem[mon]) == 5:
            diem_clean.append(diem[mon])
    
    return diem_clean
            

# xuly(request_diem('5751071024'))
pprint(len(request_diem('555101A010')))