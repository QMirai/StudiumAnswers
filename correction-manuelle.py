ANSWERS = 'reponses.csv'
GRADES = 'notes-intra.csv'
MANUAL = [7,14]


import pandas as pd
import re

grades = pd.read_csv(GRADES)

questions = []
rename = {}
for column in grades.columns:
    m = re.match(r'^Q\. (\d+) /(\d+,\d+)$', column)
    if m:
        n = m.group(1)
        question = 'Q'+n
        questions.append(question)
        rename[column] = question
grades.rename(columns=rename, inplace=True)

# Convert strings to floats
for q in questions:
    grades[q] = grades[q].apply(lambda s: re.sub(r'^\-$', '0', s))
    grades[q] = grades[q].apply(lambda s: re.sub(r'^(\d+),(\d+)$', r'\1.\2', s))
grades[questions] = grades[questions].astype(float)


answers = pd.read_csv(ANSWERS)
rename = {}
for column in answers.columns:
    m = re.match(r'^Réponse (\d+)$', column)
    if m:
        n = m.group(1)
        answer = 'A'+n
        rename[column] = answer
answers.rename(columns=rename, inplace=True)

data = grades.set_index('Adresse de courriel').merge(answers.set_index('Adresse de courriel'))

for n in MANUAL:
    data[['Nom', 'Prénom', f'Q{n}', f'A{n}']].sort_values([f'Q{n}', f'A{n}']).to_excel(f'reponses-q{n}.xlsx', index=False)
