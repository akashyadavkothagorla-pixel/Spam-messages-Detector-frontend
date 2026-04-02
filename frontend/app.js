import { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const [result, setResult] = useState("");
  const [history, setHistory] = useState([]);

  const API = "https://your-backend.onrender.com";  

  const login = async () => {
    const res = await axios.post(`${API}/login`, { email, password });
    localStorage.setItem("token", res.data.token);
  };

  const register = async () => {
    await axios.post(`${API}/register`, { email, password });
    alert("User created");
  };

  const checkSpam = async () => {
    const token = localStorage.getItem("token");
    const res = await axios.post(
      `${API}/predict`,
      { message: msg },
      { headers: { Authorization: token } }
    );
    setResult(res.data.result);
  };

  const loadHistory = async () => {
    const token = localStorage.getItem("token");
    const res = await axios.get(`${API}/history`, {
      headers: { Authorization: token }
    });
    setHistory(res.data);
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>🧠 Spam Detector App</h2>

      <input placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
      <input placeholder="Password" type="password" onChange={(e) => setPassword(e.target.value)} />
      <br /><br />

      <button onClick={register}>Register</button>
      <button onClick={login}>Login</button>

      <hr />

      <textarea placeholder="Enter message" onChange={(e) => setMsg(e.target.value)} />
      <br />
      <button onClick={checkSpam}>Check</button>

      <h3>{result}</h3>

      <button onClick={loadHistory}>Load History</button>

      {history.map((h, i) => (
        <p key={i}>{h[0]} → {h[1]}</p>
      ))}
    </div>
  );
}

export default App;