def parse_json(data):
    di={}
    dat=data[1:-1].strip()
    skobki=0
    arrcheck=0
    is_key=True
    tekkey=''
    tekznach=''
    for i in range(len(dat)) :
        if dat[i]=='{':
            skobki+=1
        elif dat[i]=='[':
            arrcheck+=1
        elif dat[i]==']':
            arrcheck-=1
        elif dat[i]=='}':
            skobki-=1
        elif dat[i]==':' and skobki==0:
            is_key=False
            continue
        elif dat[i]==',' and skobki==0 and arrcheck==0:
            di[tekkey.strip()]=tekznach.strip()
            tekkey=''
            tekznach=''
            is_key=True
            continue
        if is_key==True:
            tekkey+=dat[i]
        else:
            tekznach+=dat[i]
    if tekznach and tekkey:
        di[tekkey]=tekznach
    return di


def to_dict(dii):
    din={}
    for key, value in dii.items():
        try:
            din[key.strip()[1:-1]]=eval(value)
        except:
            din[key.strip()[1:-1]] = value
            continue
    return din


def to_string(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
        return content
def to_xml(json_data, count):
    xml_result = ""
    probels = "  " * count
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if isinstance(value, (dict, list)):
                xml_result += f"{probels}<{key}>\n{to_xml(value, count + 1)}{probels}</{key}>\n"
            else:
                xml_result += f"{probels}<{key}>{value}</{key}>\n"
    elif isinstance(json_data, list):
        for item in json_data:
            xml_result += f"{probels}<item>\n{to_xml(item, count + 1)}{probels}</item>\n"
    else:
        xml_result += f"{probels}{json_data}\n"

    return xml_result
data=to_string("schedule.json")
di=parse_json(data)

di=to_dict(di)
xml_output='''<root>\n''' + to_xml(di,0) +'''</root>'''

with open('xml_output.xml', 'w', encoding='utf-8') as file:
    file.write(xml_output)
