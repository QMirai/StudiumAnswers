from studium_answers import StudiumAnswers

# load excel or csv: email answers
sa = StudiumAnswers('reponses.csv', 'q14-references.csv', 14)
sa.concat_previous_answers('new.csv')
sa.compile_grades('new.csv', 'results.csv')
