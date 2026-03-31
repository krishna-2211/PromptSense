import { useState } from "react";
import PromptInputBox from "../components/input/PromptInputBox";
import ImprovedPromptCard from "../components/output/ImprovedPromptCard";
import MissingContextCard from "../components/output/MissingContextCard";
import ExplanationCard from "../components/output/ExplanationCard";
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
    <div className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="mx-auto max-w-6xl space-y-8">
        <div className="space-y-2">
          <h1 className="text-4xl font-bold text-slate-900">PromptSense</h1>
          <p className="text-slate-600">
            Turn vague thoughts into structured, LLM-ready instructions.
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-2">
          <div className="space-y-5 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <PromptInputBox value={prompt} onChange={setPrompt} />

            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-700">
                Audience
              </label>
              <select
                value={audience}
                onChange={(e) => setAudience(e.target.value)}
                className="w-full rounded-xl border border-slate-300 p-3 text-sm"
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
                className="w-full rounded-xl border border-slate-300 p-3 text-sm"
              >
                <option value="structured">Structured</option>
                <option value="concise">Concise</option>
                <option value="detailed">Detailed</option>
                <option value="professional">Professional</option>
              </select>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-700">
                Additional Context
              </label>
              <textarea
                value={additionalContext}
                onChange={(e) => setAdditionalContext(e.target.value)}
                placeholder="Optional: add details that help the system understand your intent"
                className="w-full min-h-24 rounded-2xl border border-slate-300 p-4 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-400"
              />
            </div>

            <button
              onClick={handleImprove}
              disabled={loading || !prompt.trim()}
              className="w-full rounded-2xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
            >
              {loading ? "Improving..." : "Improve Prompt"}
            </button>

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
                  <div className="rounded-xl bg-slate-50 p-4 text-sm whitespace-pre-wrap text-slate-700">
                    {result.expected_output_preview}
                  </div>
                </div>
              </>
            ) : (
              <div className="rounded-3xl border border-dashed border-slate-300 bg-white p-10 text-center text-slate-500 shadow-sm">
                Your improved prompt will appear here.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default WorkspacePage;
