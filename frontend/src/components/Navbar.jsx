import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ThemeToggle from './ThemeToggle';
import { Link2, LogOut, User, LayoutDashboard } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  return (
    <div className="navbar bg-base-100 border-b border-base-content/10 px-4 md:px-8 sticky top-0 z-50 backdrop-blur-md bg-opacity-80">
      <div className="flex-1">
        <Link to="/" className="flex items-center gap-2 text-xl font-bold tracking-tighter">
          <div className="bg-primary text-base-100 p-1.5 rounded-lg">
            <Link2 size={24} />
          </div>
          <span>SHORTLY</span>
        </Link>
      </div>
      <div className="flex-none gap-2">
        <ThemeToggle />
        {user ? (
          <div className="dropdown dropdown-end">
            <label tabIndex={0} className="btn btn-ghost btn-circle avatar border border-base-content/20">
              <div className="w-10 rounded-full flex items-center justify-center">
                <User size={20} />
              </div>
            </label>
            <ul tabIndex={0} className="mt-3 z-[1] p-2 shadow menu menu-sm dropdown-content bg-base-100 rounded-box w-52 border border-base-content/10">
              <li>
                <div className="px-4 py-2 font-bold text-xs opacity-50 uppercase tracking-widest">
                  {user.email}
                </div>
              </li>
              <li>
                <Link to="/dashboard" className="flex items-center gap-2">
                  <LayoutDashboard size={16} /> Dashboard
                </Link>
              </li>
              <li>
                <button onClick={handleLogout} className="text-red-500 flex items-center gap-2">
                  <LogOut size={16} /> Logout
                </button>
              </li>
            </ul>
          </div>
        ) : (
          <div className="flex gap-2">
            <Link to="/login" className="btn btn-ghost btn-sm">Login</Link>
            <Link to="/register" className="btn btn-primary btn-sm rounded-lg px-6">Sign Up</Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default Navbar;
