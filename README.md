# Boxing Match Analyst

AI-powered boxing match analysis tool using Google Gemini API.

## Features

- Upload boxing match videos or provide YouTube links
- AI analysis of:
  - Fighter habits
  - Telegraph movements before attacks
  - Defensive weaknesses
  - Strategic tips

## Setup

1. Clone the repository:
```bash
git clone https://github.com/mc-yonga/boxing.git
cd boxing/boxing-analyst
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Google Gemini API key
```

Get your API key from: https://makersuite.google.com/app/apikey

4. Run the application:
```bash
streamlit run app.py
```

## Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/mc-yonga/boxing)

### Manual Deployment Steps

1. Push your code to GitHub
2. Go to [Railway](https://railway.app/) and create a new project
3. Connect your GitHub repository
4. Add environment variable:
   - `GOOGLE_API_KEY`: Your Google Gemini API key
5. Railway will automatically detect and deploy using:
   - **Procfile** (simplest method) or
   - **Dockerfile** (more control)

Railway will automatically assign a PORT and make your app publicly accessible.

## Technology Stack

- Streamlit - Web interface
- Google Gemini 2.5 Flash - Video analysis AI
- yt-dlp - YouTube video download
- python-dotenv - Environment variable management

## License

MIT
