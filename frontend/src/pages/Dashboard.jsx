import { useState, useEffect } from "react";
import { urlApi, analyticsApi } from "../utils/api";
import {
  ExternalLink,
  Trash2,
  BarChart2,
  Calendar,
  MousePointer2,
  Copy,
  Check,
} from "lucide-react";
import { motion } from "framer-motion";

const Dashboard = () => {
  const [urls, setUrls] = useState([]);
  const [loading, setLoading] = useState(true);
  const [copiedId, setCopiedId] = useState(null);

  useEffect(() => {
    fetchUrls();
  }, []);

  const fetchUrls = async () => {
    try {
      const res = await urlApi.list();
      setUrls(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (code) => {
    if (confirm("Are you sure you want to delete this link?")) {
      try {
        await urlApi.delete(code);
        setUrls(urls.filter((u) => u.short_code !== code));
      } catch (err) {
        alert("Failed to delete link");
      }
    }
  };

  const copyToClipboard = (code) => {
    const url = `${window.location.origin}/r/${code}`;
    navigator.clipboard.writeText(url);
    setCopiedId(code);
    setTimeout(() => setCopiedId(null), 2000);
  };

  if (loading)
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <span className="loading loading-spinner loading-lg"></span>
      </div>
    );

  return (
    <div className="max-w-6xl mx-auto px-4 py-12 space-y-12">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-4xl font-black uppercase tracking-tighter">
            My Dashboard
          </h1>
          <p className="text-base-content/60 font-medium">
            Manage and track your shortened links
          </p>
        </div>
        <div className="stats shadow bg-base-100 border border-base-content/10 rounded-2xl">
          <div className="stat px-8">
            <div className="stat-title text-xs uppercase tracking-widest font-bold">
              Total Links
            </div>
            <div className="stat-value text-3xl font-black">{urls.length}</div>
          </div>
        </div>
      </div>

      {urls.length === 0 ? (
        <div className="p-20 text-center bg-base-200/50 rounded-[3rem] border-2 border-dashed border-base-content/10">
          <p className="text-lg font-medium opacity-50">
            No links found. Start by shortening one!
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6">
          {urls
            .filter((url) => url.is_active)
            .map((url, idx) => (
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.1 }}
                key={url.short_code}
                className="group p-6 rounded-[2rem] bg-base-100 border border-base-content/5 hover:border-primary/20 hover:shadow-2xl hover:shadow-primary/5 transition-all duration-300"
              >
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
                  <div className="flex-1 min-w-0 space-y-1">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="bg-primary text-base-100 text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-tighter">
                        Active
                      </span>
                      <span className="text-xs font-mono opacity-40">
                        #{url.short_code}
                      </span>
                    </div>
                    <h3 className="text-2xl font-bold truncate group-hover:text-primary transition-colors">
                      {window.location.origin}/r/{url.short_code}
                    </h3>
                    <p className="text-sm opacity-50 truncate flex items-center gap-1">
                      <ExternalLink size={12} /> {url.long_url}
                    </p>
                  </div>

                  <div className="flex flex-wrap items-center gap-3">
                    <button
                      onClick={() => copyToClipboard(url.short_code)}
                      className="btn btn-sm btn-ghost rounded-xl px-4 hover:bg-primary hover:text-base-100"
                    >
                      {copiedId === url.short_code ? (
                        <Check size={16} />
                      ) : (
                        <Copy size={16} />
                      )}
                      {copiedId === url.short_code ? "Copied" : "Copy"}
                    </button>
                    <div className="flex gap-2">
                      <button
                        onClick={() => handleDelete(url.short_code)}
                        className="btn btn-sm btn-ghost text-red-500 hover:bg-red-500 hover:text-white rounded-xl"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                </div>

                <div className="mt-6 pt-6 border-t border-base-content/5 grid grid-cols-2 md:grid-cols-4 gap-4">
                  <StatMini
                    icon={<MousePointer2 size={14} />}
                    label="Clicks"
                    value={url.click_count > 0 ? url.click_count : "--"}
                  />
                  <StatMini
                    icon={<BarChart2 size={14} />}
                    label="Top Region"
                    value="--"
                  />
                  <StatMini
                    icon={<Calendar size={14} />}
                    label="Created"
                    value="New"
                  />
                </div>
              </motion.div>
            ))}
        </div>
      )}
    </div>
  );
};

const StatMini = ({ icon, label, value }) => (
  <div className="flex items-center gap-3">
    <div className="p-2 rounded-lg bg-base-200 text-base-content/60">
      {icon}
    </div>
    <div>
      <p className="text-[10px] uppercase tracking-widest font-bold opacity-40">
        {label}
      </p>
      <p className="font-bold">{value}</p>
    </div>
  </div>
);

export default Dashboard;
