import itertools
import random
import os

def generate_combinations(information_fields):
    """
    对给定的企业办公信息进行排列组合

    Parameters:
    - information_fields: 包含各种信息的字典，每个键值对代表一个信息字段及其可能的取值

    Returns:
    生成的排列组合列表
    """
    all_combinations = []

    # 将所有输入的字符串合并为一个集合
    unique_values = set(value for values in information_fields.values() for value in values)

    # 生成所有可能的两两、三三、四四等排列组合
    for r in range(2, len(unique_values) + 1):
        combinations_r = list(itertools.combinations(unique_values, r))
        all_combinations.extend(combinations_r)

    return all_combinations

def randomize_combinations(combinations):
    """
    随机排列生成的组合

    Parameters:
    - combinations: 组合列表

    Returns:
    随机排列后的组合列表
    """
    random.shuffle(combinations)
    return combinations

def save_combinations_to_file(file_path, combinations):
    """
    将生成的组合保存到文件

    Parameters:
    - file_path: 文件路径
    - combinations: 组合列表
    """
    with open(file_path, 'w') as file:
        for combination in combinations:
            # 将每个组合中的元素转换为字符串再写入文件
            file.write(''.join(map(str, combination)) + '\n')

if __name__ == '__main__':
    # 输入企业办公信息
    information_fields = {
        "公司名称": input("请输入公司名称（多个值用逗号分隔）: ").split(','),
        "公司域名": input("请输入公司域名（多个值用逗号分隔）: ").split(','),
        "姓名": input("请输入姓名（多个值用逗号分隔）: ").split(','),
        "英文名": input("请输入英文名（多个值用逗号分隔）: ").split(','),
        "姓名首字母缩写": input("请输入姓名首字母缩写（多个值用逗号分隔）: ").split(','),
        "工号": input("请输入工号（多个值用逗号分隔）: ").split(','),
        "办公地点": input("请输入办公地点（多个值用逗号分隔）: ").split(',')
    }

    all_combinations = generate_combinations(information_fields)

    if all_combinations:
        # 随机排列组合
        randomized_combinations = randomize_combinations(all_combinations)

        # 生成文件路径
        file_name = "_".join(information_fields["姓名"]) + ".txt"
        file_path = os.path.join(os.getcwd(), file_name)

        # 保存组合到文件
        save_combinations_to_file(file_path, randomized_combinations)
        print(f"\n组合已保存到文件：{file_path}")
    else:
        print("\n未生成组合列表。")
