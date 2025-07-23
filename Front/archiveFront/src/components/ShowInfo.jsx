import { useState, useEffect } from "react";
import { useParams, useLoaderData, useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import axios from "axios";
import EnseignantForm from "./reUsable/EnseignantForm";
import {
  FaUser,
  FaCalendarAlt,
  FaMapMarkerAlt,
  FaTransgender,
  FaIdCard,
  FaSave,
  FaEdit,
  FaTimes,
  FaAlignJustify,
  FaRegBuilding,
} from "react-icons/fa";
import Select from "./reUsable/Select";
import GRADES from "./reUsable/Grades";
import FACULTIES from "./reUsable/Faculties";
import FACULTIES_EMP from "./reUsable/Faculties_emp";
import POSITIONS from "./reUsable/Positions";
import { addYears, format } from "date-fns";
const Field = ({ label, icon, value, onChange, isEditing, type = "text" }) => (
  <div className="flex flex-col">
    <label className="flex items-center gap-2 text-blue-600  font-medium mb-1">
      {icon}
      {label}
    </label>
    {isEditing ? (
      <input
        type={type}
        value={value ?? ""}
        onChange={(e) => onChange(e.target.value)}
        className="bg-white border border-gray-300 px-3 py-2 rounded-md focus:ring-2 focus:ring-blue-400 outline-none"
      />
    ) : (
      <p className="bg-gray-100 border border-gray-200 text-right p-2 rounded-md">
        {value || "—"}
      </p>
    )}
  </div>
);

const ShowInfo = ({
  id,
  selectedEnseignant,
  setSelectedEnseignant,
  updateObj,
  type,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  //const FACUL = FACULTIES.push("المديرية");
  // console.log(FACUL);
  console.log(selectedEnseignant);
  let FAC = type === "enseignant" ? FACULTIES : FACULTIES;
  const handleSubmit = (e) => {
    e.preventDefault();
    updateObj(selectedEnseignant); //, id);

    //navigate(`/ens/${id}`);
    //    navigate(`/AllOperations/${id}`);
    toast.success("تم التحديث ينجاح");
    setIsEditing(false);
  };
  const handleObject = async () => {
    if (selectedEnseignant.position !== "في الخدمة")
      if (!selectedEnseignant.debut_position) {
        alert("أدخل بداية الوضغية");
        return;
      }
  };
  const handleFieldChange = (field, value) => {
    setSelectedEnseignant((prev) => {
      const updated = { ...prev, [field]: value };
      if (field === "position" && value === "في الخدمة") {
        updated.debut_position = null;
        updated.fin_position = null;
      }
      if (field === "position" && value !== "في الخدمة") {
        updated.debut_position = null;
      }

      if (field === "debut_position") {
        const debutDate = new Date(value);

        if (!isNaN(debutDate)) {
          let finDate = "";
          if (prev.position === "وضع تحت التصرف جمعوي") {
            finDate = format(addYears(debutDate, 2), "yyyy-MM-dd");
          } else if (prev.position === "وضع تحت التصرف بيداغوجي") {
            finDate = format(addYears(debutDate, 1), "yyyy-MM-dd");
          } else if (prev.position === "وضع تحت التصرف") {
            finDate = format(addYears(debutDate, 2), "yyyy-MM-dd");
          } else if (prev.position === "إستيداع قانوني") {
            finDate = format(addYears(debutDate, 5), "yyyy-MM-dd");
          } else if (prev.position === "إستيداع شخصي") {
            finDate = format(addYears(debutDate, 2), "yyyy-MM-dd");
          } else if (prev.position === "عطلة مرضية طويلة المدة") {
            finDate = format(addYears(debutDate, 3), "yyyy-MM-dd");
          } else if (prev.position === "إنتداب محدد") {
            finDate = format(addYears(debutDate, 4), "yyyy-MM-dd");
          } else if (
            prev.position === "إنتداب غ محدد" ||
            prev.position === "إنتداب" ||
            prev.position === "عطلة غ مدفوعة الأجر"
          ) {
            finDate = null;
          }

          updated.fin_position = finDate;
        } else {
          console.warn("Invalid debut_position date:", value);
        }
      }
      return updated;
    });
  };

  return (
    <form
      onSubmit={handleSubmit}
      //      {handleUpload}
      className="bg-white shadow-md rounded-xl p-2 max-w-4xl mx-auto  space-y-6"
    >
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-green-600  mb-3 flex items-center gap-2">
          {isEditing ? "✏️ تحديث معلومات الأستاذ" : "📄 معاينة معلومات الأستاذ"}
        </h2>
        <button
          type="button"
          onClick={() => setIsEditing(!isEditing)}
          className={`flex items-center gap-2 text-white font-semibold py-2 px-4 rounded transition
             ${
               isEditing
                 ? "bg-red-500 hover:bg-red-600"
                 : "bg-yellow-500 hover:bg-yellow-600"
             }`}
        >
          {isEditing ? <FaTimes /> : <FaEdit />}
          {isEditing ? "إلغاء" : "تحديث"}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Field
          label="الإسم"
          icon={<FaUser />}
          value={selectedEnseignant?.Nom || ""}
          onChange={(value) => handleFieldChange("Nom", value)}
          isEditing={isEditing}
        />
        <Field
          label="اللقب"
          icon={<FaUser />}
          value={selectedEnseignant?.Prénom || ""}
          onChange={(value) => handleFieldChange("Prénom", value)}
          isEditing={isEditing}
        />
        <Field
          label="تاريخ الميلاد"
          icon={<FaCalendarAlt />}
          type="date"
          value={selectedEnseignant.dat_naiss}
          onChange={(value) => handleFieldChange("dat_naiss", value)}
          isEditing={isEditing}
        />
        <Field
          label="مكان الميلاد"
          icon={<FaMapMarkerAlt />}
          value={selectedEnseignant.Lieu_naiss}
          onChange={(value) => handleFieldChange("Lieu_naiss", value)}
          isEditing={isEditing}
        />
        <Field
          label="النوع"
          icon={<FaTransgender />}
          value={selectedEnseignant.Type}
          onChange={(value) => handleFieldChange("Type", value)}
          isEditing={false} //{isEditing}
        />
        <Field
          label="الرقم الوطني"
          icon={<FaIdCard />}
          value={selectedEnseignant.NIN}
          onChange={(value) => handleFieldChange("NIN", value)}
          isEditing={isEditing}
        />
        <Field
          label="رقم ض إ"
          icon={<FaIdCard />}
          value={selectedEnseignant.matricule}
          onChange={(value) => handleFieldChange("matricule", value)}
          isEditing={isEditing}
        />
        <Field
          label="تاريخ التوظيف"
          icon={<FaCalendarAlt />}
          type="date"
          value={selectedEnseignant.date_recrut}
          onChange={(value) => handleFieldChange("date_recrut", value)}
          isEditing={isEditing}
        />
        {/*<Field
          label="الرتبة"
          icon={<FaUser />}
          value={selectedEnseignant.grade}
          onChange={(value) => handleFieldChange("grade", value)}
          isEditing={isEditing}
        />*/}

        <Select
          label={type === "contrat" ? "المنصب" : "الرتبة"}
          options={
            type === "enseignant"
              ? GRADES.ENS
              : type == "employe"
              ? GRADES.EMP
              : GRADES.CONTRAT
          }
          disabled={!isEditing}
          value={selectedEnseignant.grade}
          onChange={(value) => handleFieldChange("grade", value)}
        />

        <Field
          label="تاريخ الرتبة"
          icon={<FaCalendarAlt />}
          type="date"
          value={selectedEnseignant.date_grade}
          onChange={(value) => handleFieldChange("date_recrut", value)}
          isEditing={isEditing}
        />
        <Field
          label="الدرجة"
          icon={<FaAlignJustify />}
          value={selectedEnseignant.Echelon}
          onChange={(value) => handleFieldChange("Echelon", value)}
          isEditing={isEditing}
        />
        <Field
          label={type === "employe" ? "الفئة" : "الصنف"}
          icon={<FaAlignJustify />}
          value={selectedEnseignant.Catégorie}
          onChange={(value) => handleFieldChange("Catégorie", value)}
          isEditing={false}
        />
        {type === "employe" && (
          <Field
            label="الشعبة"
            icon={<FaAlignJustify />}
            value={selectedEnseignant.division}
            onChange={(value) => handleFieldChange("division", value)}
            isEditing={false}
          />
        )}
        <Select
          label="الكلية"
          options={type === "enseignant" ? FACULTIES : FACULTIES_EMP}
          disabled={!isEditing}
          value={selectedEnseignant.faculte}
          onChange={(value) => handleFieldChange("faculte", value)}
        />
        <Select
          label="الوضعية"
          options={
            type === "enseignant"
              ? POSITIONS.ENS
              : type == "employe"
              ? POSITIONS.EMP
              : POSITIONS.CONTRAT
          }
          disabled={!isEditing}
          value={selectedEnseignant.position}
          onChange={(value) => handleFieldChange("position", value)}
        />

        <Field
          label="بداية الوضعية"
          icon={<FaCalendarAlt />}
          type="date"
          value={selectedEnseignant.debut_position}
          onChange={
            (value) => {
              handleFieldChange("debut_position", value);
            }
            /*if (selectedEnseignant.position == "وضع تحت التصرف جمعوي") {
              const debutDate = new Date(selectedEnseignant.debut_position);
              const finDate = format(addYears(debutDate, 2));
              // "yyyy-MM-dd");
              handleFieldChange("fin_position", finDate);
            } else {
              handleFieldChange("fin_position", value);
            }
          }*/
          }
          isEditing={isEditing}
        />
        {/*<Field
          label="نهاية الوضعية"
          icon={<FaCalendarAlt />}
          type="date"
          value={selectedEnseignant.fin_position}
          onChange={(value) => handleFieldChange("fin_position", value)}
          isEditing={isEditing}
        />*/}

        <Field
          label="نهاية الوضعية"
          icon={<FaCalendarAlt />}
          type="date"
          value={selectedEnseignant.fin_position}
          onChange={(value) => handleFieldChange("fin_position", value)}
          isEditing={false}
        />
      </div>

      {isEditing && (
        <div className="flex justify-end mt-6">
          <button
            type="submit"
            onClick={handleObject}
            disabled={
              selectedEnseignant.position !== "في الخدمة" &&
              !selectedEnseignant.debut_position
            }
            className="bg-blue-600 hover:bg-blue-700 text-white font-semibold flex items-center gap-2 px-6 py-2 rounded-lg transition"
          >
            <FaSave />
            حفظ
          </button>
        </div>
      )}
    </form>
  );
};

export default ShowInfo;
