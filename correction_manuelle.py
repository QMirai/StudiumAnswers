# For test

from studium_answers import StudiumAnswers

# load excel or csv: email answers
sa = StudiumAnswers('reponses.csv', 'q14-references.csv', 14)
sa.concat_previous_answers('Q14-concatenated_ref_to_correct.csv')
sa.compile_grades('Q14-concatenated_ref_to_correct.csv', 'Q14-notes.csv')
