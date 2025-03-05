import requests
import json
import os
import base64 # Encode your Jira API credentials

JIRA_URL = "https://uncch-rdmc.atlassian.net"
API_TOKEN = "your_token"
EMAIL = "your_email"

# Encode authentication
auth_string = f"{EMAIL}:{API_TOKEN}"
b64_auth = base64.b64encode(auth_string.encode()).decode()
headers = {
    "Authorization": f"Basic {b64_auth}",
    "Accept": "application/json"
}

# Create a folder for attachments
os.makedirs("jira_attachments", exist_ok=True)

# Initialize counters
total_issues_checked = 0  
total_downloaded = 0  

# Optional: Customize JQL Filters
ASSIGNED_TO_ME = False  # Set to True to fetch only your assigned issues
CREATED_BY_ME = False   # Set to True to fetch only issues you reported
FILE_EXTENSIONS = []  # Example: ['pdf', 'csv', 'jpg'] (Leave empty for all files)

# Construct JQL Query
jql_query = "issuetype IS NOT EMPTY"
if ASSIGNED_TO_ME:
    jql_query += " AND assignee = currentUser()"
if CREATED_BY_ME:
    jql_query += " AND reporter = currentUser()"

# Pagination variables
start_at = 0
max_results = 100  # Jira's max limit per request

while True:
    # Construct the API URL with dynamic JQL query
    search_url = f"{JIRA_URL}/rest/api/3/search?jql={jql_query}&fields=attachment&startAt={start_at}&maxResults={max_results}"
    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print("Error fetching issues:", response.json())
        break

    issues = response.json().get("issues", [])

    # Stop when no more issues are returned
    if not issues:
        break

    for issue in issues:
        total_issues_checked += 1  # Increment issue counter
        print(f"Checking issue: {issue['key']}")

        for attachment in issue.get("fields", {}).get("attachment", []):
            filename = attachment["filename"]
            file_url = attachment["content"]

            # Filter by file extension if specified
            if FILE_EXTENSIONS:
                if not any(filename.lower().endswith(ext) for ext in FILE_EXTENSIONS):
                    print(f"Skipping {filename} (does not match file types {FILE_EXTENSIONS})")
                    continue  # Skip downloading this file

            print(f"Attachment found: {filename} - {file_url}")

            # Download the file
            try:
                file_response = requests.get(file_url, headers=headers, stream=True)
                if file_response.status_code == 200:
                    file_path = os.path.join("jira_attachments", filename)
                    with open(file_path, "wb") as file:
                        for chunk in file_response.iter_content(chunk_size=1024):
                            file.write(chunk)
                    
                    # Confirm file was saved correctly
                    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                        print(f"Successfully saved: {file_path}")
                        total_downloaded += 1  # Increment file counter
                    else:
                        print(f"ERROR: {filename} not saved properly.")
                else:
                    print(f"ERROR: Failed to download {filename}, Status Code: {file_response.status_code}")

            except Exception as e:
                print(f"Error downloading {filename}: {e}")

    # Move to the next batch of issues
    start_at += max_results

# Print the total counts at the end
print("Download complete.")
print(f"Total issues checked: {total_issues_checked}")
print(f"Total files downloaded: {total_downloaded}")