import json
import os

# 确保 data 目录存在
os.makedirs('data', exist_ok=True)
os.makedirs('data/FB15K237', exist_ok=True)

# 读取 data/entity.json 文件
entity_file = 'data/entity.json'
with open(entity_file, 'r', encoding='utf-8') as f:
    entity_data = json.load(f)

# 读取 data/FB15K237/entity.json 文件
fb_entity_file = 'data/FB15K237/entity.json'
with open(fb_entity_file, 'r', encoding='utf-8') as f:
    fb_entity_data = json.load(f)

# 创建 entity 到 class 的映射字典
entity_to_class = {item["entity"]: item["class"] for item in entity_data}

# 遍历 fb_entity_data 并更新 classname 字段
unmatched_labels = []
for item in fb_entity_data:
    label = item["label"]
    if label in entity_to_class:
        item["classname"] = entity_to_class[label]
    else:
        # 如果没有匹配的 entity，记录下来
        unmatched_labels.append(label)

fb_entity_file = 'data/FB15K237/entity1.json'
# 将更新后的数据存储回 data/FB15K237/entity.json 文件
with open(fb_entity_file, 'w', encoding='utf-8') as f:
    json.dump(fb_entity_data, f, indent=4, ensure_ascii=False)

# 输出没有匹配的数据
print("以下数据在 data/entity.json 中没有对应项：")
for label in unmatched_labels:
    print(label)