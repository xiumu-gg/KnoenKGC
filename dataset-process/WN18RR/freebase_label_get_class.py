from ollama import chat
import json
import re


# 我每次会按照[{"entity":"entity name1"},{"entity":"entity name1"}]的格式输入十个实体名称，你能帮我生成他们对应的实体类型也就是class吗，请按照格式{"entity":"entity name1", "class":"class name"}的格式进行输出，并且不要输出其他无关的内容。

# [
#     {"entity":"Dominican Republic"},
#     {"entity":"republic"},
#     {"entity":"Mighty Morphin Power Rangers"},
#     {"entity":"Wendee Lee"},
#     {"entity":"drama film"},
#     {"entity":"American History X"},
#     {"entity":"Michelle Rodriguez"},
#     {"entity":"Naveen Andrews"},
#     {"entity":"Australia men's national soccer team"},
#     {"entity":"midfielder"}
# ]

def extract_json_from_text(text):
    """
    从文本中提取JSON格式的部分
    """
    # 使用正则表达式匹配JSON格式的字符串
    json_pattern = r'\[\s*({.*?})\s*\]'
    match = re.search(json_pattern, text, re.DOTALL)
    if match:
        # 提取匹配到的JSON字符串
        json_str = match.group(0)
        try:
            # 将JSON字符串转换为Python对象
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    return None

def algorithm(message):
    messages = [
        {'role': 'user', 'content': message},
    ]
    result = chat('deepseek-r1:32b', messages=messages)
    return result['message']['content']


