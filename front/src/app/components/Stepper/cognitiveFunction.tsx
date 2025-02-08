export default function CognitiveFunction() {
    return (
      <div>
        <h2 className="text-xl font-semibold mb-4">Cognitive Function</h2>
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
    );
  }