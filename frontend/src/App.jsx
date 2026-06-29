import { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleAnalyze = async () => {
    if (!file) return alert("Please select a file first!");

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      alert("Server Response: " + response.data.message);
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Upload failed! Make sure your Flask server is running.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-white shadow-lg p-4">
        <h1 className="text-2xl font-bold text-blue-600">ThreadCounty</h1>
      </nav>

      {/* Main Content */}
      <main className="p-8">
        <h2 className="text-3xl font-semibold text-center">AI-Powered Textile Inspection</h2>
        <p className="text-center mt-4 text-gray-600">Upload your fabric image to get instant AI analysis.</p>

        {/* Upload Section */}
        <div className="mt-10 max-w-md mx-auto bg-white p-6 rounded-lg shadow-md text-center">
          <input 
            type="file" 
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg" 
            onChange={handleFileChange} 
          />
          <button 
            className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
            onClick={handleAnalyze}
          >
            Analyze Fabric
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;