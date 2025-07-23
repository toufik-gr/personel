import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import logo from "../../assets/images/log.png";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:8000/api/token/", {
        username,
        password,
      });
      localStorage.setItem("access_token", res.data.access);
      localStorage.setItem("refresh_token", res.data.refresh);
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${res.data.access}`;
      navigate("/");
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form
        onSubmit={handleLogin}
        className="w-full max-w-md bg-white p-8 rounded-2xl shadow-md"
      >
        <div>
          <div className="text-center">
            <img
              src={logo}
              alt="Card Image"
              style={{
                borderRadius: "15px 15px 0px 0px",
                width: "70px",
                height: "70px",
              }}
              className=" mx-auto h-auto mb-4"
            />

            <h3 className="text-2xl font-bold text-center mb-6">
              التوثيق الرقمي{" "}
            </h3>
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 font-medium mb-2">
              المستخدم
            </label>
            <input
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter Username"
              name="username"
              type="text"
              value={username}
              required
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 font-medium mb-2">
              كلمة المرور
            </label>
            <input
              name="password"
              type="password"
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter password"
              value={password}
              required
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <div>
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition"
            >
              تسجيل دخول
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
