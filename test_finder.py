import pytest
from unittest.mock import MagicMock
from github_email_finder import match_dict, git_repos

# ---------------------------------------------------------
# 1. Testing the logic function (match_dict) 
# ---------------------------------------------------------
def test_match_dict():
    input_data = [("foo", "foo@example.com"), ("foo", "foo@example.com"), ("bar", "bar@example.com")]
    expected = [("foo", "foo@example.com"), ("bar", "bar@example.com")]
    
    result = match_dict(input_data)
    assert sorted(result) == sorted(expected)

# ---------------------------------------------------------
# 2. Testing repository operations using a mock GitHub API
# ---------------------------------------------------------
def test_get_commit_emails_success():
    git = git_repos(username="testuser", link=None, token=None, fork=False, deep=3)
    
    mock_commit1 = MagicMock()
    mock_commit1.commit.author.name = "Author One"
    mock_commit1.commit.author.email = "one@example.com"
    
    mock_commit2 = MagicMock()
    mock_commit2.commit.author.name = "Author Two"
    mock_commit2.commit.author.email = "two@example.com"
    
    dummy_commits_list = [mock_commit1, mock_commit2]

    mock_get_commits = MagicMock()
    mock_get_commits.totalCount = 2
    mock_get_commits.__getitem__.return_value = dummy_commits_list

    mock_repo = MagicMock()
    mock_repo.fork = False
    mock_repo.get_commits.return_value = mock_get_commits

    from github.Repository import Repository
    mock_repo.__class__ = Repository

    result = git.get_commit_emails(mock_repo)

    expected = [("Author One", "one@example.com"), ("Author Two", "two@example.com")]
    assert sorted(result) == sorted(expected)


def test_get_commit_emails_skip_fork():
    git = git_repos(username="testuser", link=None, token=None, fork=False, deep=3)
    
    mock_repo = MagicMock()
    mock_repo.fork = True
    
    from github.Repository import Repository
    mock_repo.__class__ = Repository

    result = git.get_commit_emails(mock_repo)
    assert result is None

# ---------------------------------------------------------
# 3. Exception Handling (Abnormal Scenario) Testing
# ---------------------------------------------------------
from github_email_finder import NotFoundError

def test_get_Users_Public_repos_user_not_found():
    git = git_repos(username="non_existent_user", link=None, token=None, fork=False, deep=3)
    
    git.g = MagicMock()
    git.g.get_user.side_effect = Exception("GitHub API Error: User not found")

    with pytest.raises(NotFoundError) as exc_info:
        git.get_Users_Public_repos()
        
    assert "User non_existent_user not found." in str(exc_info.value)


def test_get_commit_emails_api_error_handling():
    git = git_repos(username="testuser", link=None, token=None, fork=False, deep=3)
    
    mock_repo = MagicMock()
    mock_repo.fork = False
    
    mock_repo.get_commits.side_effect = Exception("API rate limit exceeded")
    
    from github.Repository import Repository
    mock_repo.__class__ = Repository

    result = git.get_commit_emails(mock_repo)
    
    assert result == []
