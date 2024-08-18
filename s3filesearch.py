import boto3
import sys
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def search_files_in_s3(bucket_name: str, search_string: str, s3_client=None):
    """
    Searches for files in the specified S3 bucket that contain a given substring (case-insensitive).
    Handles potential encoding issues by attempting different decoding strategies.
    
    Args:
    - bucket_name: Name of the S3 bucket to search.
    - search_string: Substring to search for in the files (case-insensitive).
    - s3_client: A boto3 S3 client. If None, a new client will be created. This argument facilitates unit testing.

    Returns:
    - List of file names containing the substring.
    """

    try:
        # Setup the S3 client
        if s3_client is None:
            s3_client = boto3.client('s3')

        # List all objects in the specified S3 bucket
        objects = s3_client.list_objects_v2(Bucket=bucket_name)

        # Check if the bucket contains any files
        if 'Contents' not in objects:
            print(f"No files found in bucket: {bucket_name}")
            return []

        matching_files = []

        # Normalize the search string to lowercase for case-insensitive comparison
        search_string_lower = search_string.lower()

        for obj in objects['Contents']:
            file_key = obj['Key']
            print(f"Checking file: {file_key}")

            # Get the content of the file
            file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)

            try:
                # Attempt to decode using UTF-8
                file_content = file_obj['Body'].read().decode('utf-8')
            except UnicodeDecodeError:
                try:
                    # Fallback to ISO-8859-1 if UTF-8 decoding fails
                    file_content = file_obj['Body'].read().decode('ISO-8859-1')
                except UnicodeDecodeError:
                    print(f"Skipping file {file_key} due to encoding issues.")
                    continue

            # Normalize the file content to lowercase and check for the substring
            if search_string_lower in file_content.lower():
                matching_files.append(file_key)

        return matching_files

    except (NoCredentialsError, PartialCredentialsError) as e:
        print("Credentials not available or invalid.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def main():
    if len(sys.argv) < 3:
        print("Usage: python s3filesearch.py <s3_bucket_name> <substring>")
        return

    bucket_name = sys.argv[1]
    substring = sys.argv[2]

    matching_files = search_files_in_s3(bucket_name, substring)

    if matching_files:
        print(f"Files containing the substring '{substring}':")
        for file_name in matching_files:
            print(file_name)
    else:
        print(f"No files found containing the substring '{substring}'.")

if __name__ == "__main__":
    main()
