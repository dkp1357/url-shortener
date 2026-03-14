import { Outlet } from "react-router-dom";
import Navbar from "./Navbar";

const Layout = () => {
  return (
    <div className="min-h-screen bg-base-100 selection:bg-primary selection:text-base-100">
      <Navbar />
      <main>
        <Outlet />
      </main>
      <footer className="py-12 px-4 border-t border-base-content/5 mt-20">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6 opacity-40 grayscale">
          {/* <p className="font-bold tracking-tighter uppercase">© 2026 Shortly Inc.</p> */}
          <div className="flex gap-8 text-xs font-bold uppercase tracking-widest">
            {/* <a href="#" className="hover:text-primary transition-colors">Privacy</a>
            <a href="#" className="hover:text-primary transition-colors">Terms</a> */}
            <a href="#" className="hover:text-primary transition-colors">
              API docs
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
