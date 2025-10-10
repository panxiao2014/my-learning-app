import { useRandomUser } from "../hooks/userHook";

function UserManagement() {
  const { randomUser, randomUserError, fetchRandomUser } = useRandomUser();

  return (
    <div id="users-content" data-testid="users-content">
      <h1 className="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-200">Users Management</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div id="display-user-section" className="p-4 border rounded-lg shadow-sm bg-white/60 dark:bg-gray-800/40" data-testid="display-user-area">
          <h2 className="text-lg font-semibold mb-4">Random User</h2>
          <div className="flex items-center gap-4 mb-4">
            <button
              onClick={fetchRandomUser}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg shadow-md hover:bg-purple-700 transition-colors duration-200"
            >
              Show me a user
            </button>
          </div>
          <div id="user-display-content" className="rounded-md border p-3 text-sm text-gray-800 dark:text-gray-100 min-h-[64px]" data-testid="user-display-content">
            {randomUserError ? (
              <div className="text-red-600">
                Error: {randomUserError.message}
              </div>
            ) : randomUser ? (
              <div>
                <div><span className="font-medium">Name:</span> {randomUser.name}</div>
                <div><span className="font-medium">Gender:</span> {randomUser.gender}</div>
                <div><span className="font-medium">Age:</span> {randomUser.age}</div>
              </div>
            ) : (
              <span>No user selected yet.</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default UserManagement;
