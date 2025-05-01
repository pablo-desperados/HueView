'use client';
import 'bootstrap/dist/css/bootstrap.min.css';
import Image from "next/image";
import { useState } from 'react';
import Search from './search/page'




export default function Home() {
  const [showSearch, setShowSearch] = useState(false);

  if (showSearch) {
    return <Search/>;
  }

  return (
    <div className="d-flex flex-column justify-content-center align-items-center vh-100 text-center">
    <Image src="/HueView.svg" alt="Logo" width={600} height={400} />
    <h1 className="mb-4">Color-Based Image Search</h1>
      <button className="btn btn-primary btn-lg" onClick={() => setShowSearch(true)}>
          Enter
      </button>
  </div>
  );
}
