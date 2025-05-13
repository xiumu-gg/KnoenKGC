import json
import os

# 确保 data 目录存在
os.makedirs('data', exist_ok=True)

# 读取 data/entity.json 文件
entity_file = 'data/entity.json'
with open(entity_file, 'r', encoding='utf-8') as f:
    entity_data = json.load(f)

# 创建 classname 到 classid 的映射字典
classname_to_id = {}

# 初始化 classid 计数器
classid_counter = 0

# 遍历数据并为每个 classname 分配 classid
for item in entity_data:
    classname = item["classname"]
    if classname not in classname_to_id:
        classname_to_id[classname] = classid_counter
        classid_counter += 1
    item["classid"] = classname_to_id[classname]

# 将更新后的数据存储回 data/entity.json 文件
with open(entity_file, 'w', encoding='utf-8') as f:
    json.dump(entity_data, f, indent=4, ensure_ascii=False)

# 将 classname 与 classid 的对应关系存储到 data/class.json 文件
class_output_file = 'data/class.json'
class_data = [{"classname": cls, "classid": classid} for cls, classid in classname_to_id.items()]
with open(class_output_file, 'w', encoding='utf-8') as f:
    json.dump(class_data, f, indent=4, ensure_ascii=False)

print(f"已成功更新 data/entity.json 文件，并将 classname 与 classid 的对应关系存储到 data/class.json 文件")