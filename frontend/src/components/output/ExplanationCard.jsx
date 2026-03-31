function ExplanationCard({ explanation, promptType }) {
  const formattedType = promptType
    ? promptType
        .replaceAll("_", " ")
        .replace(/\b\w/g, (char) => char.toUpperCase())
    : "Unknown";

  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:shadow-md space-y-3">
      <div>
        <h2 className="text-lg font-semibold text-slate-800">Why This Works</h2>
        <p className="mt-1 text-xs uppercase tracking-wide text-slate-500">
          Detected type: {formattedType}
        </p>
      </div>

      <p className="text-sm leading-6 text-slate-700">{explanation}</p>
    </div>
  );
}

export default ExplanationCard;
