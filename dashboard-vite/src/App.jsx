import React, { useState, useEffect, useCallback } from "react";

const PAGE_SIZE = 10;

export default function Dashboard() {
  const [videos, setVideos] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [inputValue, setInputValue] = useState(""); 
  const [sort, setSort] = useState("asc");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const fetchVideos = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        page: page.toString(),
        page_size: PAGE_SIZE.toString(),
        search,
        sort,
      });

      const res = await fetch(`http://localhost:8000/videos?${params.toString()}`);

      if (!res.ok) {
        throw new Error(`Error: ${res.status} ${res.statusText}`);
      }

      const data = await res.json();
      console.log("Backend response:", data);

      if (Array.isArray(data.videos)) {
        setVideos(data.videos);
        setTotal(data.total ?? data.videos.length);
      } else if (Array.isArray(data)) {
        setVideos(data);
        setTotal(data.length);
      } else {
        setVideos([]);
        setTotal(0);
      }
    } catch (err) {
      setError(err.message);
      setVideos([]);
      setTotal(0);
    }

    setLoading(false);
  }, [page, search, sort]);
  useEffect(() => {
    fetchVideos();
  }, [fetchVideos]);
  useEffect(() => {
    const handler = setTimeout(() => {
      setSearch(inputValue);
      setPage(1);
    }, 500); 

    return () => clearTimeout(handler);
  }, [inputValue]);

  const totalPages = Math.ceil(total / PAGE_SIZE);

  return (
    <div style={{ maxWidth: 900, margin: "auto", padding: 20 }}>
      <h1>Video Dashboard</h1>

      <div style={{ marginBottom: 20 }}>
        <input
          type="text"
          placeholder="Search videos (e.g., cricket, music)"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          style={{ width: 300, padding: 8, fontSize: 16 }}
        />
        <select
          value={sort}
          onChange={(e) => setSort(e.target.value)}
          style={{ marginLeft: 10, padding: 8 }}
        >
          <option value="asc">Sort by Published Date Asc</option>
          <option value="desc">Sort by Published Date Desc</option>
        </select>
      </div>

      {loading && <p>Loading videos...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {!loading && !error && videos.length === 0 && (
        <p>No videos found for "{search}"</p>
      )}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {videos.map((video) => (
          <li
            key={video.id || video.videoId || video.snippet?.resourceId?.videoId}
            style={{
              border: "1px solid #ccc",
              borderRadius: 8,
              padding: 16,
              marginBottom: 12,
            }}
          >
            <h3>{video.title || video.snippet?.title || "No Title"}</h3>
            <p>{video.description || video.snippet?.description || "No description"}</p>
            <p>
              Published:{" "}
              {new Date(
                video.publishedAt ||
                  video.published_datetime ||
                  video.snippet?.publishedAt
              ).toLocaleString()}
            </p>
            {video.thumbnails?.medium?.url && (
              <img
                src={video.thumbnails.medium.url}
                alt={video.title}
                style={{ width: 320, borderRadius: 6 }}
              />
            )}
            <br />
            <a
              href={`https://www.youtube.com/watch?v=${video.id || video.videoId || video.snippet?.resourceId?.videoId}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              Watch on YouTube
            </a>
          </li>
        ))}
      </ul>

      {/* Pagination controls */}
      {totalPages > 1 && (
        <div style={{ marginTop: 20 }}>
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
          >
            Prev
          </button>
          <span style={{ margin: "0 10px" }}>
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
