interface ResultsProps {
  title: string;
  data: any;
}

const Results: React.FC<ResultsProps> = ({ title, data }) => {
  const renderData = (data: any) => {
    if (Array.isArray(data)) {
      return (
        <div className="overflow-x-auto w-full">
          <table className="table-auto w-full border-collapse border border-gray-300 rounded-lg shadow">
            <thead>
              <tr className="bg-gray-100 text-gray-700">
                {Object.keys(data[0] || {}).map((key) => (
                  <th
                    key={key}
                    className="border border-gray-300 px-4 py-2 text-left font-semibold"
                  >
                    {key.charAt(0).toUpperCase() + key.slice(1)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((item, index) => (
                <tr
                  key={index}
                  className={`${
                    index % 2 === 0 ? "bg-white" : "bg-gray-50"
                  } hover:bg-gray-100`}
                >
                  {Object.values(item).map((value, idx) => (
                    <td
                      key={idx}
                      className="border border-gray-300 px-4 py-2 text-gray-700"
                    >
                      {typeof value === "object" ? (
                        <span className="text-sm text-gray-500">
                          {JSON.stringify(value)}
                        </span>
                      ) : (
                        <span>{String(value)}</span>
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    } else if (typeof data === "object") {
      return (
        <div className="grid grid-cols-1 gap-6 w-full">
          {Object.entries(data).map(([key, value]) => (
            <div
              key={key}
              className="bg-gray-100 p-4 rounded-lg shadow border border-gray-300"
            >
              <h3 className="font-bold text-gray-700 mb-2">
                {key.charAt(0).toUpperCase() + key.slice(1)}
              </h3>
              <p className="text-gray-600">
                {typeof value === "object" ? (
                  <span className="text-sm text-gray-500">
                    {JSON.stringify(value)}
                  </span>
                ) : (
                  <span>{String(value)}</span>
                )}
              </p>
            </div>
          ))}
        </div>
      );
    } else {
      return (
        <p className="text-gray-600 text-center text-lg font-medium">{data}</p>
      );
    }
  };

  return (
    <div className="mt-6 p-6 bg-white shadow-lg rounded-lg flex flex-col mx-auto justify-center w-full max-w-4xl">
      <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">
        {title}
      </h2>
      {renderData(data)}
    </div>
  );
};

export default Results;
