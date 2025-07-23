import { useState, useEffect } from "react";
import ShowInfo from "../components/ShowInfo";
import PDFUploader from "../components/PDFUploader";
import PdfList from "../components/PdfList";
import { useParams } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";

const AllOperations = ({ type }) => {
  const { id } = useParams();
  const [selectedEnseignant, setSelectedEnseignant] = useState("");
  const [refreshTrigger, setRefreshTrigger] = useState(false);
  const ur =
    type == "enseignant"
      ? `http://127.0.0.1:8000/enseign/ens/${id}/`
      : type == "employe"
      ? `http://127.0.0.1:8000/employe/emp/${id}/`
      : type == "contrat"
      ? `http://127.0.0.1:8000/posts/emp/${id}/`
      : null;
  useEffect(() => {
    axios
      .get(ur, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      })
      .then((res) => setSelectedEnseignant(res.data));
  }, [id]);
  console.log(selectedEnseignant);

  const updateEns = (updateData) => {
    //,id) => {
    axios
      .put(ur, updateData)

      .then((res) => {
        console.log(res.data);
        setSelectedEnseignant(updateData);
        toast.success("Enseignant updated succesfully");
      })

      .catch((err) => console.log(err.message));
  };
  //  console.log(id);
  return (
    // <form>
    <div className="p-6 bg-gray-200 font-sans w-full h-full ">
      <div className="grid [grid-template-columns:40%_60%] gap-6 ml-5 h-[500px]">
        <div className="bg-white p-4 rounded-lg shadow  ">
          <ShowInfo
            id={id}
            updateObj={updateEns}
            selectedEnseignant={selectedEnseignant}
            setSelectedEnseignant={setSelectedEnseignant}
            type={type}
          />
        </div>
        <div className="h-full grid grid-rows-[30%_70%] gap-3">
          <div className="bg-white p-6 rounded-lg shadow text-center w-full">
            {/* <div className="p-6 bg-white rounded-xl shadow w-full max-w-2xl mx-auto border border-gray-200"> */}
            <PDFUploader
              id={id}
              selectedEnseignant={selectedEnseignant}
              setRefreshTrigger={setRefreshTrigger}
              type={type}
            />
          </div>
          <div className="bg-white p-6 rounded-lg shadow text-center w-full">
            <PdfList
              enseignantId={id}
              selectedEnseignant={selectedEnseignant}
              refreshTrigger={refreshTrigger}
              type={type}
            />
          </div>
        </div>
      </div>
    </div>
    // </form>
  );
};

export default AllOperations;
