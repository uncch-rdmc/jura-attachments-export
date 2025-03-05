# jura-attachments-export

## Overview
This Python script automates the process of **exporting all attachments** from Jira issues using the **Jira REST API**. 

## Features  
**Filters by user** (assigned issues, reported issues)  
**Filters by file type** (e.g., `.pdf`, `.csv`, `.jpg`)  
**Tracks total issues checked & total files downloaded**  


## 🔧 Prerequisites
Before running the script, ensure you have:
- **Python 3.x** installed
- A **Jira API token** (🔗 [Generate API Token](https://id.atlassian.com/manage-profile/security/api-tokens))
- Jira **read permissions** for issues & attachments
- The following Python package installed:
  ```sh
  pip install requests
  pip install base64
