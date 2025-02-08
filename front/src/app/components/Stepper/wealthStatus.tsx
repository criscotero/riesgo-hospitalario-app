export default function WealthStatus() {
    return (
      <div>
        <h2 className="text-xl font-semibold mb-4">Wealth Status</h2>
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
    );
  }