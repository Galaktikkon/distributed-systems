import { useState } from "react";

interface InputFormProps {
  onFetch: (endpoint: string, location: string) => void;
}

const InputForm: React.FC<InputFormProps> = ({ onFetch }) => {
  const [location, setLocation] = useState<string>("");

  const handleSubmit = (endpoint: string) => {
    if (!location) {
      alert("Please enter a location.");
      return;
    }
    onFetch(endpoint, location);
  };

  return (
    <div className="my-4 flex flex-col gap-10 items-center">
      <input
        type="text"
        placeholder="Enter location (e.g., Warsaw, Poland)"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        className="border border-gray-300 rounded px-4 py-2 w-[300px] text-center"
      />
      <div className="flex flex-row gap-10">
        <button
          onClick={() => handleSubmit("weather")}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Get Weather
        </button>
        <button
          onClick={() => handleSubmit("air_quality")}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Get Air Quality
        </button>
        <button
          onClick={() => handleSubmit("pollen")}
          className="bg-yellow-600 text-white px-4 py-2 rounded hover:bg-yellow-700"
        >
          Get Pollen
        </button>
        <button
          onClick={() => handleSubmit("should_run")}
          className="bg-purple-600 text-white px-4 py-2 rounded hover:bg-purple-700"
        >
          Should I Run?
        </button>
      </div>
    </div>
  );
};

export default InputForm;
