import axios from "axios";

function Login() {
  const login = async () => {
    const res = await axios.post("http://localhost:5000/login", {
      email: "admin@gmail.com",
      password: "1234"
    });

    localStorage.setItem("token", res.data.token);
  };

  return <button onClick={login}>Login</button>;
}
export default Login;