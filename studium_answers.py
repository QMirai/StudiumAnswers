import pandas as pd
import re

ENCODING='utf8'

def clean_string(string):
    """
    Strips a string and cleans it from uppercase, punctuation and paragraph html tag.
    Parameters
        string (string): string to clean
    Returns
        clean string
    """
    punct = [',', '.', '!', '?', ';']
    string = string.strip().lower()
    string = ''.join(ch for ch in string if ch not in punct)
    string = re.sub('\s+', ' ', string)
    html = re.compile(('<p>|</p>'))
    string = re.sub(html, '', string)
    return string

def clean_answers(in_file, out_file, column):
    """
    Cleans answers from a column of answers extracted from Studium and creates a new file with unique clean answers and an empty column to grade them manually.
    Parameters
        in_file (string): name of input file extracted from studium with all answers, info etc.
        out_file (string): output file name
        column (string): column of answers from in_file to be graded
    Returns
        None, saves df to file
    """
    df = pd.read_csv(in_file)
    df = df.fillna('vide')
    answers = set([clean_string(r) for r in df[column].to_list()])
    out_df = pd.DataFrame({column: list(answers), 'Note': ''})
    with open(out_file, 'w', encoding=ENCODING) as f:
        out_df.to_csv(out_file)

def compile_grades(in_file, graded_file, out_file, column):
    """
    Maps unique answers and corresponding grade to student's email in a df and saves it to file.
    Parameters
        in_file (string): name of input file extracted from studium with all answers, info etc.
        graded_file (string): name of manually graded file containing unique answers and corresponding grade + previous years' answers and their grade. Should be created with clean_answers()
        out_file (string): output file name
        column (string): column of answers shared between in_file and graded_file to compare answers and map them to corresponding student
    Returns
        None, saves df to file
    """
    in_df = pd.read_csv(in_file)
    in_df = in_df.fillna('vide')
    graded_df = pd.read_csv(graded_file)
    notes = dict()
    for index, row in in_df.iterrows():
        answer = clean_string(row.loc[column])
        notes[row.loc['Adresse de courriel']] = ([r.Note for i, r in
        graded_df.iterrows() if answer == r.loc[column]])
    out_df = pd.DataFrame(notes, index=['Note']).transpose()
    with open(out_file, 'w', encoding=ENCODING) as f:
        out_df.to_csv(out_file, index_label='Adresse de courriel')

def merge_previous_answers(previous_answers, current_answers, out_file, column):
    """
    Merges in df previous years' unique answers and their grade to not yet graded current year's unique answers. Current year's answers identical to previous years' answers are dropped.
    Parameters
        previous_answers (string): name of input file containing previous year's clean answers and their grade
        current_answers (string): name of input file containing this year's clean answers with empty column for grade
        out_file (string): output file name
        column (string): column name in both input files corresponding to the question for which answers are to be graded
    Returns
        None, saves csv file merging both new and previous answers to the same question
    """
    if previous_answers.endswith('csv'):
        old_df = pd.read_csv(previous_answers)
    elif previous_answers.endswith('xlsx'):
        old_df = pd.read_excel(previous_answers)
    current_df = pd.read_csv(current_answers)
    df_all = df.merge(current_df[[column, 'Note']], how='outer')
    df_all = df.sort_values('Note')
    df_all = df_all.drop_duplicates(column)
    df_all.to_csv(out_file)
