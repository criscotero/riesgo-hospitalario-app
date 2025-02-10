interface Params {
    score: number;
    classType: number;
  }
  
  const HealthScore = ({ score, classType}: Params) => {
    const healthScore = Number(score) || 0;
  
    // Determine the color based on className
    const getColor = (className: number) => {
      return className === 0 ? "green" : "red";
    };
  
    // Determine health recommendations based on className and score
    const getRecommendations = (className: number, /* score: number */) => {
      if (className === 0) {
        return "You are in good health! Keep maintaining a healthy lifestyle to reduce any potential risks.";
      } else {
      /*   if (score <= 30)
          return "Your health risk is high. Consider consulting a healthcare professional immediately.";
        if (score <= 50) */
          return "Your health condition needs attention. Focus on improving your lifestyle and monitoring your health closely.";
/*         if (score <= 70)
          return "You are doing okay, but there's still room for improvement. Stay focused on your health goals.";
        return "You're on the right track! Continue working on your health and monitor your progress."; */
      }
    };
  
    const color = getColor(classType);
    const recommendations = getRecommendations(classType);
  
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
        <h1 className="text-2xl font-semibold mb-4 text-gray-800">
          {classType === 0 ? "You have a low risk of hospitalization." : "Your health risk level needs attention."}
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
            <span className="text-4xl font-bold">{healthScore}%</span>
          </div>
        </div>
        <div className="mt-8 p-4 bg-white rounded-lg shadow-md">
          <p className="text-lg text-gray-700">{recommendations}</p>
        </div>
      </div>
    );
  };
  
  export default HealthScore;
  