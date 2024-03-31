import json
import argparse
import pdb
prompt = '''
Below is the README text of a Python package. I only need you to tell me whether the author mentioned that they had deprecated this package or have the intention to deprecate the package. 0 means no, 1 means yes. Additionally, if they deprecated (which means 1), you need to tell me whether the author has provided alternative solutions. Your answer be:\n(0) if no deprecation\nOR\nThe alternative method mentioned by the author (if mentioned) & (1). \n ATTENTION: The archive package should also be taken into deprecation. \n {readme_text}
'''

def generate_query(data):
    readme_text = data['query']
    return prompt.format(readme_text=readme_text)


def prepare_data(args):
    try:
        # 读取上传的JSON文件
        with open(args.input_path, encoding='utf-8') as f:
            data = json.load(f)

        print(f"Read {len(data)} items from '{args.input_path}'")

        # 根据要求转换
        jsonl_data = [
            {
                "id": id,
                "query": generate_query(item),
                "model_answer": "",
                "alternative_method": "",
                "label": item['label']
            }
            for id, item in enumerate(data)
        ]

        # 将转换后的数据保存为JSONL文件
        with open(args.output_path, "w", encoding="utf-8") as file:
            for entry in jsonl_data:
                json.dump(entry, file, ensure_ascii=False)
                file.write("\n")
        
        print(f"Prepare finished, output to '{args.output_path}'")

    except FileNotFoundError:
        print(f"Error: File '{args.input_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{args.input_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Prepare data for OpenAIGPT generation")
    parser.add_argument("--input_path", type=str, required=True, help="Path to the input JSON file.")
    parser.add_argument("--output_path", type=str, required=True, help="Path to the output JSONL file.")
    args = parser.parse_args()
    prepare_data(args)
