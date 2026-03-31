import { useState } from "react";
import PromptInputBox from "../components/input/PromptInputBox";
import ImprovedPromptCard from "../components/output/ImprovedPromptCard";
import MissingContextCard from "../components/output/MissingContextCard";
import ExplanationCard from "../components/output/ExplanationCard";
import PromptVariantsTabs from "../components/output/PromptVariantsTabs";
import { improvePrompt } from "../services/api";

function WorkspacePage() {
  const [prompt, setPrompt] = useState("");
  const [audience, setAudience] = useState("general");
  const [outputStyle, setOutputStyle] = useState("structured");
  const [additionalContext, setAdditionalContext] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleImprove = async () => {
    setError("");
    setLoading(true);
    setResult(null);

    try {
      const data = await improvePrompt({
        original_prompt: prompt,
        audience,
        output_style: outputStyle,
        additional_context: additionalContext || null,
        file_context: null,
      });
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50 px-6 py-10">
      <div className="mx-auto max-w-7xl space-y-8">
        <div className="space-y-3">
          <div>
            <h1 className="text-5xl font-bold tracking-tight text-slate-900">
              PromptSense
            </h1>
            <p className="mt-2 text-lg text-slate-600">
              Turn vague ideas into high-performing LLM prompts.
            </p>
          </div>

          <div className="inline-flex items-center gap-2 rounded-full bg-indigo-50 px-3 py-1 text-sm font-medium text-indigo-700">
            ⚡ Hybrid Intelligence Enabled
          </div>
        </div>

        <div className="grid gap-8 lg:grid-cols-[1.05fr_1fr]">
          <div className="space-y-5 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="space-y-1">
              <h2 className="text-lg font-semibold text-slate-800">
                Your Prompt
              </h2>
              <p className="text-sm text-slate-500">
                Describe what you want the LLM to do, even if it’s vague.
              </p>
            </div>

            <PromptInputBox
              value={prompt}
              onChange={setPrompt}
              onKeyDown={(e) => {
                if (
                  e.ctrlKey &&
                  e.key === "Enter" &&
                  prompt.trim() &&
                  !loading
                ) {
                  handleImprove();
                }
              }}
            />
            <div className="space-y-2">
              <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
                Try a sample
              </p>
              <div className="flex flex-wrap gap-2">
                {[
                  "Write a professional email to recruiter",
                  "Summarize this report",
                  "Explain machine learning simply",
                  "Create a 7-day study plan",
                ].map((sample) => (
                  <button
                    key={sample}
                    type="button"
                    onClick={() => setPrompt(sample)}
                    className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-700 transition hover:bg-slate-200"
                  >
                    {sample}
                  </button>
                ))}
              </div>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">
                  Audience
                </label>
                <select
                  value={audience}
                  onChange={(e) => setAudience(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 bg-white p-3 text-sm shadow-sm transition focus:outline-none focus:ring-2 focus:ring-indigo-300"
                >
                  <option value="technical">Technical</option>
                  <option value="general">General</option>
                  <option value="beginner">Beginner</option>
                  <option value="executive">Executive</option>
                  <option value="professional">Professional</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-slate-700">
                  Output Style
                </label>
                <select
                  value={outputStyle}
                  onChange={(e) => setOutputStyle(e.target.value)}
                  className="w-full rounded-xl border border-slate-300 bg-white p-3 text-sm shadow-sm transition focus:outline-none focus:ring-2 focus:ring-indigo-300"
                >
                  <option value="structured">Structured</option>
                  <option value="concise">Concise</option>
                  <option value="detailed">Detailed</option>
                  <option value="professional">Professional</option>
                </select>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-700">
                Additional Context
              </label>
              <textarea
                value={additionalContext}
                onChange={(e) => setAdditionalContext(e.target.value)}
                placeholder="Optional: add details that help the system understand your intent"
                className="w-full min-h-28 rounded-2xl border border-slate-300 p-4 text-sm shadow-sm transition focus:outline-none focus:ring-2 focus:ring-indigo-300"
              />
            </div>

            <button
              onClick={handleImprove}
              disabled={loading || !prompt.trim()}
              className="flex w-full items-center justify-center rounded-2xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 hover:scale-[1.01] active:scale-[0.99] disabled:cursor-not-allowed disabled:bg-slate-400"
            >
              {loading ? "Thinking..." : "Improve Prompt"}
            </button>
            <p className="text-center text-xs text-slate-400">
              Press Ctrl + Enter to improve
            </p>

            {error && (
              <div className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
                {error}
              </div>
            )}
          </div>

          <div className="space-y-5">
            {result ? (
              <>
                <ImprovedPromptCard
                  improvedPrompt={result.improved_prompt}
                  confidenceScore={result.confidence_score}
                  reasoningMode={result.reasoning_mode}
                />

                <MissingContextCard missingPieces={result.missing_pieces} />

                <ExplanationCard
                  explanation={result.explanation}
                  promptType={result.prompt_type}
                />

                <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm space-y-3">
                  <h2 className="text-lg font-semibold text-slate-800">
                    Expected Output Preview
                  </h2>
                  <div className="rounded-xl bg-slate-50 p-4 text-sm whitespace-pre-wrap leading-6 text-slate-700">
                    {result.expected_output_preview}
                  </div>
                </div>

                <PromptVariantsTabs variants={result.variants} />
              </>
            ) : (
              <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center shadow-sm">
                <div className="mx-auto max-w-md space-y-3">
                  <div className="text-3xl">✨</div>
                  <h3 className="text-lg font-semibold text-slate-700">
                    Optimized output will appear here
                  </h3>
                  <p className="text-sm text-slate-500">
                    Enter a vague prompt on the left, then let PromptSense turn
                    it into a stronger LLM instruction.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default WorkspacePage;
