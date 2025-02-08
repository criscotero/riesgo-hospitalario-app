'use client'
import { useSearchParams } from "next/navigation";
import HealthScore from "../components/healthScore";



const HealthScorePage = () => {
  const searchParams = useSearchParams()
   const score = searchParams.get('score')
   const healthScore = Number(score)  || 0 ;
  return <HealthScore score={healthScore } />;
};

export default HealthScorePage;