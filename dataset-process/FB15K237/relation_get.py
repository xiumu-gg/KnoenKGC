import json
import re
from ollama import chat















def extract_json_from_text(text):
    """
    从文本中提取JSON格式的部分
    """
    # 使用正则表达式匹配JSON格式的字符串
    json_pattern = r'\[\s*({.*?})\s*\]'
    match = re.search(json_pattern, text, re.DOTALL)
    
    return match

def algorithm(message):
    messages = [
        {'role': 'user', 'content': message},
    ]
    result = chat('deepseek-r1:70b', messages=messages)
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


def get_str(data, id):
    res = ""
    for item in data:
        if item['id'] == id:
            continue
        res = res + item['label'] + '\t'
    return res


def process_com(data, strr):
    json_string = '["R1", "R2", "R3"]'
    messages = "在知识图谱本体框架中组合关系是指，如果A和B之间存在关系R1，B和C之间存在关系R2，且A和C之间存在关系R3，则关系R3等于关系R1和关系R2的组合，其中关系R3可以是R1和R2的任意一个，也可以是一个新的关系。当前关系R1为" + data + "请帮我从下面的关系集中找到关系B和关系C组成组合关系，并且严格按照" + json.dumps(json_string).strip('"') + "的格式进行输出，不要输出任何其他东西。\n下面是你需要分析的关系集：\n" + strr
    llm_result = algorithm(messages)

    ans = remove_think_part(llm_result) # 去掉 think
    return ans

def process_equ(data, strr):
    json_string = '["relationname1", "relationname2",]'
    messages = "在知识图谱本体框架中等价关系是指，如果A和B之间存在关系R1，A和B之间存在关系R2，则R1和R2为等价关系。请帮我分析下面哪些关系和" + data + "是等价关系，并且严格按照" + json.dumps(json_string).strip('"') + "的格式进行输出，不要输出任何其他东西。\n下面是你需要分析的关系：\n" + strr
    llm_result = algorithm(messages)

    ans = remove_think_part(llm_result) # 去掉 think
    return ans


def process_dis(data, strr):
    json_string = '["relationname1", "relationname2",]'
    messages = "在知识图谱本体框架中互斥关系是指，如果A和B之间存在关系R1，A和B之间存在一定不存在关系R2，并且R1和R2大概率为反义词，则R1和R2为互斥关系。请帮我分析下面哪些关系和" + data + "是互斥关系，并且严格按照" + json.dumps(json_string).strip('"') + "的格式进行输出，不要输出任何其他东西。\n下面是你需要分析的关系：\n" + strr
    llm_result = algorithm(messages)

    ans = remove_think_part(llm_result) # 去掉 think
    return ans







def write_to_file(data, file_path):
    """
    将数据写入指定的JSON文件中
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Data has been written to {file_path}")

file_ = 'data/relation.json'
with open(file_, 'r', encoding='utf-8') as file:
    data = json.load(file)


def parse_data(data_str):
    # 尝试使用json.loads()函数将字符串转换为Python列表
    try:
        data_list = json.loads(data_str)
        return data_list
    except json.JSONDecodeError:
        # 如果解析失败，打印错误信息并返回None
        print(f"Failed to parse data: {data_str}")
        return None

def process_list(data):
    cleaned_data_str = data.strip()

    # 分割字符串以获取所有数组字符串
    array_strs = cleaned_data_str.split('\n')

    # 存储解析成功的数据
    all_data = []

    # 遍历所有数组字符串，尝试解析每个数据项
    for array_str in array_strs:
        parsed = parse_data(array_str)
        if parsed is not None:
            all_data.extend(parsed)  # 将解析成功的数组元素添加到大数组中
        else:
            return None

    # 输出解析成功的大数组
    return all_data

ans = 0
for item in data:
    if type(item["equiralence"]) == list:
        continue
    strr = get_str(data, item['id'])
    res = process_equ(item["label"], strr)
    cleaned_data_str = res.strip()
    try:
        data_list = json.loads(cleaned_data_str)
        item["equiralence"] = data_list
        print(item['id'])
        write_to_file(data, file_)
    except json.JSONDecodeError:
        # 如果解析失败，打印错误信息并返回None
        print(f"Failed to parse data: {cleaned_data_str}")
        ans = ans + 1
print(ans)

for item in data:
    if type(item["disjointness"]) == list:
        continue
    strr = get_str(data, item['id'])
    res = process_dis(item["label"], strr)
    cleaned_data_str = res.strip()
    try:
        data_list = json.loads(cleaned_data_str)
        item["disjointness"] = data_list
        print(item['id'])
        write_to_file(data, file_)
    except json.JSONDecodeError:
        # 如果解析失败，打印错误信息并返回None
        print(f"Failed to parse data: {cleaned_data_str}")
        ans = ans + 1
print(ans)

for item in data:
    if type(item["composition"]) == list:
        continue
    strr = get_str(data, item['id'])
    res = process_com(item["label"], strr)
    cleaned_data_str = res.strip()
    data_list = process_list(cleaned_data_str)
    if data_list != None:
        item["composition"] = data_list
        print(item['id'])
    else:
        ans = ans + 1
    write_to_file(data, file_)
print(ans)
