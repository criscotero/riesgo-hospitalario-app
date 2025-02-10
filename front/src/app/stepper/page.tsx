'use client'
import { useRouter } from 'next/navigation'
import { useState } from 'react';
import HealthStatus from '../components/Stepper/healthStatus';
import GeneralInformation from '../components/Stepper/generalInformation';
import { useFormStore } from '../store/formStore';
import Accident from '../components/Stepper/accident';
import { useMutation } from '@tanstack/react-query';
import { createPrediction } from '../services/prediction.service';
import Spinner from '../components/spinner';

export default function HospitalizationForm() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState(1);
  const { formData, setFormData,clearFormData } = useFormStore();
  
  const { mutate, status, isPending } = useMutation({
    mutationFn: createPrediction,
    onSuccess: (data) => {
      console.log('Mutation successful:', data);
    },
    onError: (error) => {
      console.error('Mutation error:', error);
    },
  });

  const handleNext = () => {
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1);
      console.log(formData)
    }
  };
    // Function to validate and move to next step
    const handleBack = () => {
      if (currentStep > 1) {
        setCurrentStep(currentStep - 1);
      }
    };
    const submitted = () => {
      console.dir(formData)
      mutate(formData);
      
    }
  const steps = [
    { id: 1, name: 'General Information', component: <GeneralInformation handleNext={handleNext} /> },
    { id: 2, name: 'Physical Health & Mobility', component: <HealthStatus handleBack={handleBack} handleNext={handleNext} /> },
    { id: 3, name: 'Accidents & Risk Factors', component: <Accident handleBack={handleBack} submitted={submitted} /> },


  ];




  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      {/* Single Form Container */}
      <div className={`bg-white shadow-lg rounded-lg p-8 max-w-4xl w-full ${isPending ? 'blur-sm' : ''}`}>
        {/* Fixed Title */}
        <h1 className="text-2xl font-bold mb-6 text-center">
          Hospitalization Prediction Form 
        </h1>

        {/* Fixed Stepper Header */}
        <div className="flex justify-between items-center w-full mb-8 relative">
          {steps.map((step) => (
            <div key={step.id} className="flex flex-col items-center z-10">
              {/* Step Circle */}
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  currentStep === step.id
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-600'
                }`}
              >
                {step.id}
              </div>
              {/* Step Name */}
              <span
                className={`mt-2 text-sm ${
                  currentStep === step.id ? 'text-blue-500' : 'text-gray-600'
                }`}
              >
                {step.name}
              </span>
            </div>
          ))}
          {/* Connecting Line */}
          <div className="absolute top-4 left-8 right-8 h-0.5 bg-gray-200 z-0"></div>
        </div>

        {/* Dynamic Form Content */}
        <div className="mb-8">
          {steps[currentStep - 1].component}
        </div>

     
      </div>
  {/* Show spinner while submitting */}
       {isPending && (
        <div className="absolute inset-0 flex items-center justify-center z-20">
          <Spinner />
        </div>
      )}
       
    </div>
  );
}

