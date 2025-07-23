import { useEffect, useState } from "react";
import axios from "axios";
import { FaFilePdf } from "react-icons/fa";
import SelectTableEns from "./reUsable/SelectTableEns";
import GRADES from "./reUsable/Grades";

export default function PdfList({
  enseignantId,
  selectedEnseignant,
  refreshTrigger,
  type,
}) {
  const [pdfs, setPdfs] = useState([]);
  const [grade, setGrade] = useState("");
  const [grades, setGrades] = useState([]);
  const ur =
    type == "enseignant"
      ? `http://127.0.0.1:8000/enseign/pdfsList/${enseignantId}/`
      : type == "employe"
      ? `http://127.0.0.1:8000/employe/pdfsList/${enseignantId}/`
      : `http://127.0.0.1:8000/posts/pdfsList/${enseignantId}/`;

  useEffect(() => {
    const fetchPdfs = async () => {
      try {
        const res = await axios.get(ur, {
          params: {
            grade,
          },
        });
        setPdfs(res.data);
      } catch (error) {
        console.error("Failed to fetch PDFs", error);
      }
    };
    if (enseignantId) {
      fetchPdfs();
    }
  }, [enseignantId, refreshTrigger, grade]); // Add refreshTrigger here

  //   fetchPdfs();
  // }, [enseignantId]);
  console.log(pdfs);
  console.log(enseignantId);

  //get grades by division employe
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
  return (
    <div>
      <div className="flex justify-between mb-5">
        <h2 className="text-xl font-bold text-green-600 flex items-center mb-3 gap-2">
          <FaFilePdf className="text-green-500" />
          الملفات المرفوعة
        </h2>
        <SelectTableEns
          //label="الرتبة"
          value={grade}
          placeholder={
            type === "contrat" ? "-- إختر المنصب --" : "-- إختر الرتبة--"
          }
          options={
            type === "enseignant"
              ? GRADES.ENS
              : type === "employe"
              ? grades
              : GRADES.CONTRAT
          }
          onChange={(e) => {
            setGrade(e.target.value);
            //setPage(1);
          }}
        />
      </div>
      {pdfs.length === 0 ? (
        <p className="text-gray-700 font-medium">لا توجد ملفات</p>
      ) : (
        <div className="overflow-x-auto rounded-lg shadow">
          <table className="min-w-full divide-y divide-gray-200 text-sm text-right">
            <thead className="bg-gray-100">
              <tr>
                <th className="px-6 py-3 font-bold text-gray-700 uppercase tracking-wider">
                  الملف
                </th>
                {type != "contrat" && (
                  <th className="px-6 py-3 font-bold text-gray-700 uppercase tracking-wider">
                    الرتبة
                  </th>
                )}
                <th className="px-6 py-3 font-bold text-gray-700 uppercase tracking-wider">
                  المستخدم
                </th>
                <th className="px-6 py-3 font-bold text-gray-700 uppercase tracking-wider">
                  بتاريخ
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 bg-white">
              {pdfs.map((pdfList) => {
                const fileName = decodeURIComponent(
                  pdfList.file.split("/").pop()
                ).replace(/_/g, " ");
                return (
                  <tr key={pdfList.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-blue-600">
                      <a
                        href={pdfList.file}
                        target="_blank"
                        rel="noreferrer"
                        className="hover:underline"
                      >
                        {fileName}
                      </a>
                    </td>
                    {type != "contrat" && (
                      <td className="px-6 py-4 font-medium text-gray-800">
                        {pdfList.grade}
                      </td>
                    )}
                    <td className="px-6 py-4 text-gray-600">{pdfList.user}</td>
                    <td className="px-6 py-4 text-gray-500 text-sm">
                      {pdfList.uploaded_at.split("T")[0]}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
