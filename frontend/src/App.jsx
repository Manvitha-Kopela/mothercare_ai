import { useState } from "react";
import "./App.css";

function App() {
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [loggedInUser, setLoggedInUser] = useState(null);

  const handleLogin = async (event) => {
    event.preventDefault();

    setMessage("");
    setError("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            mobile,
            password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Login failed. Please check your credentials."
        );
      }

      // Store the JWT token locally for this development version.
      localStorage.setItem(
        "mothercareai_token",
        data.access_token
      );

      // Store basic user information.
      localStorage.setItem(
        "mothercareai_user",
        JSON.stringify({
          id: data.health_worker_id,
          name: data.name,
          role: data.role,
        })
      );

      setLoggedInUser({
        id: data.health_worker_id,
        name: data.name,
        role: data.role,
      });

      setMessage("Login successful!");

      setMobile("");
      setPassword("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("mothercareai_token");
    localStorage.removeItem("mothercareai_user");

    setLoggedInUser(null);
    setMessage("");
    setError("");
  };

  if (loggedInUser) {
    return (
      <div className="app">
        <div className="dashboard-card">
          <div className="logo">MC</div>

          <h1>MotherCareAI</h1>

          <p className="subtitle">
            Maternal Health Decision Support System
          </p>

          <div className="welcome-box">
            <h2>Welcome, {loggedInUser.name}</h2>

            <p>
              Role: <strong>{loggedInUser.role}</strong>
            </p>

            <p>
              Health Worker ID:{" "}
              <strong>{loggedInUser.id}</strong>
            </p>
          </div>

          <div className="dashboard-actions">
            <button className="primary-button">
              Register Pregnant Woman
            </button>

            <button className="secondary-button">
              View Referrals
            </button>

            <button className="secondary-button">
              Follow-up Cases
            </button>
          </div>

          <button
            className="logout-button"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="login-card">
        <div className="logo">MC</div>

        <h1>MotherCareAI</h1>

        <p className="subtitle">
          Maternal Health Decision Support System
        </p>

        <div className="pregnancy-icon">
          🤰
        </div>

        <h2>Health Worker Login</h2>

        <form onSubmit={handleLogin}>
          <label htmlFor="mobile">
            Mobile Number
          </label>

          <input
            id="mobile"
            type="tel"
            placeholder="Enter mobile number"
            value={mobile}
            onChange={(event) =>
              setMobile(event.target.value)
            }
            required
          />

          <label htmlFor="password">
            Password
          </label>

          <input
            id="password"
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            required
          />

          <button
            type="submit"
            className="login-button"
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        {message && (
          <div className="success-message">
            {message}
          </div>
        )}

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <p className="language">
          English &nbsp;|&nbsp; తెలుగు
        </p>

        <p className="worker-label">
          ASHA / ANM
        </p>
      </div>
    </div>
  );
}

export default App;