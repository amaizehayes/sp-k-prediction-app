from git import Repo
from datetime import date, datetime

today = date.today().strftime("%A, %B %d, %Y")

def commit_and_push(repo_path, commit_message):
    try:
        # Open the repository
        repo = Repo(repo_path)

        # Add all changes to the staging area
        repo.index.add('*')

        # Commit the changes
        repo.index.commit(commit_message)

        # Push the changes to the remote repository
        origin = repo.remote(name='origin')
        origin.push()

        print("Changes committed and pushed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Example usage
repo_path = '/home/amaizehayes/sp-k-prediction-app'  # Replace with the path to your repository
commit_message = f'Data for {today}'

commit_and_push(repo_path, commit_message)
