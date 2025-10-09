import { useState } from "react";
import MainContent from "./components/MainContent";

function App() {
  const [activeTab, setActiveTab] = useState("main");

  return (
    <div className="min-h-screen flex">
      {/* Left Navigation Pane */}
      <div id="navigation-pane" data-testid="navigation-pane" className="w-64 bg-gray-100 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 p-4">
        <h2 className="text-lg font-semibold mb-6 text-gray-800 dark:text-gray-200">Navigation</h2>
        <nav className="space-y-2">
          <button
            id="main-nav-button"
            data-testid="main-nav-button"
            onClick={() => setActiveTab("main")}
            className={`w-full text-left px-4 py-2 rounded-lg transition-colors duration-200 ${
              activeTab === "main"
                ? "bg-blue-500 text-white"
                : "text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700"
            }`}
          >
            Main
          </button>
        </nav>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 p-4">
        {activeTab === "main" && <MainContent />}
      </div>
    </div>
  );
}

export default App;