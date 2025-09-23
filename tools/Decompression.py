#!/usr/bin/env python3  
"""  
Arrow 数据集解压脚本（修复版）  
将 data-00000-of-00001.arrow 中的所有内容解压出来  
能存 JSON 的存 JSON，不能存的转成 base64  
"""

import json
import base64
import os
from pathlib import Path
from datasets import Dataset
from PIL import Image
import io


def extract_arrow_dataset(arrow_file_path="data-00000-of-00001.arrow",
                          output_dir="./extracted_data"):
    """  
    解压 Arrow 数据集文件  

    Args:  
        arrow_file_path: Arrow 文件路径  
        output_dir: 输出目录  
    """

    # 创建输出目录  
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # 加载 Arrow 数据集  
    print(f"正在加载 {arrow_file_path}...")
    dataset = Dataset.from_file(arrow_file_path)

    print(f"数据集信息:")
    print(f"- 样本数量: {len(dataset)}")
    print(f"- 列名: {dataset.column_names}")

    # 存储所有解压的数据  
    extracted_data = []

    for i in range(len(dataset)):
        print(f"正在处理样本 {i + 1}/{len(dataset)}...")

        row = dataset[i]
        extracted_row = {}

        # 处理每一列的数据  
        for column_name, value in row.items():
            if column_name == 'image' and value is not None:
                # 图像数据处理  
                try:
                    # 检查是否已经是 PIL Image 对象  
                    if hasattr(value, 'save'):  # PIL Image 对象有 save 方法  
                        image = value
                        print(f"  - 检测到 PIL Image 对象")
                    else:
                        # 如果是字节数据，则转换为 PIL Image  
                        image = Image.open(io.BytesIO(value))
                        print(f"  - 从字节数据创建 PIL Image")

                    # 保存为 PNG 文件
                    image_filename = f"image_{i}.png"
                    image_path = output_path / image_filename
                    image.save(image_path)

                    extracted_row[f'{column_name}_file'] = image_filename

                    print(f"  - 图像已保存: {image_filename}")

                except Exception as e:
                    print(f"  - 图像处理失败: {e}")
                    # 如果处理失败，尝试将对象转换为字符串  
                    extracted_row[f'{column_name}_error'] = str(value)

            elif isinstance(value, bytes):
                # 其他二进制数据：转换为 base64  
                extracted_row[f'{column_name}_base64'] = base64.b64encode(value).decode('utf-8')
                print(f"  - {column_name} 已转换为 base64")

            elif isinstance(value, (str, int, float, bool, list, dict)) or value is None:
                # 可以直接 JSON 序列化的数据  
                extracted_row[column_name] = value

            else:
                # 其他类型：尝试转换为字符串  
                try:
                    extracted_row[column_name] = str(value)
                    print(f"  - {column_name} 已转换为字符串: {type(value)}")
                except Exception as e:
                    # 最后手段：记录错误信息  
                    extracted_row[f'{column_name}_error'] = f"无法处理的类型: {type(value)}"
                    print(f"  - {column_name} 处理失败: {e}")

        extracted_data.append(extracted_row)

        # 保存完整的 JSON 数据  
    json_file = output_path / "complete_dataset.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 解压完成!")
    print(f"- JSON 数据: {json_file}")
    print(f"- 图像文件: {output_path}/*.png")

    # 生成数据统计  
    stats = {
        "total_samples": len(extracted_data),
        "columns": list(dataset.column_names),
        "output_directory": str(output_path),
        "files_created": []
    }

    # 统计生成的文件  
    for file in output_path.iterdir():
        if file.is_file():
            stats["files_created"].append(file.name)

            # 保存统计信息  
    stats_file = output_path / "extraction_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"- 统计信息: {stats_file}")

    return extracted_data, stats


def main():
    """主函数"""
    try:
        # 检查 Arrow 文件是否存在  
        arrow_file = "data-00000-of-00001.arrow"
        if not os.path.exists(arrow_file):
            print(f"❌ 错误: 找不到文件 {arrow_file}")
            print("请确保已经运行过 DataDreamer 管道并生成了数据文件")
            return

            # 执行解压  
        data, stats = extract_arrow_dataset(arrow_file)

        print(f"\n📊 解压统计:")
        print(f"- 总样本数: {stats['total_samples']}")
        print(f"- 列数: {len(stats['columns'])}")
        print(f"- 生成文件数: {len(stats['files_created'])}")

    except Exception as e:
        print(f"❌ 解压过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()