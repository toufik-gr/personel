import React, { useState, useEffect, useRef } from "react";
import { useParams, useLoaderData, useNavigate, data } from "react-router-dom";
import axios from "axios";
import Select from "./reUsable/Select";
import GRADES from "./reUsable/Grades";
import { FaUpload } from "react-icons/fa";
import { FaFilePdf } from "react-icons/fa";

function PDFUploader({ id, selectedEnseignant, setRefreshTrigger, type }) {
  const [pdfFiles, setPdfFiles] = useState([]);
  const [grade, setGrade] = useState("");
  const [user, setUser] = useState("");
  const fileInputRef = useRef();
  const navigate = useNavigate();
  const ur =
    type == "enseignant"
      ? "http://localhost:8000/enseign/upload-folder/"
      : type == "employe"
      ? "http://localhost:8000/employe/upload-folder/"
      : "http://localhost:8000/posts/upload-folder/";

  const [grades, setGrades] = useState([]);
  console.log(selectedEnseignant);
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
  // get grades by division employe
  useEffect(() => {
    const fetchGrades = async () => {
      if (!selectedEnseignant || type !== "employe") return;

      try {
        const token = localStorage.getItem("access_token");
        const res = await axios.get(
          `http://localhost:8000/employe/emp/${selectedEnseignant.id}/grades/`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        setGrades(res.data.grades);
        console.log(res.data.grades);
      } catch (err) {
        console.error("Failed to load grades:", err);
      }
    };

    fetchGrades();
  }, [selectedEnseignant, type]);

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);

    const pdfs = files.filter((file) => file.type === "application/pdf");
    if (pdfs.length === 0) {
      alert("No valid PDF files selected.");
    }

    setPdfFiles(pdfs);
  };

  const handleUpload = async () => {
    if (!grade || !selectedEnseignant || pdfFiles.length === 0) {
      alert("إختر الرتبة ، والملفات .");
      return;
    }
    console.log("pdfFiles selected:", pdfFiles);

    const formData = new FormData();
    pdfFiles.forEach((file) => {
      formData.append("pdfs", file);
    });
    formData.append("grade", grade);
    formData.append("n_ident", selectedEnseignant.id);

    //formData.append("user", user.id); // send just the ID
    try {
      for (const pair of formData.entries()) {
        console.log(pair[0], pair[1]);
      }

      await axios.post(ur, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });

      alert("تم رفع الملفات بنجاح!");
      setPdfFiles([]);
      fileInputRef.current.value = null; // ✅ resets the input
      setRefreshTrigger((prev) => !prev); // refresh the list
    } catch (error) {
      console.error("فشل الرفع:", error);
      alert("Upload failed.");
    }
  };

  return (
    <>
      <h2 className="text-xl font-bold text-green-600  mb-3 flex items-center gap-2">
        <FaUpload className="" />
        إضافة ملفات
      </h2>

      <div className="space-y-6">
        {/* Grade Selector */}
        <div className="flex flex-col text-right">
          {/* <label className="mb-1 text-sm font-medium text-gray-600">
            الرتبة
          </label> */}
          <Select
            label={type === "contrat" ? "المنصب" : "الرتبة"}
            options={
              type === "enseignant"
                ? GRADES.ENS
                : type == "employe"
                ? grades
                : GRADES.CONTRAT
            }
            value={grade}
            onChange={setGrade}
          />{" "}
        </div>

        {/* File Upload */}
        <div className="flex flex-col text-right">
          <label className="mb-1 text-sm font-medium text-gray-600">
            تحميل ملفات (PDF فقط)
          </label>
          <div className="flex items-center gap-2">
            <input
              type="file"
              webkitdirectory="true"
              multiple
              accept="application/pdf"
              ref={fileInputRef}
              onChange={handleFileChange}
              className="block w-full text-sm text-gray-600
                   file:mr-4 file:py-2 file:px-4
                   file:rounded-lg file:border-0
                   file:text-sm file:font-semibold
                   file:bg-blue-50 file:text-blue-700
                   hover:file:bg-blue-100 display flex"
            />
            <button
              onClick={handleUpload}
              className="whitespace-nowrap bg-blue-500 hover:bg-blue-700 text-white font-medium px-2 py-2 rounded-lg transition duration-150"
            >
              رفع الملفات
            </button>
            {/* </div> */}
          </div>
        </div>
      </div>
    </>
  );
}

export default PDFUploader;
