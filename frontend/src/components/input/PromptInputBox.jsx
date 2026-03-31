function PromptInputBox({ value, onChange, onKeyDown }) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-slate-700">
        Your raw prompt
      </label>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={onKeyDown}
        placeholder="Example: Analyze this dataset and give insights"
        className="w-full min-h-36 rounded-2xl border border-slate-300 p-4 text-sm shadow-sm transition focus:outline-none focus:ring-2 focus:ring-slate-400"
      />
    </div>
  );
}

export default PromptInputBox;
