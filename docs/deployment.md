# Public dashboard deployment

The dashboard defaults to fictional demonstration data. No public live feed is enabled. Users may upload a single authorized CSV snapshot; uploads are processed in the server session, not intentionally written to disk. Do not upload private or confidential data to a public deployment.

## Local
Install requirements, run python -m unittest discover -s tests -v, then streamlit run app.py.

## Community Cloud
Sign in at https://share.streamlit.io/ and connect GitHub. Create an app from samuel6183/alphascope-investment-intelligence, branch main, entrypoint app.py. Select Python 3.11 if available. Deploy and check demo data, upload validation and scenario calculation. Official guide: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## Before enabling public market feeds
Obtain appropriate provider redistribution rights, review financial regulatory obligations, add quote timestamps, provider failure handling, stablecoin classification and security/privacy controls. yfinance describes Yahoo data as intended for personal use. No software license was found at time of implementation; owner should choose one before inviting reuse. Public visibility alone is not an open-source license.
