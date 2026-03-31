function ImprovedPromptCard({ improvedPrompt, confidenceScore }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-slate-800">
          Improved Prompt
        </h2>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700">
          Confidence: {Math.round(confidenceScore * 100)}%
        </span>
      </div>
      <div className="rounded-xl bg-slate-50 p-4 text-sm whitespace-pre-wrap text-slate-700">
        {improvedPrompt}
      </div>
    </div>
  );
}

export default ImprovedPromptCard;
