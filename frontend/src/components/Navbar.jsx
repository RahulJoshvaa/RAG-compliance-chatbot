import { Sparkles } from "lucide-react";

export default function Navbar({ mode, setMode, modes }) {
  return (
    <header className="flex items-center justify-between py-2">
      {/* Brand */}
      <a href="#" className="flex items-center gap-2.5">
        <span className="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-brand-300 via-brand-500 to-accent shadow-md shadow-brand-500/30">
          <Sparkles className="h-4.5 w-4.5 text-white" strokeWidth={2.2} />
        </span>
        <span className="text-xl font-bold tracking-tight text-white">
          AXIOM
        </span>
      </a>

      {/* RAG mode toggle — sits at the top, directly above the chat box */}
      <div
        role="tablist"
        aria-label="Retrieval mode"
        className="relative flex items-center rounded-full bg-white/5 p-1 ring-1 ring-white/10 backdrop-blur"
      >
        <span
          className="absolute top-1 bottom-1 w-1/2 rounded-full bg-gradient-to-r from-brand-400 to-accent shadow-md shadow-brand-500/40 transition-transform duration-300 ease-out"
          style={{
            transform:
              mode === modes[1] ? "translateX(100%)" : "translateX(0%)",
          }}
        />
        {modes.map((m) => (
          <button
            key={m}
            role="tab"
            aria-selected={mode === m}
            onClick={() => setMode(m)}
            className={`relative z-10 rounded-full px-4 py-1.5 text-xs font-semibold tracking-wide transition-colors duration-200 sm:px-5 ${
              mode === m ? "text-white" : "text-slate-400 hover:text-brand-300"
            }`}
          >
            {m}
          </button>
        ))}
      </div>
    </header>
  );
}
