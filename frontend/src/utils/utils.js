function isNameValid(name) {
    if (!name || typeof name !== "string") return false;
    return /^[a-zA-Z]/.test(name);
  }

function isAgeValid(age) {
    if (!age || typeof age !== "number") return false;
    return age >= 0 && age <= 100;
}

export { isNameValid, isAgeValid };