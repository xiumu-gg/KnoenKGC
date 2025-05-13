# 我有一个知识图谱中的关系，他在freebase上的标签为/government/politician/government_positions_held./government/government_position_held/jurisdiction_of_office，你可以帮我把这个关系表述为类似 :hasWife 这种简单的形式吗，请以{"result":"hasWife"}的形式进行输出


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
    if match:
        return match.group(1)
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
    data = [
        {
            "freebase": "_hypernym",
            "id": 0
        },
        {
            "freebase": "_derivationally_related_form",
            "id": 1
        },
        {
            "freebase": "_instance_hypernym",
            "id": 2
        },
        {
            "freebase": "_also_see",
            "id": 3
        },
        {
            "freebase": "_member_meronym",
            "id": 4
        },
        {
            "freebase": "_synset_domain_topic_of",
            "id": 5
        },
        {
            "freebase": "_has_part",
            "id": 6
        },
        {
            "freebase": "_member_of_domain_usage",
            "id": 7
        },
        {
            "freebase": "_member_of_domain_region",
            "id": 8
        },
        {
            "freebase": "_verb_group",
            "id": 9
        },
        {
            "freebase": "_similar_to",
            "id": 10
        }
    ]

    # 每十个一组调用algorithm函数
    res = []
    error = []
    aaaa = 0
    for item in data:
        if "label" in item:
            continue
        group = item["freebase"]
        json_string = '[{"result":"hasWife"}]'
        messages = "我有一个知识图谱中的关系，他在freebase上的标签为" + group + "，你可以帮我把这个关系表述为类似 :hasWife 这种简单的形式吗，请严格按照" + json.dumps(json_string).strip('"') + "的形式进行输出，不要输出其他无关的内容。"
        llm_result = algorithm(messages)

        ans = remove_think_part(llm_result) # 去掉 think
        json_result = extract_json_from_text(ans)
        print(json_result)
        if json_result == None:
            print("Error")
            print(item['id'])
            print(ans)
            error.append(group)
            aaaa = aaaa + 1
        else:
            item["label"] = json_result[0]["result"]
            write_to_file(data, "relation.json")
        # print(data)
    print(error)
    print(aaaa)



# 假设你的数据存储在entity.json文件中
process_entities('data/relation.json')
