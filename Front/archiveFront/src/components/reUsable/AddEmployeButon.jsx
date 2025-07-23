import React from "react";
import { Link } from "react-router-dom";
import { FaSquarePlus } from "react-icons/fa6";

function AddEmployeButon({ text, link }) {
  return (
    <div>
      <Link to={link} className="no-underline ">
        <button
          type="button"
          className="flex items-center gap-2 text-sm border border-blue-500 text-blue-500 px-4 py-2 rounded hover:bg-blue-50"
        >
          <FaSquarePlus className="text-base" />
          إضافة {text}
        </button>
      </Link>
    </div>
  );
}

export default AddEmployeButon;
