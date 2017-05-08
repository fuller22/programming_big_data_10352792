import csv
import pandas as pd
from commit import Commit,Change

from collections import OrderedDict
from datetime import date

def read_file(changes_file):
    # use strip to strip out spaces and trim the line.
    data = [line.strip() for line in open(changes_file, 'r')]
    return data


def get_commits_and_changes(data):
    sep = 72*'-'
    commits = []
    changes = []
    current_commit = None
    new_change = None
    index = 0

    author = {}
    while True:
        try:
            # parse each of the commits and put them into a list of commits
            current_commit = Commit()
            details = data[index + 1].split('|')
            current_commit.revision = int(details[0].strip().strip('r'))
            current_commit.author = details[1].strip()
            date = details[2].strip()
            date = date.split("+")
            current_commit.date = date[0].strip()
            current_commit.comment_line_count = int(details[3].strip().split(' ')[0])
           
            # parse each of the commits change log and put them into a list changes
            changes_data = data[index+3:data.index('',index+1)]
            for i in changes_data:
                new_change = Change()
                if  isinstance(i,str) and i.startswith("A "):
                    new_change.type = "add"
                    new_change.revision = current_commit.revision
                    new_change.path = i.strip('A ');
                    changes.append(new_change)
                elif isinstance(i,str) and i.startswith("D "):
                    new_change.type = "delete"
                    new_change.revision = current_commit.revision
                    new_change.path = i.strip('D ')
                    changes.append(new_change)
                elif isinstance(i,str)and  i.startswith("M "):
                    new_change.type = "modify"
                    new_change.revision = current_commit.revision
                    new_change.path = i.strip('M ')
                    changes.append(new_change)

            index = data.index(sep, index + 1)
            current_commit.comment = data[index-current_commit.comment_line_count:index]
            commits.append(current_commit)
        except IndexError:
            break
    return [commits, changes]


# write the commits to cvs file
def write_commits_to_cvs(commits):
    with open('commit_log.csv', 'w') as csvfile:
        fieldnames = Commit.LABELS
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i, commit in enumerate(commits):
            writer.writerow(commits[i].get_commit())


# write the changes to cvs file, easier to data analyze when the changes are in separate file
def write_changes_to_cvs(changes):
    with open('commit_change_log.csv', 'w') as csvfile:
        fieldnames = Change.LABELS
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i, change in enumerate(changes):
            writer.writerow(changes[i].get_change())

# populate dataframe with date from cvs file
def get_commit_data_frame():
    return pd.read_csv('commit_log.csv')

# populate dataframe with date from cvs file
def get_commit_changes_data_frame():
    return pd.read_csv('commit_change_log.csv')


# Analyse date data
def analazye_date_data(df):
    
    df['date'] = pd.to_datetime(df['date'])
    dates = df.groupby([df.date.dt.year, df.date.dt.month, df.date.dt.day]).size()
    no_dates = dates.count();
    print("Number of different dates: " + str(no_dates))
    print("")
    
    most_commits_per_date = dates.max()
    print("Most number of commits made on a single day: " + str(most_commits_per_date))
    print("")
    
    date_most_commits = dates.idxmax()
    print("Date most changes were  commited: " + str(date_most_commits))
    print("")


def analyze_change_data(df):

    change_types = df.type.unique()
    print("Type of changes made to repository: " + str(change_types))
    print("")
    
    total_number_file_changes = len(df)
    print("Total number of file changes: " + str(total_number_file_changes))
    print("")

    num_file_changed = df.path.nunique()
    print("Number of different files that were altered: "  + str(num_file_changed))
    print("")
    
    type_counts = df.groupby('type').size()
    print("Break down of change types: " + str(type_counts))
    print("")
    
    file_path_counts = df['path'].value_counts()
    file_changed_most = file_path_counts.max()
    print("Most times a file was changed " + str(file_changed_most))
    print("")

    file_id = df['path'].value_counts().idxmax()
    print("File most changed:"  + str(file_id))
    print("")

    changes_per_revision =df.groupby('revision').size()

    commit_with_most_changes = df['revision'].value_counts().idxmax()
    print("Commit with most changes: " + str(commit_with_most_changes))
    print("")

    most_changes_per_commit =  df['revision'].value_counts().max()
    print("The highest number of changes per commit: " + str(most_changes_per_commit))
    print("")

    average_changes_per_commit =  df['revision'].value_counts().mean()
    print("Average changes per commit " + str(average_changes_per_commit))
    print("")


# Analyse author data
def analazye_author_data(df):
    
    num_authors =df.author.nunique()
    print("Number of authors: " + str(num_authors))
    print("")
    
    list_authors = df.author.unique()
    print("List of all authors: " + str(list_authors))
    print("")
    
    commits_per_author = df.groupby('author').size()
    print("Authors and the number of commits" + str(df.groupby('author').size()))
    print("")
   
    author_least_commits = df['author'].value_counts().idxmin()
    print("Author with the least commits: " + str(author_least_commits))
    print("")
    
    author_most_commits = df['author'].value_counts().idxmax()
    print("Author with most commits: " + str(author_most_commits))
    print("")
    
    max_commits = commits_per_author.max()
    print("Highest number of commits by author: " + str(max_commits))
    print("")
    
def get_authors_most_commits(df):
    return df['author'].value_counts().idxmax()

def get_most_commit_single_day(df):
    df['date'] = pd.to_datetime(df['date'])
    dates = df.groupby([df.date.dt.year, df.date.dt.month, df.date.dt.day]).size()
    return dates.max()

def get_commit_with_most_changes(df):
    return df['revision'].value_counts().idxmax()


if __name__ == '__main__':
    # open the file - and read all of the lines.
    changes_file = 'changes_python.log'
    data = read_file(changes_file)
    log = get_commits_and_changes(data)
    commits = log[0]
    changes = log[1]
    write_commits_to_cvs(commits)
    write_changes_to_cvs(changes)
    changes_df = get_commit_changes_data_frame()
    commits_df = get_commit_data_frame()
    analyze_change_data(changes_df)
    analazye_date_data(commits_df)
    analazye_author_data(commits_df)


