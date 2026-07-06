const API_URL = "http://127.0.0.1:8000";
function getAuthToken() {
  return localStorage.getItem("access_token");
}
function logout() {
  localStorage.removeItem("access_token");
  window.location.href = "login.html";
}
