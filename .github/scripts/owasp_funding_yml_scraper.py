import json
import os
import requests

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

def check_funding_file(repo_name):
    funding_url = f'https://raw.githubusercontent.com/{ORG_NAME}/{repo_name}/master/.github/FUNDING.yml'
    response = requests.get(funding_url)
    print(f"Checking funding URL: {funding_url} - Status Code: {response.status_code}")
    if response.status_code == 200:
        return funding_url
    return None

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
    if project_name.startswith('www-'):
        print(f"Skipping repository: {project_name}")
        continue

    print("project name", project_name)
    repo_name = project_name
    funding_url = check_funding_file(repo_name)
    if funding_url:
        project_links.append({
            'project_name': project_name,
            'repo_url': project['html_url'],
            'funding_url': funding_url
        })
        print(f"Added project: {project_name} with funding URL: {funding_url}")

# Write the JSON output file
output_file = 'project_repos_links.json'
with open(output_file, 'w') as f:
    json.dump(project_links, f, indent=2)

print(f"Output written to '{output_file}'")

# Generate the index.html file
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BLT Tomato - OWASP Projects Seeking Funding</title>
    <style>
        .heart-icon {
            color: red;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <h1>BLT Tomato - this is an OWASP BLT project created to help other OWASP projects.</h1>
    <p>The following OWASP projects are seeking funding and have a funding.yml file:</p>
    <ul>
"""

for project in project_links:
    html_content += f'<li><a href="{project["repo_url"]}">{project["project_name"]}</a> <a href="{project["funding_url"]}" class="heart-icon">&#10084;</a></li>\n'

html_content += """
    </ul>
</body>
</html>
"""

with open('index.html', 'w') as f:
    f.write(html_content)

print("index.html file has been created.")
