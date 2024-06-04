import json
import re
import os
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

file_path = 'www_project_repos.json'
default_data = [
    {
        "name": "Sample Project",
        "html_url": "https://github.com/OWASP/SampleProject"
    }
]

if not os.path.exists(file_path):
    with open(file_path, 'w') as f:
        json.dump(default_data, f, indent=2)
    print(f"The file '{file_path}' did not exist and has been created with default data. Please update it with your project information.")

with open(file_path, 'r') as f:
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

output_file = 'project_repos_links.json'
with open(output_file, 'w') as f:
    json.dump(project_links, f, indent=2)

print(f"Output written to '{output_file}'")
