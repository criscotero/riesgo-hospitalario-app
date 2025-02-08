interface Params {
    score: number;
  }
  
  const HealthScore = ({ score }: Params) => {
    const healthScore = Number(score) || 0;
  
    // Determine the color based on the score
    const getColor = (score: number) => {
      if (score <= 30) return "red";
      if (score <= 50) return "orange";
      if (score <= 70) return "yellow";
      return "green";
    };
  
    // Determine health recommendations based on the score
    const getRecommendations = (score: number) => {
      if (score <= 30)
        return "Consider consulting a healthcare professional for a comprehensive health checkup.";
      if (score <= 50)
        return "Focus on improving your diet and incorporating regular exercise into your routine.";
      if (score <= 70)
        return "You are on the right track, but there is room for improvement. Keep up the good work!";
      return "Great job! Maintain your healthy lifestyle and continue to monitor your health.";
    };
  
    const color = getColor(healthScore);
    const recommendations = getRecommendations(healthScore);
  
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
        <h1 className="text-2xl font-semibold mb-4 text-gray-800">
          Your overall score is
        </h1>
        <div className="relative w-64 h-64">
          <div
            className="absolute w-full h-full rounded-full"
            style={{
              background: `conic-gradient(${color} ${
                healthScore * 3.6
              }deg, #e5e7eb ${healthScore * 3.6}deg)`, // 3.6 converts score (0-100) to degrees
            }}
          ></div>
          <div className="absolute inset-4 bg-gray-100 rounded-full"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-4xl font-bold">{healthScore}</span>
          </div>
        </div>
        <div className="mt-8 p-4 bg-white rounded-lg shadow-md">
          <p className="text-lg text-gray-700">{recommendations}</p>
        </div>
      </div>
    );
  };
  
  export default HealthScore;
  