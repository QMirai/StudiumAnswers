import pandas as pd
import re

ENCODING = 'utf-8'


class StudiumAnswers:
    """
    One answer to treat, one instance.
    """
    def __init__(self, studium_file: str, previous_answers: str, answer_num: float):
        """
        self.data contains just 2 columns: 'Adresse de courriel' and 'Réponse num'.
        Parameters
            studium_file: Studium file path.
            response_num: Question number whose answers to be corrected.
        """
        self.answer_column = f'Réponse {answer_num}'
        self.email_answer = pd.read_csv(studium_file)[['Adresse de courriel', self.answer_column]]
        self.cleaned_email_answers_note = pd.DataFrame()  # cleaned answers without note
        if previous_answers.endswith('csv'):
            self.pre_answers = pd.read_csv(previous_answers)
        elif previous_answers.endswith('xlsx'):
            self.pre_answers = pd.read_excel(previous_answers)
        else:
            raise Exception(f'{previous_answers} not .csv or .xlsx file')

    @staticmethod
    def clean_string(string: str):
        """
        Strips a string and cleans it from uppercase, punctuation and paragraph html tag.
        Parameters
            string (string): string to clean
        Returns
            clean string
        """
        punct = ['.', '!', '?', ';']
        string = string.strip().lower()
        string = ''.join(ch for ch in string if ch not in punct)
        string = re.sub(r'\s+', ' ', string)
        html = re.compile('<p>|</p>')
        string = re.sub(html, '', string)
        return string

    def clean_answers(self):
        """
        Cleans answers from a column of answers extracted from Studium and creates a new file with unique clean answers
        and an empty column to grade them manually.
        Returns
            df contains email, answers, note
        """
        df = self.email_answer
        df = df.fillna('vide')

        # clean answers
        df[self.answer_column] = df[self.answer_column].apply(self.clean_string)

        # set new empty column 'Note'
        df['Note'] = 'DONNEZ UNE VALEUR'
        return df

    def concat_previous_answers(self, out_file):
        """
        Make references file with previous answers and current answers.
        Merges in df previous years' unique answers and their grade to not yet graded current year's unique answers.
        Current year's answers identical to previous years' answers are dropped.
        Parameters
            out_file (string): output file name
        Returns
            None, saves csv file merging both new and previous answers to the same question
        """
        self.cleaned_email_answers_note = self.clean_answers()
        current_answers = self.cleaned_email_answers_note[[self.answer_column, 'Note']]
        df_all = pd.concat([self.pre_answers, current_answers], ignore_index=True)
        df_all = df_all.drop_duplicates(self.answer_column).sort_values(by=self.answer_column)
        df_all.to_csv(out_file, encoding=ENCODING, index=False)

    def compile_grades(self, references_file: str, out_file: str):
        """
        Maps unique answers and corresponding grade to student's email in a df and saves it to file.
        Parameters
            references_file (string): name of manually graded file containing unique answers and corresponding grade +
            previous years' answers and their grade.
            out_file (string): output file name
        Returns
            None, saves df to file
        """
        references_df = pd.read_csv(references_file).sort_values(by=self.answer_column)
        notes = dict()
        for index, row in self.cleaned_email_answers_note.sort_values(by=self.answer_column).iterrows():
            for i_g, r_g in references_df.iterrows():
                if row[self.answer_column] == r_g.loc[self.answer_column]:
                    notes[row.loc['Adresse de courriel']] = r_g.loc['Note']
                    break
            else:
                raise Exception(f"<{row[self.answer_column]}> : Not found its note in referneces")
        out_df = pd.DataFrame(notes, index=['Note']).transpose()
        out_df.to_csv(out_file, index_label='Adresse de courriel', encoding=ENCODING)
        print(f"<{out_file}> written successfully.")
