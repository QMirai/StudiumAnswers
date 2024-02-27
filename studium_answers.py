import pandas as pd
import re

ENCODING = 'utf-8'


class StudiumAnswers:
    """
    One question, one instance.
    """
    def __init__(self, studium_file, references_file, answer_num: float):
        """
        self.data contains just 2 columns: 'Adresse de courriel' and 'Réponse num'.
        Parameters
            studium_file: Studium file path.
            previous_answers: references (an answers-notes pool) path.
            response_num: Question number whose answers to be corrected.
        """
        self.answer_column = f'Réponse {answer_num}'
        self.email_answer = pd.read_csv(studium_file)[['Adresse de courriel', self.answer_column]]
        self.email_answer.rename(columns={self.answer_column: 'Réponse'}, inplace=True)
        self.cleaned_email_answers_note = pd.DataFrame()  # email, cleaned answers and empty note
        self.references_file = pd.read_csv(references_file, sep='\t')

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
        string = re.sub(r"['’ʼ‛]", "'", string)  # formalize apostrophes
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
        df['Réponse'] = df['Réponse'].apply(self.clean_string)

        # set new empty column 'Note'
        df['Note'] = ''
        return df

    def concat_previous_answers(self, current_answers, out_file: str):
        """
        Update references file with previous answers and current answers.
        Merges in df previous years' unique answers and their grade to not yet graded current year's unique answers.
        Current year's answers identical to previous years' answers are dropped.
        Parameters
            out_file (string): output file name
        Returns
            None, saves tsv file merging both new and previous answers to the same question
        """
        df_all = pd.concat([self.references_file, current_answers], ignore_index=True)
        df_all = df_all.drop_duplicates('Réponse').sort_values('Réponse')
        df_all.to_csv(out_file, sep='\t', encoding=ENCODING, index=False)

    def compile_grades(self, email_cleaned_answers_note, out_file: str):
        """
        Maps unique answers and corresponding grade to student's email in a df and saves it to file.
        Parameters
            email_cleaned_answers_note: A DataFrame instance that contains email, cleaned answers and empty note columns
            out_file (string): output file name
        Returns
            None, saves df to file
        """
        references_df = self.references_file.sort_values(by='Réponse')
        notes = dict()
        for index, row in email_cleaned_answers_note.sort_values(by='Réponse').iterrows():
            for i_g, r_g in references_df.iterrows():
                if row['Réponse'] == r_g.loc['Réponse']:
                    notes[row.loc['Adresse de courriel']] = r_g.loc['Note']
                    break
            else:
                raise Exception(f"<{row['Réponse']}> : Not found its note in referneces")
        out_df = pd.DataFrame(notes, index=['Note']).transpose()
        out_df.to_csv(out_file, index_label='Adresse de courriel', encoding=ENCODING)
        print(f"<{out_file}> written successfully.")
