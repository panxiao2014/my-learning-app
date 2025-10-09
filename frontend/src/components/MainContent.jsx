import { usePing } from "../hooks/usePing";

function MainContent() {
  const { message, error, fetchPing } = usePing();

  return (
    <div id="main-content" data-testid="main-content">
      <h1 className="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-200">Main Page</h1>
      <div className="flex items-center gap-4">
        <button
          id="ping-button"
          data-testid="ping-button"
          onClick={fetchPing}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 transition-colors duration-200"
        >
          Click me
        </button>
        {message !== "" && (
          <span className="text-xl font-bold text-gray-800 dark:text-gray-200">
            {message}
          </span>
        )}
        {error && (
          <span className="text-red-600">Error connecting to the backend</span>
        )}
      </div>
    </div>
  );
}

export default MainContent;