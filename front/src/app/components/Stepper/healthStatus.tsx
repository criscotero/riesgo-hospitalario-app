export default function HealthStatus() {
    return (
      <div >
        {/* <h2 className="text-xl font-semibold mb-4">Health Status</h2> */}
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
    );
  }
