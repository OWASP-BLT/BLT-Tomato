import json
import re
import requests
from bs4 import BeautifulSoup

def extract_github_links(url, project_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    
    github_links = set()
    for link in links:
        match = re.match(r'https://github\.com/[^/]+/[^/#]+', link['href'].lower())
        if match and project_name.lower() not in link['href'].lower():
            github_links.add(match.group(0))
    
    return list(github_links)

def check_funding_file(repo_url):
    owner_repo = '/'.join(repo_url.split('/')[-2:])
    funding_url = f'https://raw.githubusercontent.com/{owner_repo}/main/.github/FUNDING.yml'
    response = requests.get(funding_url)
    return response.status_code == 200

with open('www_project_repos.json', 'r') as f:
    data = json.load(f)

project_links = []

for project in data:
    print("project name", project['name'])
    project_name = project['name']
    github_url = project['html_url'].replace('github.com/OWASP/', 'owasp.org/')

    repo_links = extract_github_links(github_url, project_name)
    if repo_links:  # Only append projects with GitHub links
        project_repos = []
        for repo in repo_links:
            funding_exists = check_funding_file(repo)
            project_repos.append({
                'repo_url': repo,
                'funding_file': funding_exists
            })
        project_links.append({
            'project_name': project_name,
            'repos': project_repos
        })

with open('project_repos_links.json', 'w') as f:
    json.dump(project_links, f, indent=2)
