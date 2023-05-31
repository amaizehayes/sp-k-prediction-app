from git import Repo

def pull_changes(repo_path):
    try:
        # Open the repository
        repo = Repo(repo_path)

        # Pull the latest changes from the remote repository
        origin = repo.remote(name='origin')
        origin.pull()

        print("Changes pulled successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# Example usage
repo_path = '/home/amaizehayes/sp-k-prediction-app'  # Replace with the path to your repository

pull_changes(repo_path)