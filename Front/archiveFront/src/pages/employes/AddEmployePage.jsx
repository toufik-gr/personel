import React, { useState } from "react";
//import "./AddNotePage.css";
import { useNavigate } from "react-router-dom";
import EnseignantForm from "../../components/reUsable/EnseignantForm";
import { toast } from "react-toastify";
import axios from "axios";
const AddEmployePage = () => {
  const [Nom, setNom] = useState("");
  const [Prénom, setPrénom] = useState("");
  const [Type, setType] = useState("Emplo");
  const [NIN, setNIN] = useState("");
  const [matricule, setMatricule] = useState("");
  const [dat_naiss, setDat_naiss] = useState("");
  const [Lieu_naiss, setLieu_naiss] = useState("");
  const [date_recrut, setDate_recrut] = useState("");
  const [grade, setGrade] = useState("");
  const [date_grade, setDate_grade] = useState("");
  const [Echelon, setEchelon] = useState("");
  const [Catégorie, setCatégorie] = useState("");
  const [division, setDivision] = useState("");
  const [position, setPosition] = useState("");
  const [faculte, setFaculte] = useState("");
  const [debut_position, setDebut_position] = useState("");
  const [fin_position, setFin_position] = useState("");

  const navigate = useNavigate();

  const newEmploye = {
    Nom: Nom,
    Prénom: Prénom,
    Type: Type,
    NIN: NIN,
    matricule: matricule,
    dat_naiss: dat_naiss,
    Lieu_naiss: Lieu_naiss,
    date_recrut: date_recrut,
    grade: grade,
    date_grade: date_grade,
    Echelon: Echelon,
    Catégorie: Catégorie,
    division: division,
    position: position,
    faculte: faculte,
    debut_position: debut_position,
    fin_position: fin_position,
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://127.0.0.1:8000/employe/create/", newEmploye);
      toast.success("تمت الإضافة بنجاح");
      navigate("/allEmp"); // or wherever you want
    } catch (err) {
      toast.error("فشل في الإضافة");
      console.error(err);
    }
  };
  /*
  const handleSubmit = (e) => {
    e.preventDefault();
    // if (!title && !body && !category) {
    //   return;
    // }
    props.addNew(newEmploye);

    console.log(newEmploye);
  };*/
  return (
    <EnseignantForm
      type="employe"
      title="إضافة موظف جديد"
      onSubmit={handleSubmit}
      Nom={Nom}
      setNom={setNom}
      Prénom={Prénom}
      setPrénom={setPrénom}
      Type={Type}
      //setType={setType}
      NIN={NIN}
      setNIN={setNIN}
      matricule={matricule}
      setMatricule={setMatricule}
      dat_naiss={dat_naiss}
      setDat_naiss={setDat_naiss}
      Lieu_naiss={Lieu_naiss}
      setLieu_naiss={setLieu_naiss}
      date_recrut={date_recrut}
      setDate_recrut={setDate_recrut}
      grade={grade}
      setGrade={setGrade}
      date_grade={date_grade}
      setDate_grade={setDate_grade}
      Echelon={Echelon}
      setEchelon={setEchelon}
      Catégorie={Catégorie}
      setCatégorie={setCatégorie}
      division={division}
      setDivision={setDivision}
      position={position}
      setPosition={setPosition}
      faculte={faculte}
      setFaculte={setFaculte}
      debut_position={debut_position}
      setDebut_position={setDebut_position}
      fin_position={fin_position}
      setFin_position={setFin_position}
    />
  );
};

export default AddEmployePage;
