import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import { KeyRound, Mail, ArrowRight } from 'lucide-react';
import { motion } from 'framer-motion';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await login(email, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 bg-base-100">
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="max-w-md w-full p-8 space-y-8 bg-base-100 border border-base-content/10 rounded-[2.5rem] shadow-2xl"
      >
        <div className="text-center space-y-2">
          <h2 className="text-4xl font-black tracking-tighter uppercase">Welcome Back</h2>
          <p className="text-base-content/60 font-medium">Please enter your details</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            <div className="relative">
              <Mail className="absolute left-4 top-1/2 -translate-y-1/2 text-base-content/40" size={20} />
              <input
                type="email"
                placeholder="Email address"
                className="input input-bordered w-full h-14 pl-12 rounded-2xl bg-base-200/50 border-none focus:ring-2 focus:ring-primary transition-all"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="relative">
              <KeyRound className="absolute left-4 top-1/2 -translate-y-1/2 text-base-content/40" size={20} />
              <input
                type="password"
                placeholder="Password"
                className="input input-bordered w-full h-14 pl-12 rounded-2xl bg-base-200/50 border-none focus:ring-2 focus:ring-primary transition-all"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>

          {error && (
            <div className="text-sm text-red-500 font-medium px-2 italic">
              * {error}
            </div>
          )}

          <button 
            type="submit" 
            disabled={loading}
            className="btn btn-primary w-full h-14 text-lg rounded-2xl shadow-xl shadow-primary/20 hover:scale-95 transition-transform"
          >
            {loading ? <span className="loading loading-spinner"></span> : (
              <span className="flex items-center gap-2">
                Continue <ArrowRight size={20} />
              </span>
            )}
          </button>
        </form>

        <p className="text-center text-sm font-medium text-base-content/60 pt-4">
          Don't have an account? {' '}
          <Link to="/register" className="text-primary font-bold hover:underline">Sign up for free</Link>
        </p>
      </motion.div>
    </div>
  );
};

export default Login;
