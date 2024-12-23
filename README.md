# University Subtitle RAG System

This application uses a Retrieval-Augmented Generation (RAG) system to allow users to query relevant university lecture subtitles and retrieve accurate timestamped information. The data is scraped from publicly available university subtitle files, and the system leverages the power of generative models to provide specific and relevant information in response to user queries.

## Features
- **Scraped Data**: The system scrapes subtitles from university lecture videos to gather relevant textual data.
- **RAG System**: Uses a Retrieval-Augmented Generation model to find the most relevant parts of the lecture subtitle data based on a user’s query.
- **Timestamped Results**: Returns results with the specific timestamps for the relevant segments in the lecture video.
- **FastAPI Backend**: A robust and lightweight backend built using FastAPI to handle user queries and responses.
- Streamlit Frontend: A simple, interactive frontend built using Streamlit for an easy-to-use interface.

## Tech Stack
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Database**: ChromaDB, SQLModel
- **Web Scraping**: Selenium
- **Generative Models**: Geminis models for the RAG system
- **Containerization**: Docker (for deployment)
- **Deployment**: Render

## Getting Started

# Prerequisites
- Python 3.10
- Docker (for containerization)

# Installation
1. Clone the repository:
```
git clone https://github.com/AviTirto/KalturaWebSearchSystem.git
cd KalturaSearchSystem
```

2. Set up a virtual environment (optional but recommended)::
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the dependencies:
```
pip install -r requirements.txt
```

4. Set Up Enviorment Variables
```
LOCAL_SRT_PATH="your_srt_path
LOCAL_DB_PATH=your_local_db_path
GOOGLE_API_KEY=your_google_api_key
GEMINI_API_KEY=your_gemini_api_key
```

# Running Locally
1. Start the FastAPI server:
```
cd app
uvicorn server:app --reload
```

2. Start the Streamlit frontend:
```
streamlit run notebook.py
```

# Docker
1. Build the Docker image::
```
docker build -t university-subtitle-rag-system .
```

2. Run the container:
```
docker run -p 8000:8000 --env-file .env university-subtitle-rag-system
```

## How It Works
1. **Scraping**: The application scrapes subtitles from publicly available university lecture videos using Selenium. The scraped data is stored in a database (ChromaDB or SQLModel).
2. **Querying**: When a user submits a query via the Streamlit frontend, the FastAPI backend processes the request and uses a RAG system to retrieve relevant subtitle data from the database.
3. **Response**: The system returns timestamped sections of the lecture that are most relevant to the query, enabling users to jump to the exact part of the lecture video.

## Deployment
The application can be deployed on platforms like Render or any other cloud service that supports Docker.

### Deployment on Render
1. Create a new Web Service on Render.
2. Link the service to your Git repository.
3. Set the Dockerfile as the build configuration.
4. Add environment variables through Render’s dashboard (e.g., GOOGLE_API_KEY, GEMINI_API_KEY).
5. Render will automatically build and deploy your container.

## Acknowledgments
- **FastAPI**: Fast, modern web framework for building APIs with Python 3.8+.
- **Streamlit**: A great tool for building interactive frontends for machine learning apps.
- **Selenium**: Used to scrape subtitles from university lecture videos.
- **ChromaDB**: Used for efficient data storage and retrieval.
- **Geminis Models**: Leveraged for the RAG system to provide relevant responses.


