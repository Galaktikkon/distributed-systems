import { useState } from "react";
import InputForm from "./components/InputForm";
import Results from "./components/Results";

interface ResultsData {
  title: string;
  data: any;
}

const App: React.FC = () => {
  const [results, setResults] = useState<ResultsData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async (endpoint: string, location: string) => {
    setError(null);
    setResults(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/${endpoint}?location=${encodeURIComponent(
          location
        )}`
      );
      if (!response.ok) {
        throw new Error(await response.text());
      }
      const data = await response.json();
      setResults({ title: endpoint.replace("_", " ").toUpperCase(), data });
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <section className="bg-gray-800 min-h-screen min-w-screen flex items-center justify-center">
      <div className="w-full flex flex-col">
        <h1 className="text-9xl font-bold text-center">RunAir</h1>
        <InputForm onFetch={fetchData} />
        {error && (
          <div className="flex justify-center items-center">
            <p className="text-red-600 font-bold text-center">{error}</p>
          </div>
        )}
        {results && <Results title={results.title} data={results.data} />}
      </div>
    </section>
  );
};

export default App;
