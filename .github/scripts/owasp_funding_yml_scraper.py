import json
import os
import requests

GITHUB_API_URL = "https://api.github.com"
ORG_NAME = "OWASP"
ADDITIONAL_PROJECTS = [
    {"name": "Juice Shop", "repo_url": "https://github.com/bkimminich/juice-shop"},
    {"name": "MAS", "repo_url": "https://github.com/OWASP/owasp-masvs"},
    {"name": "BLT", "repo_url": "https://github.com/OWASP/BLT"},
    {"name": "SAMM", "repo_url": "https://github.com/OWASP/samm"},
    {"name": "CycloneDX", "repo_url": "https://github.com/CycloneDX/cyclonedx-cli"},
    {"name": "Dependency-Track", "repo_url": "https://github.com/DependencyTrack/dependency-track"},
    {"name": "Wrongsecrets", "repo_url": "https://github.com/OWASP/wrongsecrets"},
    {"name": "ModSecurity Core Rule Set", "repo_url": "https://github.com/coreruleset/coreruleset"},
    {"name": "ASVS", "repo_url": "https://github.com/OWASP/ASVS"},
    {"name": "OpenCRE", "repo_url": "https://github.com/OWASP/OpenCRE"}
]

def get_owasp_repos():
    url = f"{GITHUB_API_URL}/orgs/{ORG_NAME}/repos"
    repos = []
    while url:
        response = requests.get(url)
        response.raise_for_status()
        repos.extend(response.json())
        url = response.links.get('next', {}).get('url')
    return repos

def check_funding_file(repo_url):
    repo_name = '/'.join(repo_url.split('/')[-2:])
    funding_url = f'https://raw.githubusercontent.com/{repo_name}/master/.github/FUNDING.yml'
    response = requests.get(funding_url)
    print(f"Checking funding URL: {funding_url} - Status Code: {response.status_code}")
    if response.status_code == 200:
        return funding_url
    return None

# Fetch OWASP repos
owasp_repos = get_owasp_repos()
owasp_repos_data = [
    {"name": repo['name'], "repo_url": repo['html_url']}
    for repo in owasp_repos
]

# Combine OWASP repos and additional projects
data = owasp_repos_data + ADDITIONAL_PROJECTS

# Remove duplicates based on the 'repo_url' key
unique_data = {project['repo_url']: project for project in data}.values()

project_links = []

for project in unique_data:
    project_name = project['name']
    repo_url = project['repo_url']
    
    if project_name.startswith('www-'):
        print(f"Skipping repository: {project_name}")
        continue

    print("project name", project_name)
    funding_url = check_funding_file(repo_url)
    if funding_url:
        project_links.append({
            'project_name': project_name,
            'repo_url': repo_url,
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
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }
        header {
            background-color: #d9534f;
            color: white;
            padding: 10px 0;
            text-align: center;
        }
        header img {
            vertical-align: middle;
            margin-right: 10px;
        }
        header h1 {
            display: inline;
            font-size: 24px;
            vertical-align: middle;
        }
        main {
            padding: 20px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background-color: white;
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
        }
        .heart-icon {
            color: red;
            margin-left: 10px;
            text-decoration: none;
        }
        footer {
            text-align: center;
            padding: 20px;
            background-color: #d9534f;
            color: white;
        }
        footer a {
            color: white;
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header>
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Emoji_u1f345.svg/120px-Emoji_u1f345.svg.png" alt="Tomato" width="40" height="40">
        <h1>BLT Tomato - this is an OWASP BLT project created to help other OWASP projects.</h1>
    </header>
    <main>
        <p>The following OWASP projects are seeking funding and have a funding.yml file:</p>
        <ul>
"""

for project in project_links:
    html_content += f'<li><a href="{project["repo_url"]}">{project["project_name"]}</a> <a href="{project["funding_url"]}" class="heart-icon">&#10084;</a></li>\n'

html_content += """
        </ul>
    </main>
    <footer>
        <p><a href="https://github.com/OWASP-BLT/BLT-Tomato">View this script on GitHub</a></p>
    </footer>
</body>
</html>
"""

with open('index.html', 'w') as f:
    f.write(html_content)

print("index.html file has been created.")
