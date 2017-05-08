
import unittest
import pandas as pd
from commit import Commit,Change
from datetime import date

from data_analyzer import get_commits_and_changes, read_file, get_commit_changes_data_frame, get_commit_data_frame, get_authors_most_commits, get_most_commit_single_day, get_commit_with_most_changes

class TestCommits(unittest.TestCase):

    def setUp(self):
        self.data = read_file('changes_python.log')

    def test_number_of_lines(self):
        self.assertEqual(5255, len(self.data))

    def test_number_of_commits_and_changes(self):
        log = get_commits_and_changes(self.data);
        commits = log[0]
        changes = log[1]
        self.assertEqual(422, len(commits))
        self.assertEqual(3009, len(changes))


    def test_first_commit_and_change(self):
        log = get_commits_and_changes(self.data);
        commits = log[0]
        changes = log[1]
        self.assertEqual('Thomas', commits[0].author)
        self.assertEqual(1551925, commits[0].revision)
        self.assertEqual(1551925, changes[0].revision)



    def test_data_frame(self):
        #set up dataframe
        log = get_commits_and_changes(self.data);
        commits = log[0]
        changes = log[1]
        commit_df = get_commit_data_frame()
        changes_df = get_commit_changes_data_frame()
        
        self.assertEqual(422, (len(commit_df.index)))
       
        # test column labels are correct
        data_frame_columns = list(commit_df)
        commit_labels = Commit.LABELS
        self.assertEqual(commit_labels, data_frame_columns)
        
        # test correct number of columns
        self.assertEqual(len(commit_df.columns), 5)
        
        # test column labels are correct
        data_frame_columns = list(changes_df)
        changes_labels = Change.LABELS
        self.assertEqual(changes_labels, data_frame_columns)
        
        # test correct number of columns
        self.assertEqual(len(changes_df.columns), 3)
        
        
        #test  some of analysis logic
        authors_most_commits= get_authors_most_commits(commit_df)
        self.assertEqual( authors_most_commits, 'Thomas' )

        most_commit_single_day= get_most_commit_single_day(commit_df)
        self.assertEqual(most_commit_single_day, 19)

        commit_with_most_changes = get_commit_with_most_changes(changes_df)
        self.assertEqual(commit_with_most_changes, 1495579)


if __name__ == '__main__':
    unittest.main()
