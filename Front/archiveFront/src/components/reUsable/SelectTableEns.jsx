// components/reUsable/TableSelect.jsx
const SelectTableEns = ({
  label,
  value,
  placeholder = "--",
  options,
  onChange,
}) => {
  return (
    <div className="w-full max-w-xs">
      <label className="block mb-1 text-sm font-medium text-gray-700">
        {label}
      </label>
      <select
        value={value}
        onChange={onChange}
        //className="border border-gray-300 rounded px-3 py-2 bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent w-full"
        className="border border-gray-300 rounded px-3 py-2 bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent w-full max-w-xs"
      >
        <option value="">{placeholder}</option>
        {options.map((opt, index) => (
          <option key={index} value={opt}>
            {opt}
          </option>
        ))}
      </select>
    </div>
  );
};

export default SelectTableEns;
