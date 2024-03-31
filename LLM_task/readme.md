
run 1.prepare_data.py:
    python 1.prepare_data.py --input_path="./data/1.sample.json" --output_path="./data/2.sample_prepared.jsonl"

run GPT_parse.py:
    python GPT_parse.py

run 2.GPT_multi_parse.py:
    python ./2.GPT_multi_parse.py --keys_path="gpt3keys.txt" --input_path="./data/2.sample_prepared.jsonl" --output_path="./data/3.sample_aftgpt.jsonl" --max_workers=5

run 3.scorer.py:
    python 3.scorer.py --input_path="./data/3.sample_aftgpt.jsonl" --wrong_ans_path="./data/4.wrong_ans.json" --score_path="./data/4.score.json"