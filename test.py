import pandas as pd
from pywebio.input import *
from pywebio.output import *
from studium_answers import StudiumAnswers
from io import StringIO
import re
import sys

text = ("If the references file has been updated by the auxiliary, please select 'Yes.' Otherwise, select 'No.' "
        "In this case, we will only output a concatenated references file that the auxiliary needs to mark.")


def get_question_num(file_content):
    df = pd.read_csv(StringIO(file_content['content'].decode('utf-8')))
    return [col for col in df.columns if col.startswith('Réponse')]


def upload_file_validation(files):
    if files['studium_file'] is None:
        return f"Error: No file uploaded as Studium answers file."
    else:
        return None


def main():
    files = input_group(
        'Upload file',
        [
            file_upload("Upload Studium answers table:", accept='.csv', name='studium_file',
                        onchange=lambda content: input_update('q_num', options=get_question_num(content))),
            checkbox('Please select the question number(s) that you want to process.',
                     options=['Waiting for the uploaded file...'], name='q_num')],
        validate=upload_file_validation
    )
    print(files['q_num'])


if __name__ == "__main__":
    main()
