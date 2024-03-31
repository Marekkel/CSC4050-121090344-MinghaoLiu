import re

text = "dsaf3sf"
match = re.search(r'([01])', text)

if match:
    result = match.group(1)
else:
    result = "字符串中没有0或1"

print(result)  # 输出：0
