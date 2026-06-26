import { useState, useRef, useEffect } from "react";
import { SendHorizonal, Loader2, FileText } from "lucide-react";
import { sendChat } from "../api.js";

export default function ChatCard({ mode, onMetrics }) {
  const [messages, setMessages] = useState([]);
  const [value, setValue] = useState("");
  const [loading, setLoading] = useState(false);
  const [streaming, setStreaming] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, loading]);

  // Reveal the answer progressively, like a live token stream.
  function streamAnswer(full, sources, live, notice) {
    return new Promise((resolve) => {
      // tokens that keep the whitespace so spacing is preserved
      const tokens = full.match(/\S+\s*/g) || [full];

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "",
          sources: [],
          live,
          notice,
          streaming: true,
        },
      ]);

      let i = 0;
      let acc = "";

      const tick = () => {
        acc += tokens[i];
        i += 1;

        setMessages((prev) => {
          const copy = [...prev];
          const last = copy.length - 1;
          copy[last] = { ...copy[last], text: acc };
          return copy;
        });

        if (i < tokens.length) {
          setTimeout(tick, 18);
        } else {
          // finished — attach sources and stop the cursor
          setMessages((prev) => {
            const copy = [...prev];
            const last = copy.length - 1;
            copy[last] = { ...copy[last], sources, streaming: false };
            return copy;
          });
          resolve();
        }
      };

      tick();
    });
  }

  async function handleSend(e) {
    e.preventDefault();
    const q = value.trim();
    if (!q || loading || streaming) return;

    setMessages((prev) => [...prev, { role: "user", text: q }]);
    setValue("");
    setLoading(true);

    try {
      const data = await sendChat(q, mode);
      if (data.metrics) onMetrics?.(data.metrics);

      setLoading(false);
      setStreaming(true);
      await streamAnswer(
        data.answer,
        data.sources || [],
        data.live,
        data.notice
      );
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: `Couldn't reach the backend: ${err.message}. Is the API running on port 8000?`,
          error: true,
        },
      ]);
    } finally {
      setLoading(false);
      setStreaming(false);
    }
  }

  const busy = loading || streaming;

  return (
    <div className="rounded-2xl p-3 ring-2 ring-brand-400/70">
      {/* Conversation — answer on the left, query on the right */}
      <div
        ref={scrollRef}
        className="no-scrollbar flex max-h-[380px] min-h-28 flex-col gap-3 overflow-y-auto px-1 py-2"
      >
        {messages.length === 0 && !loading ? (
          <div className="flex flex-1 items-center justify-center text-center text-xs text-slate-500">
            Ask a compliance question to start the conversation.
          </div>
        ) : (
          messages.map((m, i) => (
            <div
              key={i}
              className={`flex ${
                m.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-3.5 py-2 text-xs leading-relaxed ${
                  m.role === "user"
                    ? "rounded-tr-sm bg-white/10 text-slate-200 ring-1 ring-white/10"
                    : m.error
                    ? "rounded-tl-sm bg-red-500/15 text-red-200 ring-1 ring-red-400/30"
                    : m.notice === "api_limit"
                    ? "rounded-tl-sm bg-amber-500/15 text-amber-100 ring-1 ring-amber-400/30"
                    : "rounded-tl-sm bg-gradient-to-br from-brand-500 to-accent text-white shadow-md shadow-brand-500/20"
                }`}
              >
                <p className="whitespace-pre-wrap">
                  {m.text}
                  {m.streaming && (
                    <span className="ml-0.5 inline-block animate-pulse">▋</span>
                  )}
                </p>

                {/* Source citations */}
                {m.sources?.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-1.5 border-t border-white/20 pt-2">
                    {m.sources.map((s, j) => (
                      <span
                        key={j}
                        className="inline-flex items-center gap-1 rounded-full bg-black/20 px-2 py-0.5 text-[10px] font-medium text-white/90"
                      >
                        <FileText className="h-2.5 w-2.5" />
                        {s.source}
                        {s.page != null ? ` · p.${s.page}` : ""}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))
        )}

        {/* Thinking indicator */}
        {loading && (
          <div className="flex justify-start">
            <div className="flex items-center gap-2 rounded-2xl rounded-tl-sm bg-white/10 px-3.5 py-2 text-xs text-slate-300 ring-1 ring-white/10">
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
              Thinking…
            </div>
          </div>
        )}
      </div>

      {/* Query input */}
      <form
        onSubmit={handleSend}
        className="mt-2 flex items-center gap-2 rounded-xl bg-slate-900 p-1.5 pl-4 shadow-[0_20px_50px_-20px_rgba(0,0,0,0.6)] ring-1 ring-white/10"
      >
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          disabled={busy}
          placeholder="Ask me anything about compliance…"
          className="w-full bg-transparent py-2 text-sm text-white placeholder:text-slate-400 focus:outline-none disabled:opacity-60"
        />
        <button
          type="submit"
          disabled={busy}
          className="flex shrink-0 items-center gap-1.5 rounded-full bg-gradient-to-r from-brand-400 to-accent px-4 py-2 text-xs font-semibold text-white shadow-md shadow-brand-500/30 transition-transform hover:scale-105 active:scale-95 disabled:cursor-not-allowed disabled:opacity-60 disabled:hover:scale-100"
        >
          {busy ? (
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
          ) : (
            <SendHorizonal className="h-3.5 w-3.5" />
          )}
          Send
        </button>
      </form>
    </div>
  );
}
