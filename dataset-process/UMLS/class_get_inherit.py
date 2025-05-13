# 我有一个知识图谱中的关系，他在freebase上的标签为/government/politician/government_positions_held./government/government_position_held/jurisdiction_of_office，你可以帮我把这个关系表述为类似 :hasWife 这种简单的形式吗，请以{"result":"hasWife"}的形式进行输出
# "在知识图谱本体框架中逆关系是指，如果A和B之间存在关系R1，B和A之间存在关系R2，则R1和R2为逆关系。请帮我分析下面哪些关系和" + relation + "是逆关系，并且严格按照" + json.dumps(json_string).strip('"') + "的格式进行输出，不要输出任何其他东西，如果下面没有的逆关系，请输出[]，不要输出其他[]之外的任何内容。\n下面是你需要分析的关系：\n" + strr
# "在知识图谱本体框架中对称关系是指，如果A和B之间存在关系R，B和A之间也存在关系R，则R为对称关系。请帮我分析关系" + relation + "是否为对称关系，如果是对称关系，请输出True，如果不是，请输出False，不要输出其他内容。"
# "在知识图谱本体框架中组合关系是指，如果A和B之间存在关系R1，B和C之间存在关系R2，且A和C之间存在关系R3，则关系R3等于关系R1和关系R2的组合，其中关系R3可以是R1和R2的任意一个，也可以是一个新的关系。请帮我分析下面哪些关系和" + relation + "是组合关系，并且严格按照" + json.dumps(json_string).strip('"') + "的格式进行输出，不要输出任何其他东西。\n下面是你需要分析的关系：\n" + strr
# "实体类别的继承关系是一种层次化的分类关系，用于描述实体类别之间的包含关系。如果实体类别 A 继承自实体类别 B，则表示 A 是 B 的一个子类别，即 A 是 B 的一种具体形式。请帮我分析类别" + entity + "继承下面的哪些类别，并且严格按照" + json.dumps(json_string).strip('"') + "的格式进行输出，不要输出任何其他东西。\n下面是你需要分析的类别：\n" + strr

from ollama import chat
import json
import re


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
        if item['classid'] == id:
            continue
        res = res + item['classname'] + '\t'
    return res

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
    lines = data.strip().split('\n')

    # 分割字符串以获取所有数组字符串
    lines = [line for line in lines if line.strip()]

    # 解析每一行为JSON数组
    result = []
    for line in lines:
        try:
            parsed_line = json.loads(line)
            result.append(parsed_line)
        except json.JSONDecodeError as e:
            print(f"Error parsing line: {line}. Error: {e}")
            return

    # 输出解析成功的大数组
    return result

def process_entities(file_path):
    # 打开并读取JSON文件
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 每十个一组调用algorithm函数
    res = []
    error = []
    aaaa = 0
    for item in data:
        entity = item["classname"]
        if "father" in item:
            continue
        json_string = '["class1", "class2", ]'
        print(item['classid'])
        strr1 = get_str(data, item['classid'])
        messages = "实体类别的继承关系可以表示为，如果实体类别 A 继承自实体类别 B，则 A 是 B 的一种具体形式。当前实体类别A为" + entity + "，请帮我分析" + entity + "继承于实体类别B，请帮我从下面的实体类别集合中选择出符合条件的实体类别B，并且严格按照" + json.dumps(json_string).strip('"') + "的格式进行输出，不要输出任何其他东西。\n下面是你需要分析的类别集合：\n" + strr1
        llm_result = algorithm(messages)
        ans = remove_think_part(llm_result) # 去掉 think
        print(ans)

        aa = parse_data(ans)
        if aa != None:
            item['father'] = aa

            write_to_file(data, file_path)




# 假设你的数据存储在entity.json文件中

aaa = True 
while(aaa):
    aaa = False
    process_entities('class.json')
    with open('class.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for item in data:
        if "father" not in item:
            aaa = True
            break