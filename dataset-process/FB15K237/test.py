import json
import re
from ollama import chat



def algorithm(message):
    messages = [
        {'role': 'user', 'content': message},
    ]
    result = chat('deepseek-r1:70b', messages=messages)
    return result['message']['content']

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


def process_com(data, strr):
    entity = data
    json_string = '["class1", "class2", ]'
    messages = "实体类别的继承关系可以表示为，如果实体类别 A 继承自实体类别 B，则 A 是 B 的一种具体形式。当前实体类别A为" + entity + "，请帮我分析" + entity + "继承于实体类别B，请帮我从下面的实体类别集合中选择出符合条件的实体类别B，并且严格按照" + json.dumps(json_string).strip('"') + "的格式进行输出，不要输出任何其他东西。\n下面是你需要分析的类别集合：\n" + strr
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

def get_str(data, id):
    res = ""
    for item in data:
        if item['classid'] == id:
            continue
        if item['classid'] == 500:
            return res
        res = res + item['classname'] + '\t'
    return res

def get_class_father(item, strr1, strr2, strr3, strr4):
    pass



file_ = 'data/class.json'
with open(file_, 'r', encoding='utf-8') as file:
    data = json.load(file)

ans = 0


# for item in data:
#     resss = item["father"]
#     data_list = process_list(resss)
#     if data_list != None:
#         item["father"] = data_list
#         print(item['classid'])
#         write_to_file(data, file_)
#     else:
#         ans = ans + 1
# print(ans)



for item in data:
    if type(item["father"]) == list:
        continue
    strr1 = get_str(data[:400], item['classid'])
    strr2 = get_str(data[400:800], item['classid'])
    strr3 = get_str(data[800:1200], item['classid'])
    strr4 = get_str(data[1200:], item['classid'])
    print("start {}".format(item["classid"]))
    resss = ""
    res = process_com(item["classname"], strr1)
    resss = resss + res
    res = process_com(item["classname"], strr2)
    resss = resss + res
    res = process_com(item["classname"], strr3)
    resss = resss + res
    res = process_com(item["classname"], strr4)
    resss = resss + res
    data_list = process_list(resss)
    if data_list != None:
        item["father"] = data_list
        print(item['classid'])
        write_to_file(data, file_)
    else:
        ans = ans + 1
print(ans)





