'use client';
import 'bootstrap/dist/css/bootstrap.min.css';
import Image from "next/image";
import { useRouter } from 'next/navigation';
import styles from "./page.module.css";
import Search from './search/page'



export default function Home() {
  const router = useRouter();
  const handleEnter=()=>{
    router.push('/search')
  }
  return (
    <div className="d-flex flex-column justify-content-center align-items-center vh-100 text-center">
    {/* Logo: Replace with actual SVG or <Image /> if using next/image */}
    <Image src="/HueView.svg" alt="Logo" width={600} height={400} />
    <h1 className="mb-4">Color-Based Image Search</h1>
    <button className="btn btn-primary btn-lg" onClick={handleEnter}>
      Enter
    </button>
  </div>
  );
}
