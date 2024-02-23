from pywebio.input import *
from pywebio.output import *
from studium_answers import StudiumAnswers
from io import StringIO

text = ("If the references file has been updated by the auxiliary, please select 'Yes.' Otherwise, select 'No.' "
        "In this case, we will only output a concatenated references file that the auxiliary needs to mark.")


def must_number(s: str):
    s = s.strip().split()
    for num in s:
        if not num.isdigit():
            return f"{num} is not a number"


def main():
    # Prompt user to upload a file
    studium_file = file_upload("Upload Studium answers table:", accept='.csv')
    input_column_num = input('Question number(s)', type=TEXT, validate=must_number,
                             help_text='Separate numbers with space. If you want to process Q1 and Q20, tape: 1 20')

    # Process questions, each question is an instance of StudiumAnswers
    for num in input_column_num.split():
        references_file = file_upload("Upload references:", accept='.csv')
        radio_compile_grade = radio('Continue and compile grade?', options=['Yes', 'No'],
                                    help_text=text)
        if studium_file and references_file:
            sa = StudiumAnswers(StringIO(studium_file['content'].decode('utf-8')),
                                StringIO(references_file['content'].decode('utf-8')), num)
            sa.concat_previous_answers(f'Q{num}-concatenated_ref_to_correct.csv')
            if radio_compile_grade == 'Yes':
                sa.compile_grades(f'Q{num}-concatenated_ref_to_correct.csv', f'Q{num}-notes.csv')
                put_markdown(f'"Q{num}-notes.csv" has been written successfully.\nThank you for using.')
            else:
                put_markdown(f'"Q{num}-concatenated_ref_to_correct.csv" has been written successfully.\nThank you for '
                             f'using.')
        else:
            if studium_file is None:
                raise Exception(f"No file uploaded as Studium answers file.")
            elif references_file is None:
                raise Exception(f"No file uploaded as previous references file.")
            else:
                raise Exception(f"{studium_file['filename']} or {references_file['filename']} error.")


if __name__ == "__main__":
    main()
