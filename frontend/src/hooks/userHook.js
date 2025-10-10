import { useState, useCallback } from "react";
import { getRandomUserApi } from "../services/api";


export function useRandomUser() {
  const [randomUser, setRandomUser] = useState(null);
  const [randomUserError, setError] = useState(null);

  const fetchRandomUser = useCallback(async () => {
    setError(null);
    try {
      const user = await getRandomUserApi();
      setRandomUser(user);
    } catch (e) {
      setError(e);
      setRandomUser(null);
    }
  }, []);

  return { randomUser, randomUserError, fetchRandomUser };
}