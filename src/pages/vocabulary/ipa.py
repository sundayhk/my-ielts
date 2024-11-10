import requests
from bs4 import BeautifulSoup
from pathlib import Path
from collections import defaultdict

CUR_DIR = Path(__file__).absolute().parent
vocabulary_path = CUR_DIR / 'vocabulary.txt'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
}

def getIPA(word):
    # url = f"https://dictionary.cambridge.org/dictionary/english-chinese-simplified/{word}"
    url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}"
    response = requests.get(url, headers=headers)

    # 检查请求是否成功
    if response.status_code == 200:
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 找到所有包含音标的span标签
        # pronunciation_spans = soup.find_all('span', class_='ipa')
        pronunciation_span = soup.find('span', class_='phon')

        if pronunciation_span:
            pronunciation = pronunciation_span.text
            return f"{pronunciation}"
        else:
            print("未找到音标。")
            return False
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return False
    

# apple = getPhoneticSymbol('phenomenon')
# print(apple)

contents = '\n'.join([l.strip() for l in vocabulary_path.read_text().split('\n')])
rows = contents.split('\n')

categories = contents.split('===\n')
labels = ['===','---','+++']
for category in categories:
    category_parts = category.split('+++\n')
    label = category_parts[0].strip()
    labels.append(label)


input_file_path = 'source.txt'   # 读取的文件
output_file_path = './output.txt'  # 写入的文件
with open(output_file_path, 'w') as output_file:
    for row in rows:
        row = row + '\n'
        if row.strip() in labels:
            output_file.write(row)
        else:
            words = row.split('|')
            word = words[0]
            try:
                ipa = getIPA(word)
                if not ipa:
                    ipa = 'None'
            except Exception as e:
                ipa = 'None'
            print(ipa)
            words.insert(1, ipa)
            line = '|'.join(words)
            print(line)
            output_file.write(line)



