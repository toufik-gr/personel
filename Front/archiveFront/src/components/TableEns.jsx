import { AiOutlineFileAdd } from "react-icons/ai";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// import { faSync } from "@fortawesome/free-solid-svg-icons";
// import { faCoffee, faUser } from "@fortawesome/free-solid-svg-icons";
import { MdOutlinePageview } from "react-icons/md";
import { toast } from "react-toastify";
import { useState, useEffect } from "react";
import axios, { all } from "axios";
import { Link } from "react-router-dom";
import { FaEdit } from "react-icons/fa";
import Loader from "./Loader";
import AddEmployeButton from "./reUsable/AddEmployeButon";
import SelectTableEns from "./reUsable/SelectTableEns";
import GRADES from "./reUsable/Grades";

import POSITIONS from "./reUsable/Positions";
import { differenceInDays, parseISO } from "date-fns";
const TableEns = ({ path }) => {
  const [allenseigns, setAllEnseigns] = useState([]);
  const [count, setCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [position, setPosition] = useState("");
  const [grade, setGrade] = useState("");
  const [page, setPage] = useState(1);
  const [next, setNext] = useState(null);
  const [prev, setPrev] = useState(null);
  const today = new Date();
  const fetchEnseigns = async (url = null) => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem("access_token");
      const res = await axios.get(url || `http://127.0.0.1:8000/${path}/`, {
        // const res = await axios.get(
        // url || `http://127.0.0.1:8000/posts/empList/`,

        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: {
          search,
          position,
          grade,
          page,
        },
      });

      setAllEnseigns(res.data.results.results);
      console.log(res.data.results.results);
      setCount(res.data.count);
      setNext(res.data.next);
      setPrev(res.data.previous);
    } catch (error) {
      console.error("Fetch error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchEnseigns();
  }, [search, position, grade, page]);

  const handleFieldChange = (field, value) => {
    setGrade((prev) => ({ ...prev, [field]: value }));
  };
  return (
    <div className="container mx-auto px-2 mt-5">
      <h1 className="text-2xl font-bold text-center text-gray-800">
        قائمة{" "}
        {path == "employe/empList"
          ? "الموظفين "
          : path == "enseign/ensList"
          ? "الأساتذة "
          : " المتعاقدين "}
      </h1>

      {/* Filters */}
      <div className="my-4 flex flex-wrap gap-4">
        <input
          //className="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent w-full max-w-xs"
          className="border border-gray-300 rounded px-3 py-2 bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent w-full max-w-xs"
          placeholder="🔍 بحث"
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(1);
          }}
        />
        <SelectTableEns
          //label="الرتبة"
          value={grade}
          placeholder=" -- الرتبة"
          options={
            path == "enseign/ensList"
              ? GRADES.ENS
              : path == "employe/empList"
              ? GRADES.EMP
              : path == "posts/empContList"
              ? GRADES.CONTRAT
              : null
          }
          onChange={(e) => {
            setGrade(e.target.value);
            setPage(1);
          }}
        />
        <SelectTableEns
          //label="الوضعية"
          placeholder=" -- الوضعية"
          value={position}
          options={
            path == "employe/empList"
              ? POSITIONS.EMP
              : path == "enseign/ensList"
              ? POSITIONS.ENS
              : path == "posts/empContList"
              ? POSITIONS.CONTRAT
              : null
          }
          onChange={(e) => {
            setPosition(e.target.value);
            setPage(1);
          }}
        />
        <AddEmployeButton
          text={
            path == "employe/empList"
              ? "موظف"
              : path == "enseign/ensList"
              ? "أستاذ"
              : "متعاقد"
          }
          link={
            path == "employe/empList"
              ? "/add-emp"
              : path == "enseign/ensList"
              ? "/add-ens"
              : "/add-contrat"
          }
          //addNew={path == "employe/empList" ? addEmploye : addEnseig}
        />
      </div>

      {isLoading ? (
        <Loader loading={isLoading} />
      ) : (
        <>
          <div className="flex justify-between items-center mb-3">
            <h2>
              العدد : <strong>{count}</strong>
            </h2>
          </div>

          <div className="overflow-x-auto">
            <table className="table-auto border-collapse border border-gray-300 w-full">
              <thead className="text-xs text-gray-600 uppercase bg-gray-100">
                <tr>
                  <th className="px-6 py-2 text-center">رقم</th>
                  <th className="px-6 py-2 text-center">اللقب</th>
                  <th className="px-6 py-2 text-center">الإسم</th>
                  <th className="px-6 py-2 text-center">الميلاد</th>
                  <th className="px-6 py-2 text-center">الرتبة</th>
                  <th className="px-6 py-2 text-center">الوضعية</th>
                  <th className="px-6 py-2 text-center">من تاريخ</th>
                  <th className="px-6 py-2 text-center">إلى تاريخ</th>
                  <th className="px-6 py-2 text-center">الكلية</th>
                  {/* <th className="px-6 py-2 text-center">تحديث</th> */}
                  <th className="px-6 py-2 text-center">تفاصيل</th>
                  {/* <th className="px-6 py-2 text-center">معاينة</th> */}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {allenseigns.map((ens) => (
                  <tr
                    key={ens.id}
                    className={
                      ens.position != "في الخدمة"
                        ? ens.debut_position == null
                          ? "bg-blue-200 text-center"
                          : differenceInDays(ens.fin_position, today) <= 60
                          ? "bg-red-200  text-center"
                          : "bg-blue-200 text-center"
                        : "text-center"
                    }
                  >
                    <td className="px-2 py-2 text-center">{ens.id}</td>
                    <td className="px-2 py-2 text-center">{ens.Nom}</td>
                    <td className="px-2 py-2 text-center">{ens.Prénom}</td>
                    <td className="px-2 py-2 text-center">{ens.dat_naiss}</td>
                    <td className="px-2 py-2 text-center">{ens.grade}</td>
                    <td className="px-2 py-2 text-center">{ens.position}</td>
                    <td className="px-2 py-2 text-center">
                      {ens.debut_position}
                    </td>
                    <td className="px-2 py-2 text-center">
                      {ens.fin_position}
                    </td>
                    <td className="px-2 py-2 text-center">{ens.faculte}</td>
                    {/* <td>
                      <Link to={`/update-ens/${ens.id}`}>
                        <button className="hover:text-orange-500">
                          <FaEdit />
                        </button>
                      </Link> 
                    </td> */}
                    <td>
                      <Link
                        to={
                          path == "enseign/ensList"
                            ? `/AllOperations/ens/${ens.id}`
                            : path == "employe/empList"
                            ? `/AllOperations/emp/${ens.id}`
                            : `/AllOperations/contrat/${ens.id}`
                        }
                      >
                        <button className="hover:text-blue-500 text-blue-700">
                          <AiOutlineFileAdd />
                        </button>
                      </Link>
                    </td>
                    {/*
                    <td>
                      
                      <button className="hover:text-green-500">
                         <MdOutlinePageview />
                        
                      </button>
                      
                    </td> */}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex justify-center gap-4 mt-4">
            <button
              onClick={() => {
                setPage((p) => p - 1);
              }}
              disabled={!prev}
              className="bg-gray-300 px-3 py-1 rounded disabled:opacity-50"
            >
              ⬅ السابق
            </button>
            <button
              onClick={() => {
                setPage((p) => p + 1);
              }}
              disabled={!next}
              className="bg-gray-300 px-3 py-1 rounded disabled:opacity-50"
            >
              التالي ➡
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default TableEns;
