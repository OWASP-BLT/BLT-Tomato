import json
import re
import os
import requests
from bs4 import BeautifulSoup

GITHUB_API_URL = "https://api.github.com"
ORG_NAME = "OWASP"

def get_owasp_repos():
    url = f"{GITHUB_API_URL}/orgs/{ORG_NAME}/repos"
    repos = []
    while url:
        response = requests.get(url)
        response.raise_for_status()
        repos.extend(response.json())
        url = response.links.get('next', {}).get('url')
    return repos

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

def check_funding_file(repo_name):
    funding_url = f'https://raw.githubusercontent.com/{ORG_NAME}/{repo_name}/master/.github/FUNDING.yml'
    response = requests.get(funding_url)
    return response.status_code == 200

file_path = 'www_project_repos.json'
default_data = get_owasp_repos()

if not os.path.exists(file_path):
    with open(file_path, 'w') as f:
        json.dump(default_data, f, indent=2)
    print(f"The file '{file_path}' did not exist and has been created with default data. Please update it with your project information.")

with open(file_path, 'r') as f:
    data = json.load(f)

project_links = []

for project in data:
    project_name = project['name']
    print("project name", project_name)
    github_url = project['html_url']
    
    repo_links = extract_github_links(github_url, project_name)
    if repo_links:  # Only append projects with GitHub links
        project_repos = []
        for repo in repo_links:
            funding_exists = check_funding_file(repo.split('/')[-1])
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
