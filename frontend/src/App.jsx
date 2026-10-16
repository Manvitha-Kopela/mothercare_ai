
import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [mobile, setMobile] = useState("");
  const [password, setPassword] = useState("");

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [loggedInUser, setLoggedInUser] = useState(() => {
    try {
      return JSON.parse(
        localStorage.getItem("mothercareai_user")
      );
    } catch {
      return null;
    }
  });

  const [page, setPage] = useState("dashboard");

  const [women, setWomen] = useState([]);
  const [womenLoading, setWomenLoading] = useState(false);
  const [womenError, setWomenError] = useState("");

  const [mlInput, setMlInput] = useState({
    age: "25",
    systolic_bp: "120",
    diastolic_bp: "80",
    bs: "7.0",
    body_temp: "98.6",
    heart_rate: "75",
  });

  const [mlResult, setMlResult] = useState(null);
  const [mlError, setMlError] = useState("");
  const [mlLoading, setMlLoading] = useState(false);



  const [woman, setWoman] = useState({
    name: "",
    age: "",
    mobile: "",
    address: "",
    lmp: "",
    edd: "",
  });

  const handleLogin = async (event) => {
    event.preventDefault();

    setError("");
    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ mobile, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Login failed. Check your credentials."
        );
      }

      const user = {
        id: data.health_worker_id,
        name: data.name,
        role: data.role,
      };

      localStorage.setItem(
        "mothercareai_token",
        data.access_token
      );

      localStorage.setItem(
        "mothercareai_user",
        JSON.stringify(user)
      );

      setLoggedInUser(user);
      setPage("dashboard");
      setMobile("");
      setPassword("");
      setError("");
      setMessage("");
    } catch (err) {
      setError(err.message || "Unable to connect to the server.");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("mothercareai_token");
    localStorage.removeItem("mothercareai_user");

    setLoggedInUser(null);
    setPage("dashboard");
    setMessage("");
    setError("");
  };

  const handleWomanChange = (event) => {
    const { name, value } = event.target;

    setWoman((previous) => ({
      ...previous,
      [name]: value,
    }));
  };

  const handleWomanSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setMessage("");
    setLoading(true);

    try {
      const token = localStorage.getItem("mothercareai_token");

      if (!token) {
        handleLogout();
        throw new Error("Please log in again to continue.");
      }

      const payload = {
        name: woman.name.trim(),
        age: Number(woman.age),
        mobile: woman.mobile.trim(),
        address: woman.address.trim(),
        lmp: woman.lmp || null,
        edd: woman.edd || null,
      };

      const response = await fetch(`${API_URL}/pregnant-women/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.status === 401) {
        handleLogout();
        throw new Error("Your session is invalid or expired. Please log in again.");
      }

      if (!response.ok) {
        const details = Array.isArray(data.detail)
          ? data.detail.map((item) => item.msg).join(", ")
          : data.detail;

        throw new Error(details || "Registration failed.");
      }

      setWoman({
        name: "",
        age: "",
        mobile: "",
        address: "",
        lmp: "",
        edd: "",
      });

      setPage("dashboard");
      setMessage(
        `Registration successful! Record ID: ${data.id}`
      );
    } catch (err) {
      setError(err.message || "Unable to connect to the server.");
    } finally {
      setLoading(false);
    }
  };

  const handleViewWomen = async () => {
    setPage("women");
    setWomenError("");
    setMessage("");
    setWomenLoading(true);

    try {
      const token = localStorage.getItem("mothercareai_token");

      if (!token) {
        handleLogout();
        return;
      }

      const response = await fetch(`${API_URL}/pregnant-women/`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (response.status === 401) {
        handleLogout();
        setError("Your session has expired. Please log in again.");
        return;
      }

      if (!response.ok) {
        throw new Error(
          data.detail || "Could not load registered women."
        );
      }

      setWomen(data);
    } catch (err) {
      setWomenError(
        err.message || "Unable to connect to the server."
      );
    } finally {
      setWomenLoading(false);
    }
  };

  const handleMlPrediction = async (event) => {
    event.preventDefault();

    setMlError("");
    setMlResult(null);
    setMlLoading(true);

    try {
      const token = localStorage.getItem("mothercareai_token");

      if (!token) {
        handleLogout();
        throw new Error("Please log in again to continue.");
      }

      const payload = {
        age: Number(mlInput.age),
        systolic_bp: Number(mlInput.systolic_bp),
        diastolic_bp: Number(mlInput.diastolic_bp),
        bs: Number(mlInput.bs),
        body_temp: Number(mlInput.body_temp),
        heart_rate: Number(mlInput.heart_rate),
      };

      const response = await fetch(`${API_URL}/ml/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.status === 401) {
        handleLogout();
        throw new Error("Your session expired. Please log in again.");
      }

      if (!response.ok) {
        const details = Array.isArray(data.detail)
          ? data.detail.map((item) => item.msg).join(", ")
          : data.detail;

        throw new Error(details || "Prediction request failed.");
      }

      setMlResult(data);
    } catch (err) {
      setMlError(err.message || "Unable to connect to the server.");
    } finally {
      setMlLoading(false);
    }
  };


  if (!loggedInUser) {
    return (
      <div className="app">
        <div className="login-card">
          <div className="logo">MC</div>

          <h1>MotherCareAI</h1>

          <p className="subtitle">
            Maternal Health Decision Support System
          </p>

          <div className="pregnancy-icon" aria-hidden="true">
            🤰
          </div>

          <h2>Health Worker Login</h2>

          <form onSubmit={handleLogin}>
            <label htmlFor="login-mobile">Mobile Number</label>
            <input
              id="login-mobile"
              type="tel"
              autoComplete="username"
              placeholder="Enter mobile number"
              value={mobile}
              onChange={(event) => setMobile(event.target.value)}
              required
            />

            <label htmlFor="login-password">Password</label>
            <input
              id="login-password"
              type="password"
              autoComplete="current-password"
              placeholder="Enter password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
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

          {error && (
            <div className="error-message" role="alert">
              {error}
            </div>
          )}

          <p className="language">English | తెలుగు</p>
          <p className="worker-label">ASHA / ANM</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="dashboard-card">
        <div className="logo">MC</div>

        <h1>MotherCareAI</h1>

        <p className="subtitle">
          Maternal Health Decision Support System
        </p>

        {page === "dashboard" && (
          <>
            <div className="welcome-box">
              <h2>Welcome, {loggedInUser.name}</h2>
              <p>
                Role: <strong>{loggedInUser.role}</strong>
              </p>
              <p>
                Health Worker ID: <strong>{loggedInUser.id}</strong>
              </p>
            </div>

            {message && (
              <div className="success-message" role="status">
                {message}
              </div>
            )}

            {error && (
              <div className="error-message" role="alert">
                {error}
              </div>
            )}

            <div className="dashboard-actions">
              <button
                className="primary-button"
                onClick={() => {
                  setWoman({
                    name: "",
                    age: "",
                    mobile: "",
                    address: "",
                    lmp: "",
                    edd: "",
                  });
                  setMessage("");
                  setError("");
                  setPage("register");
                }}
              >
                Register Pregnant Woman
              </button>
              
              <button
                className="secondary-button"
                onClick={handleViewWomen}
              >
                View Registered Women
              </button>

              <button
                className="secondary-button"
                onClick={() =>
                  setMessage("Referral management is coming next.")
                }
              >
                View Referrals
              </button>

              <button
                className="secondary-button"
                onClick={() =>
                  setMessage("Follow-up management is coming next.")
                }
              >
                Follow-up Cases
              </button>

              <button
                className="secondary-button"
                onClick={() => {
                  setMlResult(null);
                  setMlError("");
                  setMessage("");
                  setError("");
                  setPage("ml-prediction");
                }}
              >
                Experimental ML Risk Prediction
              </button>

            </div>
          </>
        )}

        {page === "register" && (
          <>
            <h2>Register Pregnant Woman</h2>

            <p className="form-note">
              Enter the woman's basic registration details.
            </p>

            <form onSubmit={handleWomanSubmit}>
              <label htmlFor="woman-name">Full Name</label>
              <input
                id="woman-name"
                name="name"
                type="text"
                minLength={2}
                maxLength={100}
                placeholder="Enter full name"
                value={woman.name}
                onChange={handleWomanChange}
                required
              />

              <label htmlFor="woman-age">Age</label>
              <input
                id="woman-age"
                name="age"
                type="number"
                min="15"
                max="60"
                placeholder="Enter age"
                value={woman.age}
                onChange={handleWomanChange}
                required
              />

              <label htmlFor="woman-mobile">Mobile Number</label>
              <input
                id="woman-mobile"
                name="mobile"
                type="tel"
                minLength={10}
                maxLength={15}
                placeholder="Enter mobile number"
                value={woman.mobile}
                onChange={handleWomanChange}
                required
              />

              <label htmlFor="woman-address">Village / Address</label>
              <input
                id="woman-address"
                name="address"
                type="text"
                minLength={2}
                maxLength={255}
                placeholder="Enter village or address"
                value={woman.address}
                onChange={handleWomanChange}
                required
              />

              <label htmlFor="woman-lmp">
                Last Menstrual Period (LMP) — optional
              </label>
              <input
                id="woman-lmp"
                name="lmp"
                type="date"
                value={woman.lmp}
                onChange={handleWomanChange}
              />

              <label htmlFor="woman-edd">
                Expected Delivery Date (EDD) — optional
              </label>
              <input
                id="woman-edd"
                name="edd"
                type="date"
                value={woman.edd}
                onChange={handleWomanChange}
              />

              <button
                type="submit"
                className="login-button"
                disabled={loading}
              >
                {loading ? "Saving..." : "Save Registration"}
              </button>

              <button
                type="button"
                className="secondary-button form-back-button"
                onClick={() => {
                  setPage("dashboard");
                  setError("");
                  setMessage("");
                }}
              >
                Back to Dashboard
              </button>
            </form>

            {error && (
              <div className="error-message" role="alert">
                {error}
              </div>
            )}
          </>
        )}

        {page === "ml-prediction" && (
          <>
            <h2>Experimental ML Risk Prediction</h2>

            <p className="form-note">
              Demonstration only. This model is not clinically validated and
              must not be used for patient-care or referral decisions.
            </p>

            <form onSubmit={handleMlPrediction}>
              {[
                ["age", "Age (years)", "25"],
                ["systolic_bp", "Systolic BP (mmHg)", "120"],
                ["diastolic_bp", "Diastolic BP (mmHg)", "80"],
                ["bs", "Blood sugar (dataset units)", "7.0"],
                ["body_temp", "Body temperature (°F)", "98.6"],
                ["heart_rate", "Heart rate (bpm)", "75"],
              ].map(([name, label, placeholder]) => (
                <div key={name}>
                  <label htmlFor={`ml-${name}`}>{label}</label>
                  <input
                    id={`ml-${name}`}
                    type="number"
                    step="any"
                    value={mlInput[name]}
                    placeholder={placeholder}
                    onChange={(event) => {
                      setMlInput((previous) => ({
                        ...previous,
                        [name]: event.target.value,
                      }));
                      setMlResult(null);
                      setMlError("");
                    }}
                    required
                  />
                </div>
              ))}

              <button
                type="submit"
                className="login-button"
                disabled={mlLoading}
              >
                {mlLoading ? "Predicting..." : "Run Experimental Prediction"}
              </button>
            </form>

            {mlError && (
              <div className="error-message" role="alert">
                {mlError}
              </div>
            )}

            
            {mlResult && (
              <section className="ml-result-card" aria-live="polite">
                <h3>Model Output (Experimental)</h3>

                <div className="ml-predicted-class">
                  Predicted class: {mlResult.predicted_class}
                </div>

                <h4>Model probability estimates</h4>

                {Object.entries(mlResult.probability_estimates || {}).map(
                  ([label, probability]) => {
                    const percentage = Math.max(
                      0,
                      Math.min(100, Number(probability) * 100)
                    );

                    return (
                      <div className="ml-probability-row" key={label}>
                        <div className="ml-probability-label">
                          <span>{label}</span>
                          <span>{percentage.toFixed(2)}%</span>
                        </div>

                        <div
                          className="ml-probability-track"
                          role="img"
                          aria-label={`${label}: ${percentage.toFixed(2)} percent`}
                        >
                          <div
                            className="ml-probability-fill"
                            style={{ width: `${percentage}%` }}
                          />
                        </div>
                      </div>
                    );
                  }
                )}

                <p>
                  <strong>Clinical validation:</strong>{" "}
                  {mlResult.clinical_validation ? "Yes" : "No"}
                </p>

                <p className="ml-validation-note">
                  {mlResult.disclaimer}
                </p>
              </section>
            )}


            <button
              type="button"
              className="secondary-button form-back-button"
              onClick={() => {
                setPage("dashboard");
                setMlResult(null);
                setMlError("");
              }}
            >
              Back to Dashboard
            </button>
          </>
        )}


        {page === "women" && (
          <>
            <h2>Registered Pregnant Women</h2>

            {womenLoading && <p>Loading registered women...</p>}

            {womenError && (
              <div className="error-message" role="alert">
                {womenError}
              </div>
            )}

            {!womenLoading && !womenError && women.length === 0 && (
              <p>No registered women found.</p>
            )}

            {!womenLoading && !womenError && women.length > 0 && (
              <div className="women-table-container">
                <table className="women-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Age</th>
                      <th>Mobile</th>
                      <th>Address</th>
                      <th>LMP</th>
                      <th>EDD</th>
                    </tr>
                  </thead>
                  <tbody>
                    {women.map((item) => (
                      <tr key={item.id}>
                        <td>{item.id}</td>
                        <td>{item.name}</td>
                        <td>{item.age}</td>
                        <td>{item.mobile}</td>
                        <td>{item.address}</td>
                        <td>{item.lmp || "—"}</td>
                        <td>{item.edd || "—"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            <button
              type="button"
              className="secondary-button form-back-button"
              onClick={() => setPage("dashboard")}
            >
              Back to Dashboard
            </button>
          </>
        )}


        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </div>
  );
}

export default App;
