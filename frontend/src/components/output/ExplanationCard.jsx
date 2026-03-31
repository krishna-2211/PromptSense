function ExplanationCard({ explanation, promptType }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-3">
      <div>
        <h2 className="text-lg font-semibold text-slate-800">
          Why This Is Better
        </h2>
        <p className="text-xs uppercase tracking-wide text-slate-500 mt-1">
          Detected type: {promptType}
        </p>
      </div>
      <p className="text-sm text-slate-700">{explanation}</p>
    </div>
  );
}

export default ExplanationCard;
