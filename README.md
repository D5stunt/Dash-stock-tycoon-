# Dash Stock Tycoon V12 — Python Edition

A fake-money stock trading game made with Python and Streamlit. Prices are simulated, not live market data.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publish for mobile
1. Create a GitHub repository and upload `app.py`, `requirements.txt`, and this README.
2. Sign into [Streamlit Community Cloud](https://share.streamlit.io/), select **Create app**, and connect the GitHub repository.
3. Set the main file path to `app.py` and deploy.
4. Open the resulting URL on iPhone, iPad, Android, or desktop.

GitHub Pages alone cannot run Python server code. Streamlit Community Cloud hosts the Python app. Progress is session-only; persistent accounts and real quotes would need additional services.
