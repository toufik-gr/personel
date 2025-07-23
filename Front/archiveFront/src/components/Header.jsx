import React from "react";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const Header = () => {
  const [user, setUser] = useState("");

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem("access_token");
      if (token) {
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        try {
          const res = await axios.get("http://localhost:8000/users/profile/");
          setUser(res.data);
          console.log(res.data);
        } catch (err) {
          console.log("Not authenticated");
        }
      }
    };
    fetchUser();
  }, []);

  return (
    <nav className="bg-green-600 text-white px-3 py-3 shadow-md mb-2">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-xl font-bold">📚 التوثيق الرقمي</div>
        <ul className="flex space-x-6">
          <li>
            <Link to="/" className="hover:text-green-200">
              الرئيسية
            </Link>
          </li>

          {user && (
            <>
              <li>
                <Link to="/allEns" className="hover:text-green-200">
                  أساتذة
                </Link>
              </li>
              <li>
                <Link to="/allEmp" className="hover:text-green-200">
                  موظفين
                </Link>
              </li>
              <li>
                <Link to="/allContrat" className="hover:text-green-200">
                  متعاقدين
                </Link>
              </li>
              <li> المستخدم : {user.username}</li>
            </>
          )}

          <li>
            {user ? (
              <Link to="/logout" className="hover:text-green-200">
                خروج
              </Link>
            ) : (
              <Link to="/login" className="hover:text-green-200">
                دخول
              </Link>
            )}
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Header;
