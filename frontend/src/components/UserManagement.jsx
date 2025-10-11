import { useAddUser, useRandomUser } from "../hooks/userHook";

function UserManagement() {
  const { userForm, addUserError, addUserResponse, updateField, addUser, clearResponse } = useAddUser();
  const { randomUser, randomUserError, fetchRandomUser } = useRandomUser();

  const closePopup = () => {
    clearResponse();
  };

  function handleAddUser(e) {
    e.preventDefault();
    addUser();
  }

  return (
    <div id="users-content" data-testid="users-content">
      <h1 className="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-200">Users Management</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div id="add-user-section" className="p-4 border rounded-lg shadow-sm bg-white/60 dark:bg-gray-800/40" data-testid="add-user-form">
          <h2 className="text-lg font-semibold mb-4">Add a user</h2>
          <form onSubmit={handleAddUser} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1" htmlFor="name">Name</label>
              <input
                id="name"
                type="text"
                value={userForm.name}
                onChange={(e) => updateField("name", e.target.value)}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" htmlFor="gender">Gender</label>
              <select
                id="gender"
                value={userForm.gender}
                onChange={(e) => updateField("gender", e.target.value)}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" htmlFor="age">Age</label>
              <input
                id="age"
                type="number"
                min="0"
                max="100"
                step="1"
                value={userForm.age}
                onChange={(e) => {
                  // Only allow integer values between 0 and 100
                  const val = e.target.value;
                  // Allow empty string for controlled input
                  if (val === "") {
                    updateField("age", "");
                  } else {
                    const intVal = parseInt(val, 10);
                    if (!isNaN(intVal) && intVal >= 0 && intVal <= 100) {
                      updateField("age", intVal);
                    }
                  }
                }}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="0 - 100"
                inputMode="numeric"
                pattern="[0-9]*"
              />
            </div>
            <div>
              <button
                type="submit"
                className="px-4 py-2 bg-green-600 text-white rounded-lg shadow-md hover:bg-green-700 transition-colors duration-200"
              >
                Add User
              </button>
              {addUserError && (
                <div className="mt-2 text-red-600 text-sm">
                  Error: {addUserError.message}
                </div>
              )}
            </div>
          </form>
        </div>

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

      {/* Popup Modal */}
      {addUserResponse && (
        <div id="add-user-popup-modal" data-testid="add-user-popup-modal" className="fixed inset-0 flex items-center justify-center z-50 pointer-events-none">
          <div id="add-user-popup-content" data-testid="add-user-popup-content" className="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4 shadow-xl border-2 border-gray-300 dark:border-gray-600 pointer-events-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                {addUserResponse.status_code === 200 ? "Success" : "Error"}
              </h3>
              <button
                onClick={closePopup}
                className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            <div className="mb-4" id="add-user-popup-message" data-testid="add-user-popup-message">
              <p className={`text-sm ${
                addUserResponse.status_code === 200 
                  ? "text-green-600 dark:text-green-400" 
                  : "text-red-600 dark:text-red-400"
              }`}>
                {addUserResponse.message}
              </p>
            </div>
            <div className="flex justify-end">
              <button
                onClick={closePopup}
                className={`px-4 py-2 rounded-lg text-white font-medium ${
                  addUserResponse.status_code === 200 
                    ? "bg-green-600 hover:bg-green-700" 
                    : "bg-red-600 hover:bg-red-700"
                } transition-colors duration-200`}
              >
                OK
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default UserManagement;