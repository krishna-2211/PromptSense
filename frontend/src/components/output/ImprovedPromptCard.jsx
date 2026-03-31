function ImprovedPromptCard({
  improvedPrompt,
  confidenceScore,
  reasoningMode,
}) {
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(improvedPrompt);
    } catch (error) {
      console.error("Failed to copy prompt:", error);
    }
  };

  return (
    <div className="relative overflow-hidden rounded-[24px] border border-white/60 bg-white/90 p-5 shadow-[0_12px_40px_rgba(15,23,42,0.08)] backdrop-blur transition hover:-translate-y-0.5 hover:shadow-[0_18px_50px_rgba(99,102,241,0.16)] space-y-4">
      <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-indigo-500 via-violet-500 to-fuchsia-500" />

      <div className="flex items-start justify-between gap-3">
        <h2 className="text-lg font-semibold text-slate-800">
          Optimized Prompt
        </h2>

        <div className="flex items-center gap-2">
          <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700 ring-1 ring-indigo-100">
            Confidence: {Math.round(confidenceScore * 100)}%
          </span>

          <span
            className={`rounded-full px-3 py-1 text-xs font-semibold ring-1 ${
              reasoningMode === "hybrid"
                ? "bg-fuchsia-50 text-fuchsia-700 ring-fuchsia-100"
                : "bg-slate-100 text-slate-700 ring-slate-200"
            }`}
          >
            {reasoningMode === "hybrid" ? "⚡ Hybrid AI" : "Rule-based"}
          </span>
        </div>
      </div>

      <button
        onClick={handleCopy}
        className="absolute right-5 top-14 rounded-full bg-slate-900 px-3 py-1.5 text-xs font-semibold text-white shadow-sm transition hover:bg-slate-800 hover:scale-[1.02]"
      >
        Copy
      </button>

      <div className="rounded-2xl border border-slate-200/80 bg-gradient-to-br from-slate-50 to-white p-4 pr-20 text-sm whitespace-pre-wrap leading-7 text-slate-700">
        {improvedPrompt}
      </div>
    </div>
  );
}

export default ImprovedPromptCard;
