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
    <div className="relative rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:shadow-md space-y-4">
      <div className="flex items-start justify-between gap-3">
        <h2 className="text-lg font-semibold text-slate-800">
          Optimized Prompt
        </h2>

        <div className="flex items-center gap-2">
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
            Confidence: {Math.round(confidenceScore * 100)}%
          </span>

          <span
            className={`rounded-full px-3 py-1 text-xs font-medium ${
              reasoningMode === "hybrid"
                ? "bg-indigo-100 text-indigo-700"
                : "bg-gray-100 text-gray-700"
            }`}
          >
            {reasoningMode === "hybrid" ? "⚡ Hybrid AI" : "Rule-based"}
          </span>
        </div>
      </div>

      <button
        onClick={handleCopy}
        className="absolute right-5 top-14 rounded-lg bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700 transition hover:bg-slate-200"
      >
        Copy
      </button>

      <div className="rounded-xl bg-slate-50 p-4 pr-20 text-sm whitespace-pre-wrap leading-6 text-slate-700">
        {improvedPrompt}
      </div>
    </div>
  );
}

export default ImprovedPromptCard;
