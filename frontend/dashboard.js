import { useEffect, useState } from "react";
import axios from "axios";

function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      const token = localStorage.getItem("token");
      const res = await axios.get("http://localhost:5000/history", {
        headers: { Authorization: token }
      });
      setData(res.data);
    };
    fetchHistory();
  }, []);

  return (
    <div>
      <h2>History</h2>
      {data.map((item, i) => (
        <p key={i}>{item[0]} - {item[1]}</p>
      ))}
    </div>
  );
}
export default Dashboard;