import unittest
from unittest.mock import MagicMock
from s3filesearch import search_files_in_s3  # Replace 'script_name' with the name of your script file

class TestSearchFilesInS3(unittest.TestCase):

    def setUp(self):
        # Mock S3 client
        self.mock_s3_client = MagicMock()

    def test_single_file_contains_substring(self):
        # Setup mock response
        self.mock_s3_client.list_objects_v2.return_value = {
            'Contents': [{'Key': 'testfile.txt'}]
        }
        self.mock_s3_client.get_object.return_value = {
            'Body': MagicMock(read=MagicMock(return_value=b'This is a test content with the word python.'))
        }

        # Run the function
        result = search_files_in_s3('mock-bucket', 'python', s3_client=self.mock_s3_client)

        # Assert the result
        self.assertEqual(result, ['testfile.txt'])

    def test_multiple_files_some_contain_substring(self):
        # Setup mock response
        self.mock_s3_client.list_objects_v2.return_value = {
            'Contents': [{'Key': 'file1.txt'}, {'Key': 'file2.txt'}, {'Key': 'file3.txt'}]
        }
        self.mock_s3_client.get_object.side_effect = [
            {'Body': MagicMock(read=MagicMock(return_value=b'Content without the search term.'))},
            {'Body': MagicMock(read=MagicMock(return_value=b'This is a python script.'))},
            {'Body': MagicMock(read=MagicMock(return_value=b'Another file with Python in it.'))},
        ]

        # Run the function
        result = search_files_in_s3('mock-bucket', 'python', s3_client=self.mock_s3_client)

        # Assert the result
        self.assertEqual(result, ['file2.txt', 'file3.txt'])

    def test_no_files_contain_substring(self):
        # Setup mock response
        self.mock_s3_client.list_objects_v2.return_value = {
            'Contents': [{'Key': 'file1.txt'}, {'Key': 'file2.txt'}]
        }
        self.mock_s3_client.get_object.side_effect = [
            {'Body': MagicMock(read=MagicMock(return_value=b'No relevant content.'))},
            {'Body': MagicMock(read=MagicMock(return_value=b'Still no match here.'))},
        ]

        # Run the function
        result = search_files_in_s3('mock-bucket', 'python', s3_client=self.mock_s3_client)

        # Assert the result
        self.assertEqual(result, [])

    def test_encoding_issues_handled(self):
        # Setup mock response
        self.mock_s3_client.list_objects_v2.return_value = {
            'Contents': [{'Key': 'file1.txt'}, {'Key': 'file2.txt'}]
        }
        self.mock_s3_client.get_object.side_effect = [
            {'Body': MagicMock(read=MagicMock(return_value=b'\x80\x81\x82'))},  # Invalid UTF-8 bytes
            {'Body': MagicMock(read=MagicMock(return_value=b'Proper content with Python.'))},
        ]

        # Run the function
        result = search_files_in_s3('mock-bucket', 'python', s3_client=self.mock_s3_client)

        # Assert the result
        self.assertEqual(result, ['file2.txt'])

    def test_empty_bucket(self):
        # Setup mock response
        self.mock_s3_client.list_objects_v2.return_value = {}

        # Run the function
        result = search_files_in_s3('mock-bucket', 'python', s3_client=self.mock_s3_client)

        # Assert the result
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
