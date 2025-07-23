import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function Logout() {
  const navigate = useNavigate();

  useEffect(() => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    delete axios.defaults.headers.common["Authorization"];
    navigate("/");
  }, [navigate]);

  return <p>تسجيل الخروج ...</p>;
}
