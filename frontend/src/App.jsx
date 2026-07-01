import { useState } from "react";
import Navbar from "./components/Navbar.jsx";
import Hero from "./components/Hero.jsx";
import StatsBar from "./components/StatsBar.jsx";

const MODES = ["TRADITIONAL RAG", "COMPRESSED RAG"];

export default function App() {
  const [mode, setMode] = useState(MODES[1]);
  const [metrics, setMetrics] = useState(null);

  return (
    <div className="flex min-h-screen w-full items-center justify-center bg-gradient-to-br from-black via-night-soft to-brand-700/40 p-3 sm:p-5 lg:p-7">
      {/* Inner framed canvas */}
      <div className="relative mx-auto w-full max-w-[1320px] overflow-hidden rounded-[28px] bg-gradient-to-br from-night via-night-soft to-[#062b3a] shadow-[0_30px_80px_-30px_rgba(6,182,212,0.4)] ring-1 ring-white/10">
        {/* Decorative soft glows */}
        <div className="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full bg-brand-500/30 blur-3xl" />
        <div className="pointer-events-none absolute -bottom-24 left-1/3 h-72 w-72 rounded-full bg-accent/25 blur-3xl" />

        <div className="relative z-10 px-5 pb-6 pt-5 sm:px-8 lg:px-12">
          <Navbar mode={mode} setMode={setMode} modes={MODES} />
          <Hero mode={mode} onMetrics={setMetrics} />
          <StatsBar metrics={metrics} />
        </div>
      </div>
    </div>
  );
}
