'use client'
import { useSearchParams } from "next/navigation";
import HealthScore from "../components/healthScore";




const HealthScorePage = () => {
  const searchParams = useSearchParams()
   const score = searchParams.get('score')
   const className = searchParams.get('class')
   const healthScore = Number(score)  || 0 ;
   const classType= Number(className)  || 0 ;
  return <HealthScore score={healthScore} classType={classType} />;
};

export default HealthScorePage;