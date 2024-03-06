import pandas as pd
from pywebio.input import *
from pywebio.output import *
from studium_answers import StudiumAnswers
from io import StringIO
import re
import sys

text = ("If the references file has been updated by the auxiliary, please select 'Yes.' Otherwise, select 'No.' "
        "In this case, we will only output a concatenated references file that the auxiliary needs to mark.")


def get_question_num(file):
    df = pd.read_csv(file)
    return [col for col in df.columns if col.startswith('Réponse')]


def main():
    # Prompt user to upload a file
    studium_file = file_upload("Upload Studium answers table:", accept='.csv')
    if studium_file is None:
        put_markdown(f"Error: No file uploaded as Studium answers file.")
        raise Exception(f"Error: No file uploaded as Studium answers file.")

    input_column_num = checkbox('Please select the question number(s) that you want to process.',
                                options=get_question_num(StringIO(studium_file['content'].decode('utf-8'))))

    # Process questions, each question is an instance of StudiumAnswers
    for response in input_column_num:
        num = re.search(r'\d+', response).group(0)
        put_markdown(f"For Question {num}")
        references_file = file_upload("Upload references:", accept='.tsv')
        if references_file is None:
            put_markdown(f"Error: No file uploaded as references file.")
            raise Exception(f"Error: No file uploaded as references file.")

        radio_compile_grade = radio('Continue and compile grade?', options=['Yes', 'No'], help_text=text)

        if studium_file and references_file:
            sa = StudiumAnswers(StringIO(studium_file['content'].decode('utf-8')),
                                StringIO(references_file['content'].decode('utf-8')),
                                num)
            email_cleaned_answers_note = sa.clean_answers()
            if radio_compile_grade == 'Yes':
                try:
                    sa.compile_grades(email_cleaned_answers_note, f'Q{num}-notes.csv')
                except Exception as err:
                    print(f"{err}\nPlease make sure that you submitted the right files.")
                    put_markdown(f"{err}\nPlease make sure that you submitted the right files.")
                    sys.exit(1)
                put_markdown(f'"Q{num}-notes.csv" has been written successfully.\nThank you for using.')
            else:
                sa.concat_previous_answers(email_cleaned_answers_note[['Réponse', 'Note']],
                                           f'Q{num}-concatenated_ref_to_correct.tsv')
                put_markdown(f'"Q{num}-concatenated_ref_to_correct.tsv" has been written successfully.\nThank you for '
                             f'using.')

    if len(input_column_num) < 1:
        put_markdown('Error: number not input.')
        raise Exception('Error: number not input.')


if __name__ == "__main__":
    main()
