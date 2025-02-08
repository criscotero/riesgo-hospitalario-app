
interface Params{
    score: number
}

export default function HealthScore1({score} : Params) {

  const healthScore = Number(score) || 0;

  // Determine color and recommendations based on the score
  let color = "text-red-500";
  let recommendations = "Focus1 on improving your overall health with professional guidance.";
  if (healthScore > 30 && healthScore <= 50) {
    color = "text-orange-500";
    recommendations = "Consider small improvements in your daily routine, like balanced meals and light exercise.";
  } else if (healthScore > 50 && healthScore <= 70) {
    color = "text-yellow-500";
    recommendations = "You're doing well! Keep maintaining a healthy lifestyle with moderate exercise and a balanced diet.";
  } else if (healthScore > 70) {
    color = "text-green-500";
    recommendations = "Great job! Continue with your healthy habits and regular check-ups.";
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <div className="mb-6 text-center">
        <h1 className="text-2xl font-bold">Health Score</h1>
        <p className="text-gray-600">{recommendations}</p>
      </div>
      <div className="relative flex items-center justify-center w-40 h-40">
        <div className="absolute w-40 h-40 rounded-full border-8 border-gray-200"></div>
        <div
          className={`absolute w-40 h-40 rounded-full border-8 ${color} border-t-transparent animate-spin-slow`}
          style={{ transform: `rotate(${(healthScore / 100) * 360}deg)` }}
        ></div>
        <div className="absolute text-xl font-bold">{healthScore}</div>
      </div>
    </div>
  );
}

// Tailwind CSS animation for slow spinning (optional)
{/* <style jsx global>{`
  @tailwind base;
  @tailwind components;
  @tailwind utilities;

  @layer utilities {
    @keyframes spin-slow {
      from {
        transform: rotate(0deg);
      }
      to {
        transform: rotate(360deg);
      }
    }
    .animate-spin-slow {
      animation: spin-slow 5s linear infinite;
    }
  }
`}</style>
 */}