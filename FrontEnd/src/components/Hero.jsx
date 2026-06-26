import { Github } from "lucide-react";
import OrbitSphere from "./OrbitSphere.jsx";
import ChatCard from "./ChatCard.jsx";

export default function Hero({ mode, onMetrics }) {
  return (
    <section className="relative grid grid-cols-1 items-center gap-10 pt-6 lg:grid-cols-2 lg:pt-8">
      {/* Left column */}
      <div className="relative z-20">
        {/* Headline */}
        <h1 className="text-5xl font-extrabold leading-[1.05] tracking-tight text-white sm:text-6xl">
          Smart{" "}
          <span className="bg-gradient-to-r from-brand-400 to-accent bg-clip-text text-transparent">
            Compliance
          </span>{" "}
          Assistant with{" "}
          <span className="bg-gradient-to-r from-brand-400 to-accent bg-clip-text text-transparent">
            Advanced RAG
          </span>{" "}
          System
        </h1>

        {/* Three-line project intro */}
        <p className="mt-5 max-w-md text-base leading-relaxed text-slate-400">
          A Retrieval-Augmented Generation chatbot built for complex financial
          and operational resilience regulations.
          <br />
          It answers compliance-based queries with grounded, citation-backed
          responses you can trust.
          <br />
          Just ask in plain language and get precise answers in seconds.
        </p>

        {/* CTA */}
        <div className="mt-8 flex flex-wrap items-center gap-4">
          <a
            href="https://github.com/RahulJoshvaa/RAG-compliance-chatbot"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="View on GitHub"
            className="flex items-center gap-2 rounded-full bg-gradient-to-r from-brand-400 to-accent px-8 py-3.5 text-sm font-semibold text-white shadow-xl shadow-brand-500/30 transition-transform hover:scale-[1.03] active:scale-95"
          >
            <Github className="h-5 w-5" />
            GitHub
          </a>
        </div>
      </div>

      {/* Right column — sphere + floating chat card */}
      <div className="relative h-[420px] sm:h-[480px] lg:h-[520px]">
        <OrbitSphere />
        <div className="absolute -bottom-6 left-1/2 z-30 w-[92%] max-w-md -translate-x-1/2 lg:left-8 lg:w-[125%] lg:max-w-xl lg:translate-x-0">
          <ChatCard mode={mode} onMetrics={onMetrics} />
        </div>
      </div>
    </section>
  );
}
