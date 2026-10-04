# GitHub + Streamlit deployment

## GitHub web UI
1. GitHub → New repository → name it `seo-premium-agent`.
2. Create the repository.
3. Add file → Upload files.
4. Upload all files/folders from this package.
5. Commit changes.
6. Confirm `app.py` and `requirements.txt` are in the repository root.

## Streamlit Community Cloud
1. Open Streamlit Community Cloud and sign in with GitHub.
2. Connect/authorize GitHub.
3. Create app.
4. Select your repository, branch `main`, and file `app.py`.
5. Deploy.
6. Wait for dependency installation and app startup.

Streamlit Community Cloud uses the repository as the source; later GitHub commits update the deployed app. A `requirements.txt` file should be in the repository root or alongside the entrypoint.

## Groq key
The current UI accepts a Groq API key in the sidebar and keeps it in Streamlit session state only. Never put the key in source code or commit it to GitHub.

For production, a safer next step is to use Streamlit Secrets and remove manual key entry.