def write_to_file(data, file_path):
    """
    将数据写入指定的JSON文件中
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Data has been written to {file_path}")

def remove_think_part(text):
    # 找到<think>的起始位置
    start = text.find("<think>")
    # 如果没有<think>，直接返回原始文本
    if start == -1:
        return text
    # 找到</think>的结束位置
    end = text.find("</think>")
    # 如果没有</think>，返回原始文本
    if end == -1:
        return text
    # 去掉<think>部分
    return text[:start] + text[end + len("</think>"):]

def error_information(id, llm_result, unthink):
    result = ""
    id_ = str(id)
    result = id_ + "\n\n"
    result = result + llm_result + "\n\n" + unthink + "\n\n\n"
    return result

def process_entities(file_path):
    # 打开并读取JSON文件
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 提取"label"字段并转换为所需的格式
    entities = [{"entity": item["freebase_id"] + ', ' + item["label"]} for item in data]
    # 每十个一组调用algorithm函数
    group_size = 10
    res = []
    process = ""

    entities = entities[20000:30000]

    for i in range(0, len(entities), group_size):
        if len(entities) > i + group_size:
            group = entities[i:i + group_size]
            entity_inf = json.dumps(group, ensure_ascii=False)
            json_string = '[{"entity":"entity name1, entity description1"},{"entity":"entity name1, entity description2"}]'
            json_string2 = '[{"entity":"entity name1", "class":"class name"},{"entity":"entity name1", "class":"class name"}]'
            messages = "我每次会按照" + json.dumps(json_string).strip('"') + "的格式输入十个实体名称及其描述，你能帮我生成他们对应的本体系统中的实体类型也就是class吗，请按照格式" + json_string2 + "的格式进行输出，并且不要输出其他无关的内容。" + "\n" + entity_inf
            print(messages)
            print(i)
            llm_result = algorithm(messages)
        else:
            group = entities[i:len(entities)]
            entity_inf = json.dumps(group, ensure_ascii=False)
            json_string = '[{"entity":"entity name1, entity description1"},{"entity":"entity name1, entity description2"}]'
            json_string2 = '[{"entity":"entity name1", "class":"class name"},{"entity":"entity name1", "class":"class name"}]'
            messages = "我每次会按照" + json.dumps(json_string).strip('"') + "的格式输入十个实体名称及其描述，你能帮我生成他们对应的本体系统中的实体类型也就是class吗，请按照格式" + json_string2 + "的格式进行输出，并且不要输出其他无关的内容。" + "\n" + entity_inf
            llm_result = algorithm(messages)
        ans = remove_think_part(llm_result)
        json_result = extract_json_from_text(ans)
        if json_result == None:
            print("Error")
            process = error_information(i, llm_result, ans)
            with open("error_information.txt", "a", encoding="utf-8") as file:
                file.write(process)
        else:
            res = res + json_result
        print(i)
        if i % 100 == 0:
            write_to_file(res, "class_result3.json")

def process_results(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open("class_result1.json", 'r', encoding='utf-8') as file:
        data1 = json.load(file)
    
    with open("class_result2.json", 'r', encoding='utf-8') as file:
        data2 = json.load(file)
    
    with open("class_result3.json", 'r', encoding='utf-8') as file:
        data3 = json.load(file)

    with open("class_result4.json", 'r', encoding='utf-8') as file:
        data4 = json.load(file)

    resss = [{} for _ in range(len(data))]
    for i in range(len(data)):
        resss[i] = data[i]


    # print(data4[1])
    for i in range(len(data)):
        if i== len(data1):
            break
        print(len(data1))
        cha = data1[i]["class"][0]
        if (resss[i]["freebase_id"] == data1[i]["entity"]) and (65 <= ord(cha) <= 90 or 97 <= ord(cha) <= 122):
            resss[i]['classname'] = data1[i]["class"]
        else:
            resss[i]['classname'] = ""
        
    for i in range(len(data)):
        if i== len(data2):
            break
        cha = data2[i]["class"][0]
        if (resss[i+10000]["freebase_id"] == data2[i]["entity"]) and (65 <= ord(cha) <= 90 or 97 <= ord(cha) <= 122):
            resss[i+10000]['classname'] = data2[i]["class"]
        else:
            resss[i+10000]['classname'] = ""

    for i in range(len(data)):
        if i== len(data3):
            break
        cha = data3[i]["class"][0]
        if (resss[i+20000]["freebase_id"] == data3[i]["entity"]) and (65 <= ord(cha) <= 90 or 97 <= ord(cha) <= 122):
            resss[i+20000]['classname'] = data3[i]["class"]
        else:
            resss[i+20000]['classname'] = ""

    for i in range(len(data)):
        if i== len(data4):
            break
        cha = data4[i]["class"][0]
        if (resss[i+30000]["freebase_id"] == data4[i]["entity"]) and (65 <= ord(cha) <= 90 or 97 <= ord(cha) <= 122):
            resss[i+30000]['classname'] = data4[i]["class"]
        else:
            resss[i+30000]['classname'] = ""
    
    write_to_file(resss, "entity.json")






def process_mistakes(file_path):
    # 打开并读取JSON文件
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 提取"label"字段并转换为所需的格式
    entities = [{"entity": item["freebase_id"] + ', ' + item["label"]} for item in data]
    # 每十个一组调用algorithm函数
    group_size = 10
    res = []
    process = ""

    for i in range(0, len(entities), group_size):
        if data[i]["classname"] != "":
            continue
        if len(entities) > i + group_size:
            group = entities[i:i + group_size]
            entity_inf = json.dumps(group, ensure_ascii=False)
            json_string = '[{"entity":"entity name1, entity description1"},{"entity":"entity name1, entity description2"}]'
            json_string2 = '[{"entity":"entity name1", "class":"class name"},{"entity":"entity name1", "class":"class name"}]'
            messages = "我每次会按照" + json.dumps(json_string).strip('"') + "的格式输入十个实体名称及其描述，你能帮我生成他们对应的本体系统中的实体类型也就是class吗，请按照格式" + json_string2 + "的格式进行输出，并且不要输出其他无关的内容。" + "\n" + entity_inf
            print("start\n")
            print(i)
            llm_result = algorithm(messages)
        else:
            group = entities[i:len(entities)]
            entity_inf = json.dumps(group, ensure_ascii=False)
            json_string = '[{"entity":"entity name1, entity description1"},{"entity":"entity name1, entity description2"}]'
            json_string2 = '[{"entity":"entity name1", "class":"class name"},{"entity":"entity name1", "class":"class name"}]'
            messages = "我每次会按照" + json.dumps(json_string).strip('"') + "的格式输入十个实体名称及其描述，你能帮我生成他们对应的本体系统中的实体类型也就是class吗，请按照格式" + json_string2 + "的格式进行输出，并且不要输出其他无关的内容。" + "\n" + entity_inf
            llm_result = algorithm(messages)
        ans = remove_think_part(llm_result)
        json_result = extract_json_from_text(ans)
        if (json_result == None) or not (65 <= ord(json_result[0]["class"][0]) <= 90 or 97 <= ord(json_result[0]["class"][0]) <= 122):
            print("Error")
            print(json_result)
            print(i)

        else:
            for j in range(group_size):
                if i+j == len(data):
                    break
                data[i+j]["classname"] = json_result[j]["class"]
            write_to_file(data, file_path)





    
# 假设你的数据存储在entity.json文件中
# process_entities('class_result.json')
aaa = True
while(aaa):
    aaa = False
    process_mistakes("entity.json")
    with open('class_result.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for item in data:
        if item["classname"] == "":
            aaa = True
            break

