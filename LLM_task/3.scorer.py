import re
import jsonlines
import json
import argparse
import os

# def match_choice(text):
#     match = re.findall(r'.*?([A-E]+(?:[、, ]+[A-E]+)*)', text)
#     if match:
#         last_match = match[-1]
#         return ''.join(re.split(r'[、, ]+', last_match))
#     return ''

def match_result(text):
    match = re.search(r'([01])', text)
    if match:
        result = match.group(1)
        return result
    return ''


def calculate_score(label, model_answer):
    try:
        result = int(match_result(model_answer))
        return result == label, result
    except:
        result = match_result(model_answer)
        return result == label, result

def score_result(input_path, wrong_ans_path, score_path):
    items = []

    with jsonlines.open(input_path, "r") as reader:
        items = list(reader)

    label_sign = [0, 1]
    type2score = {q_type: {'correct': 0, 'total': 0} for q_type in label_sign}
    wrong_data = []

    for item in items:
        l_type = item['label']
        label = item['label']
        is_correct, model_label = calculate_score(label, item['model_answer'])

        if is_correct:
            type2score[l_type]['correct'] += 1
        else:
            item['model_label'] = model_label
            wrong_data.append(item)

        type2score[l_type]['total'] += 1

    total_correct = 0
    for l_type, item in type2score.items():
        sub_total = item['total']
        if sub_total == 0:
            continue
        total_correct = total_correct + item['correct']
        accuracy = item['correct'] / item['total']
        print(f'[{l_type}]accuracy：{accuracy:.3f}  sub_total: {sub_total}')

    total_questions = len(items)
    print(f'total correct：{total_correct}  / total questions：{total_questions}')
    print(f'total accuracy:{total_correct / total_questions}')
    print(f'wrong：{len(wrong_data)}, output to {wrong_ans_path}')

    with open(wrong_ans_path, 'w', encoding='utf-8') as fw:
        json.dump(wrong_data, fw, ensure_ascii=False, indent=4)

    # Output scores to a separate file
    score_info = {
        'total_score': total_correct,
        'total_questions': total_questions,
        'scores_by_type': type2score
    }
    
    with open(score_path, 'w', encoding='utf-8') as fscore:
        json.dump(score_info, fscore, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Score and analyze questions.')
    parser.add_argument('--input_path', required=True, help='Path to the input JSON file')
    parser.add_argument('--wrong_ans_path', required=True, help='Path to the output JSON file for incorrect answers')
    parser.add_argument('--score_path', required=True, help='Path to the output JSON file for scores')

    args = parser.parse_args()
    score_result(args.input_path, args.wrong_ans_path, args.score_path)


