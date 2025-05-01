'use client';
import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [color, setColor] = useState({ r: 0, g: 0, b: 0 });
  const [results, setResults] = useState([]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setColor({ ...color, [name]: parseInt(value) });
  };

  const search = async () => {
    try {
      const { r, g, b } = color;
      const response = await axios.get('http://localhost:8000/search', {
        params: { r, g, b, threshold: 30 }
      });
      setResults(response.data);
    } catch (error) {
      console.error('Search error:', error);
    }
  };

  return (
    <div className="container py-4">
      <h1 className="mb-4">Color-Based Image Search</h1>

      <div className="row mb-3">
        {['r', 'g', 'b'].map((c) => (
          <div className="col" key={c}>
            <label className="form-label">{c.toUpperCase()}</label>
            <input
              type="number"
              className="form-control"
              name={c}
              min="0"
              max="255"
              value={color[c]}
              onChange={handleChange}
            />
          </div>
        ))}
      </div>

      <button className="btn btn-primary mb-4" onClick={search}>
        Search
      </button>

      <div>
        {results.length > 0 ? (
          results.map((img, idx) => (
            <div className="card mb-3" key={idx}>
              <img src={img.url} className="card-img-top" alt="search result" />
              <div className="card-body">
                <p><strong>Author:</strong> {img.author}</p>
                <p><strong>License:</strong> {img.license}</p>
                <p><strong>Tags:</strong> {img.tags.join(', ')}</p>
                <div
                  style={{
                    width: '50px',
                    height: '20px',
                    backgroundColor: `rgb(${img.dominant_color.join(',')})`,
                    border: '1px solid #000'
                  }}
                ></div>
              </div>
            </div>
          ))
        ) : (
          <p>No results yet.</p>
        )}
      </div>
    </div>
  );
}