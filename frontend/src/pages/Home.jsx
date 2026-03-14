import { useState } from "react";
import { urlApi } from "../utils/api";
import { useAuth } from "../context/AuthContext";
import { Scissors, Copy, Check, ExternalLink, ArrowRight } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const Home = () => {
  const { user } = useAuth();
  const [url, setUrl] = useState("");
  const [customCode, setCustomCode] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState("");

  const handleShorten = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await urlApi.create({
        long_url: url,
        custom_code: customCode || null,
      });
      setResult(res.data);
      setUrl("");
      setCustomCode("");
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    const shortUrl = `${window.location.origin}/r/${result.short_code}`;
    navigator.clipboard.writeText(shortUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 py-20 bg-base-100 bg-mesh transition-colors duration-300">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl w-full text-center space-y-12"
      >
        <div className="space-y-6">
          <h1 className="text-7xl md:text-9xl font-black tracking-tighter text-base-content uppercase leading-none">
            {/* Scale <span className="text-secondary text-stroke italic">down</span> <br/>
            your <span className="text-primary italic">impact</span> */}
            URL Shortener
          </h1>
          {/* <p className="text-lg md:text-2xl text-base-content/50 font-medium max-w-2xl mx-auto uppercase tracking-wide">
            The minimalist link management platform <br/>
            built for the modern digital era.
          </p> */}
        </div>

        <form onSubmit={handleShorten} className="space-y-4">
          <div className="relative group">
            <input
              type="url"
              placeholder="Paste your long URL here..."
              className="input input-bordered w-full h-16 md:h-20 px-6 text-lg rounded-2xl bg-base-100 border-2 border-base-content/20 focus:border-primary transition-all duration-300 pr-32"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
            <button
              type="submit"
              disabled={loading}
              className="absolute right-2 top-2 bottom-2 btn btn-primary px-6 md:px-10 rounded-xl hover:scale-95 transition-transform"
            >
              {loading ? (
                <span className="loading loading-spinner"></span>
              ) : (
                "Shorten"
              )}
            </button>
          </div>

          {user && (
            <div className="flex justify-center">
              <input
                type="text"
                placeholder="Custom code (optional)"
                className="input input-sm input-bordered w-48 text-center rounded-lg bg-base-100/50"
                value={customCode}
                onChange={(e) => setCustomCode(e.target.value)}
              />
            </div>
          )}
        </form>

        {error && (
          <div className="alert alert-error bg-error/10 border-error/20 text-error rounded-xl max-w-md mx-auto">
            <span>{error}</span>
          </div>
        )}

        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="p-8 rounded-3xl bg-neutral text-neutral-content space-y-4 shadow-2xl relative overflow-hidden"
            >
              <div className="absolute top-0 right-0 p-4 opacity-10">
                <Scissors size={100} />
              </div>

              <div className="relative z-10">
                <h3 className="text-sm uppercase tracking-widest font-bold opacity-70 mb-2 text-primary">
                  Your Short Link
                </h3>
                <div className="flex flex-col md:flex-row items-center justify-between gap-4 bg-base-100/10 p-4 rounded-2xl border border-white/10">
                  <span className="text-2xl font-mono font-bold truncate max-w-full">
                    {window.location.origin}/r/{result.short_code}
                  </span>
                  <div className="flex gap-2 w-full md:w-auto">
                    <button
                      onClick={copyToClipboard}
                      className="btn btn-outline border-white/20 hover:bg-white hover:text-black flex-1 md:flex-none py-2 h-auto"
                    >
                      {copied ? <Check size={18} /> : <Copy size={18} />}
                      {copied ? "Copied" : "Copy"}
                    </button>
                    <a
                      href={`${window.location.origin}/r/${result.short_code}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn btn-primary flex-1 md:flex-none py-2 h-auto"
                    >
                      <ExternalLink size={18} />
                      Visit
                    </a>
                  </div>
                </div>
                <div className="mt-4 text-left border-t border-white/5 pt-4">
                  <p className="text-xs opacity-50 uppercase tracking-tight">
                    Original URL
                  </p>
                  <p className="text-sm truncate opacity-80">
                    {result.long_url}
                  </p>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="pt-12 grid grid-cols-1 md:grid-cols-3 gap-8">
          <FeatureCard
            icon={<ArrowRight />}
            title="Lightning Fast"
            desc="Optimized redirection system for instant access."
          />
          <FeatureCard
            icon={<ArrowRight />}
            title="Secure Links"
            desc="Encrypted hashing to protect your data."
          />
          <FeatureCard
            icon={<ArrowRight />}
            title="Detailed Analytics"
            desc="Track your link performance in real-time."
          />
        </div>
      </motion.div>
    </div>
  );
};

const FeatureCard = ({ icon, title, desc }) => (
  <div className="p-6 rounded-2xl border border-base-content/5 bg-base-200/50 hover:bg-base-200 transition-colors text-left space-y-2">
    <div className="p-2 bg-primary text-base-100 w-fit rounded-lg">{icon}</div>
    <h4 className="font-bold text-lg">{title}</h4>
    <p className="text-sm text-base-content/60">{desc}</p>
  </div>
);

export default Home;
