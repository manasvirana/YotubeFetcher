# YouTube Video Fetcher & Dashboard

## Overview

This project consists of two parts:

1. **Backend**: A FastAPI-based service that continuously fetches YouTube videos for a search query using rotating API keys, stores videos in PostgreSQL.

2. **Frontend**: A React + Vite dashboard that fetches video data from the backend and displays it with pagination, search, and sorting.

---

## Backend - YouTube Video Fetcher API

### Features

- Background fetching every 10 seconds with multiple API keys and rotation.
- Stores video metadata in PostgreSQL.
- REST GET API `/videos` supporting pagination and sorting.
- Built with FastAPI, SQLAlchemy (async), asyncpg, and httpx.

### Technologies

- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0 (async)
- httpx
- python-dotenv
- Uvicorn

---

## Frontend - React + Vite Dashboard

### Features

- Fetches videos from backend API.
- Pagination (10 videos per page).
- Search with debounce.
- Sort videos by published date.
- Displays video info and thumbnails.

### Technologies

- React 18+
- Vite
- Fetch API

---

---

## Screenshots

### Backend API

![Backend API Screenshot for Football](https://github.com/user-attachments/assets/59e5efe4-0c98-4fb8-a482-21d9c05c06ac)

![Backend API Screenshot for Cricket](https://github.com/user-attachments/assets/621d8e08-fdd9-4eb3-8877-5ebcc2b74a1b)

### Frontend Dashboard - Cricket Videos

![Cricket Dashboard Screenshot](https://github.com/user-attachments/assets/dd8cdc64-a397-4824-9b80-025324cbd2c9)


### Frontend Dashboard - Football Videos

![Football Dashboard Screenshot](https://github.com/user-attachments/assets/a3a31393-00dc-42a8-8fe6-381a101fbcf9)

![Football Dashboard Screenshot](https://github.com/user-attachments/assets/f9de16ef-4ad3-4fc7-964f-fed3615c31c4)

### Database 

![Database](https://github.com/user-attachments/assets/f0973f91-b332-42c1-b20a-13cdc76ddc2d)



---


## Project Structure

| Folder / File           | Description                                      |
|------------------------|------------------------------------------------|
| `backend/`             | FastAPI backend source code                      |
| `frontend/`            | React + Vite frontend source code                |

---

## Setup Instructions

### Prerequisites

- Python 3.10+
- PostgreSQL running locally or remotely
- Git installed
- YouTube Data API v3 keys
- Node.js and npm/yarn (for frontend React)

---

Sure! Here’s the entire backend setup section **ready to copy-paste as Markdown code** inside your `README.md` file:

### Backend Setup
````markdown
1. Clone the repo and navigate to the backend folder:

Open your command prompt or terminal and run:

git clone https://github.com/manasvirana/YotubeFetcher.git
````

2. Create and activate a Python virtual environment:

* **On Windows:**

Open your command prompt and run:

```bash
python -m venv venv
.\venv\Scripts\activate
```

* **On macOS/Linux:**

Open your terminal and run:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install backend dependencies:

Run the following command:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the backend directory with the following content:

```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
YOUTUBE_API_KEY=
FETCH_INTERVAL=10
```

5. Make sure PostgreSQL is running and the database exists.

6. Run the backend server with this command:

```bash
uvicorn server.main:app --reload
```

7. The backend API will be available at: [http://localhost:8000](http://localhost:8000)



### Frontend Setup
````markdown
1. Navigate to the frontend folder:

Open your command prompt or terminal and run:

cd dashboard-vite
````

2. Install Node.js dependencies:

Make sure you have **Node.js** and **npm** installed. Then run:

```bash
npm install
```


3. Start the React development server:

```bash
npm run dev
```

4. The frontend dashboard will be available at: [http://localhost:5173](http://localhost:5173) (or the port shown in your terminal)

---

**Note:** The frontend fetches video data from the backend API, so make sure your backend server is running at `http://localhost:8000`.



## Project Structure
```markdown
FamPay/
├── server/                  # Backend FastAPI source code
│   ├── **pycache**/         # Python cache files (should be gitignored)
│   ├── api.py               # API route definitions
│   ├── crud.py              # Database CRUD operations
│   ├── database.py          # DB connection and session management
│   ├── main.py              # FastAPI app initialization and startup
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── utils.py             # Helper functions and API key rotation
│   ├── youtube_fetcher.py   # Background video fetcher task
├── dashboard-vite/          # Frontend React + Vite source code
│   ├── public/              # Static assets
│   ├── src/                 # React components and pages
│   ├── index.html           # Main HTML file
│   ├── package.json         # Frontend dependencies and scripts
│   ├── vite.config.js       # Vite config file                
├── README.md                # Project documentation
├── .gitignore               # Git ignore rules
└── .env
└── .requirements.txt

```

---

## API Documentation

This project uses the YouTube Data API v3 to fetch video data.

### API References

- YouTube Data API v3:  
  https://developers.google.com/youtube/v3/getting-started

- Search API Reference:  
  https://developers.google.com/youtube/v3/docs/search/list

### Sample JSON Response

Here is an example of the JSON structure returned by the YouTube Search API, showing key fields stored in the database:

```json
{
  "kind": "youtube#searchListResponse",
  "etag": "etag-value",
  "items": [
    {
      "kind": "youtube#searchResult",
      "etag": "etag-value",
      "id": {
        "kind": "youtube#video",
        "videoId": "abcd1234"
      },
      "snippet": {
        "publishedAt": "2023-05-01T12:00:00Z",
        "channelId": "channelId123",
        "title": "Sample Video Title",
        "description": "This is a sample description of the video.",
        "thumbnails": {
          "default": {
            "url": "https://i.ytimg.com/vi/abcd1234/default.jpg",
            "width": 120,
            "height": 90
          },
          "medium": {
            "url": "https://i.ytimg.com/vi/abcd1234/mqdefault.jpg",
            "width": 320,
            "height": 180
          },
          "high": {
            "url": "https://i.ytimg.com/vi/abcd1234/hqdefault.jpg",
            "width": 480,
            "height": 360
          }
        },
        "channelTitle": "Channel Name"
      }
    }
  ]
}
















  
