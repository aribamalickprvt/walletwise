const API_URL = "http://127.0.0.1:8000";

// Helper to get the saved authorization token
function getAuthToken() {
  return localStorage.getItem("access_token");
}
 




// Helper to log out
function logout() {
  localStorage.removeItem("access_token");
  window.location.href = "login.html";
}
