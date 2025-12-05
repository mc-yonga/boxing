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

## Technology Stack

- Streamlit - Web interface
- Google Gemini 2.5 Flash - Video analysis AI
- yt-dlp - YouTube video download
- python-dotenv - Environment variable management

## License

MIT
