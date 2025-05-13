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

    for i in range(0, len(entities), group_size):
        if len(entities) > i + group_size:
            group = entities[i:i + group_size]
            entity_inf = json.dumps(group, ensure_ascii=False)
            json_string = '[{"entity":"entity name1, entity description1"},{"entity":"entity name1, entity description2"}]'
            json_string2 = '[{"entity":"entity name1", "class":"class name"},{"entity":"entity name1", "class":"class name"}]'
            messages = "I will input ten entity names and their descriptions in the format of " + json.dumps(json_string).strip('"') + ". Could you help me generate their corresponding entity types, which are the classes in the ontology system? Please output in the format of " + json_string2 + ", and do not output any other irrelevant content." + "\n" + entity_inf
            print(messages)
            print(i)
            llm_result = algorithm(messages)
        else:
            group = entities[i:len(entities)]
            entity_inf = json.dumps(group, ensure_ascii=False)
            json_string = '[{"entity":"entity name1, entity description1"},{"entity":"entity name1, entity description2"}]'
            json_string2 = '[{"entity":"entity name1", "class":"class name"},{"entity":"entity name1", "class":"class name"}]'
            messages = "I will input ten entity names and their descriptions in the format of " + json.dumps(json_string).strip('"') + ". Could you help me generate their corresponding entity types, which are the classes in the ontology system? Please output in the format of " + json_string2 + ", and do not output any other irrelevant content." + "\n" + entity_inf
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
            write_to_file(res, "class_result.json")

def read_and_convert(file_path):
    # 初始化一个空数组来存储结果
    result = []
    
    # 打开文件并读取每一行
    with open(file_path, 'r') as file:
        for line in file:
            # 去除行尾的换行符并分割字符串
            parts = line.strip().split()
            
            # 检查是否正确分割出两部分
            if len(parts) == 2:
                keyword, id = parts
                # 创建字典并添加到结果数组
                result.append({"freebase": keyword, "id": int(id)})
            else:
                print(f"Skipping invalid line: {line.strip()}")
    
    # 返回结果数组
    return result

# 使用函数并打印结果
file_path = 'entity2id.txt'
converted_data = read_and_convert(file_path)
write_to_file(converted_data, "relation.json")

# 假设你的数据存储在entity.json文件中
# process_entities('entity.json')



