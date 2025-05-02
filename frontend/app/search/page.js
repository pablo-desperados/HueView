'use client';
import { useState } from 'react';
import { RgbColorPicker } from "react-colorful";
import axios from 'axios';

export default function Home() {
    const [color, setColor] = useState({ r: 255, g: 255, b: 255 });
    const [results, setResults] = useState([]);


  const search = async () => {
    console.log(color)
  };

  return (
    <div className="container py-4">
      <h1 className="mb-4">Color-Based Image Search</h1>

      <div className="row mb-3">
        
      </div>
        <RgbColorPicker color={color} onChange={setColor} />;
      <button className="btn btn-primary mb-4" onClick={search}>
        Search
      </button>

    </div>
  );
}