// pages/index.js
import React from "react";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
    <div className="bg-white shadow-lg rounded-lg p-8 max-w-4xl w-full">
      <h1 className="text-2xl font-bold mb-6 text-center">
        Hospitalization Prediction Form
      </h1>
  
      {/* Health Status Section */}
      <div className="mb-6 border border-gray-200 rounded-lg p-6 bg-gray-50">
        <h2 className="text-xl font-semibold mb-4">Health Status</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Self-report of health change
            </label>
            <select className="w-full border rounded-lg p-2 mt-1">
              <option>Somewhat worse</option>
              <option>Same</option>
              <option>Somewhat better</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Height in meters
            </label>
            <input
              type="number"
              className="w-full border rounded-lg p-2 mt-1"
              placeholder="0.00"
            />
          </div>
        </div>
      </div>
  
      {/* Cognitive Function Section */}
      <div className="mb-6 border border-gray-200 rounded-lg p-6 bg-gray-50">
        <h2 className="text-xl font-semibold mb-4">Cognitive Function</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Memory rating (1-10)
            </label>
            <input
              type="number"
              className="w-full border rounded-lg p-2 mt-1"
              placeholder="0"
            />
          </div>
        </div>
      </div>
  
      {/* Wealth Status Section */}
      <div className="mb-6 border border-gray-200 rounded-lg p-6 bg-gray-50">
        <h2 className="text-xl font-semibold mb-4">Wealth Status</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Number of health insurance plans
            </label>
            <input
              type="number"
              className="w-full border rounded-lg p-2 mt-1"
              placeholder="0"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Annual income (USD)
            </label>
            <input
              type="number"
              className="w-full border rounded-lg p-2 mt-1"
              placeholder="0.00"
            />
          </div>
        </div>
      </div>
  
      {/* Submit Button */}
      <div className="text-center">
        <button className="bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700">
          Submit
        </button>
      </div>
    </div>
  </div>
  );
}
