# For test

from studium_answers import StudiumAnswers

# first load for merge
sa = StudiumAnswers('reponses.csv', 'q14-references.tsv', 14)
email_cleaned_answers_note = sa.clean_answers()
sa.concat_previous_answers(email_cleaned_answers_note[['Réponse', 'Note']],
                           'Q14-concatenated_ref_to_correct.tsv')

# reload after the references file is updated
sa = StudiumAnswers('reponses.csv', 'Q14-concatenated_ref_to_correct.tsv', 14)
email_cleaned_answers_note = sa.clean_answers()
sa.compile_grades(email_cleaned_answers_note, 'Q14-notes.csv')
