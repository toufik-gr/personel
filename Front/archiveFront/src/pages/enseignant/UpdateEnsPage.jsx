import { useState, useEffect } from "react";
import { MdEventSeat } from "react-icons/md";
import { useParams, useLoaderData, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import axios from "axios";
import EnseignantForm from "../../components/reUsable/EnseignantForm";

const UpdateEnsPage = ({ updateEns }) => {
  const [Nom, setNom] = useState("");
  const [Prénom, setPrénom] = useState("");
  const [Type, setType] = useState("");
  const [NIN, setNIN] = useState("");
  const [matricule, setMatricule] = useState("");
  const [dat_naiss, setDat_naiss] = useState("");
  const [Lieu_naiss, setLieu_naiss] = useState("");
  const [date_recrut, setDate_recrut] = useState("");
  const [grade, setGrade] = useState("");
  const [date_grade, setDate_grade] = useState("");
  const [Echelon, setEchelon] = useState("");
  const [Catégorie, setCatégorie] = useState("");
  const [position, setPosition] = useState("");
  const [faculte, setFaculte] = useState("");
  const [debut_position, setDebut_position] = useState("");
  const [fin_position, setFin_position] = useState("");

  const { id } = useParams();
  const navigate = useNavigate();
  useEffect(() => {
    axios
      .get(`http://127.0.0.1:8000/enseign/ens/${id}/`)
      .then((res) => {
        // console.log(res.data);
        setNom(res.data.Nom);
        setPrénom(res.data.Prénom);
        setType(res.data.Type);
        setNIN(res.data.NIN);
        setMatricule(res.data.matricule);
        setDat_naiss(res.data.dat_naiss);
        setLieu_naiss(res.data.Lieu_naiss);
        setDate_recrut(res.data.date_recrut);
        setGrade(res.data.grade);
        setDate_grade(res.data.date_grade);
        setEchelon(res.data.Echelon);
        setCatégorie(res.data.Catégorie);
        setPosition(res.data.position);
        setFaculte(res.data.faculte);
        setDebut_position(res.data.debut_position);
        setFin_position(res.data.fin_position);
        console.log(res.data);
      })
      .catch((err) => {
        console.log(err.message);
      });
  }, [id]);

  const updateEnsObject = {
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
    position: position,
    faculte: faculte,
    debut_position: debut_position,
    fin_position: fin_position,
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // if (!title && !body && !category) return;
    updateEns(updateEnsObject, id);

    //navigate(`/ens/${id}`);
    navigate(`/AllOperations/${id}`);
    toast.success("تم التحديث ينجاح");
  };

  return (
    <EnseignantForm
      title="تحديث بيانات الأستاذ"
      gridCol="md:grid-cols-3"
      onSubmit={handleSubmit}
      Nom={Nom}
      setNom={setNom}
      Prénom={Prénom}
      setPrénom={setPrénom}
      Type={Type}
      setType={setType}
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

export default UpdateEnsPage;
