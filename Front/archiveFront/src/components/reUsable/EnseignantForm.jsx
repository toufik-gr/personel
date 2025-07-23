import Select from "./Select";
import GRADES from "./Grades";
import FACULTIES from "./Faculties";
import POSITIONS from "./Positions";
import FACULTIES_EMP from "./Faculties_emp";
const EnseignantForm = ({
  type = type,
  title = title,
  gridCol = "md:grid-cols-2",
  onSubmit,
  Nom,
  setNom,
  Prénom,
  setPrénom,
  Type,
  setType,
  NIN,
  setNIN,
  matricule,
  setMatricule,
  dat_naiss,
  setDat_naiss,
  Lieu_naiss,
  setLieu_naiss,
  date_recrut,
  setDate_recrut,
  grade,
  setGrade,
  date_grade,
  setDate_grade,
  Echelon,
  setEchelon,
  Catégorie,
  setCatégorie,
  division,
  setDivision,
  position,
  setPosition,
  faculte,
  setFaculte,
  debut_position,
  setDebut_position,
  fin_position,
  setFin_position,
}) => {
  return (
    <form
      onSubmit={onSubmit}
      className="bg-white shadow-lg rounded-xl p-6 w-full max-w-5xl mx-auto space-y-4"
    >
      <h2 className="text-2xl font-bold text-blue-600 mb-4">🔄 {title} </h2>

      {/* Grid layout for fields */}
      <div className={`grid grid-cols-1  ${gridCol} gap-3`}>
        <Input label="الاسم" value={Nom} onChange={setNom} />
        <Input label="اللقب" value={Prénom} onChange={setPrénom} />
        <Input label="النوع" value={Type} onChange={setType} disabled={true} />
        <Input label="رقم التعريف الوطني" value={NIN} onChange={setNIN} />
        <Input
          label="الرقم الوظيفي"
          value={matricule}
          onChange={setMatricule}
        />
        <Input
          label="تاريخ الميلاد"
          type="date"
          value={dat_naiss}
          onChange={setDat_naiss}
        />
        <Input
          label="مكان الميلاد"
          value={Lieu_naiss}
          onChange={setLieu_naiss}
        />
        <Input
          label="تاريخ التوظيف"
          type="date"
          value={date_recrut}
          onChange={setDate_recrut}
        />

        <Select
          label="الرتبة"
          options={type == "enseignant" ? GRADES.ENS : GRADES.EMP}
          value={grade}
          onChange={setGrade}
        />
        <Input
          label="تاريخ الرتبة"
          type="date"
          value={date_grade}
          onChange={setDate_grade}
        />
        <Input label="الدرجة" value={Echelon} onChange={setEchelon} />
        <Input
          label={
            type == "enseignant" ? "الصنف" : type == "employe" ? "الفئة" : ""
          }
          value={Catégorie}
          onChange={setCatégorie}
        />
        {type === "employe" && (
          <Input label="الشعبة" value={division} onChange={setDivision} />
        )}
        <Select
          label="الكلية"
          options={type == "enseignant" ? FACULTIES : FACULTIES_EMP}
          value={faculte}
          onChange={setFaculte}
        />

        <Select
          label="الوضعية"
          options={type == "enseignant" ? POSITIONS.ENS : POSITIONS.EMP}
          value={position}
          onChange={setPosition}
        />
        <Input
          label="بداية الوضعية"
          type="date"
          value={debut_position}
          onChange={setDebut_position}
        />
        <Input
          label="نهاية الوضعية"
          type="date"
          value={fin_position}
          onChange={setFin_position}
        />
      </div>

      {/* Submit Button */}
      <div className="flex justify-end">
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition"
        >
          إضافة
        </button>
      </div>
    </form>
  );
};

// Reusable Input Component
const Input = ({ label, type = "text", value, onChange, disabled = false }) => (
  <div>
    <label className="block text-sm font-medium text-gray-700 mb-1">
      {label}
    </label>
    <input
      disabled={disabled}
      type={type}
      value={value ?? ""}
      onChange={(e) => onChange(e.target.value)}
      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none"
    />
  </div>
);

export default EnseignantForm;
