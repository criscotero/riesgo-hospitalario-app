'use client'
import { useRouter } from 'next/navigation'
import { useState } from 'react';
import HealthStatus from '../components/Stepper/healthStatus';
import CognitiveFunction from '../components/Stepper/cognitiveFunction';
import WealthStatus from '../components/Stepper/wealthStatus';
import GeneralInformation from '../components/Stepper/generalInformation';
import { useFormStore } from '../store/formStore';

export default function HospitalizationForm() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState(1);
  const { formData, setFormData } = useFormStore();

  const handleNext = () => {
    // Update form data with the current form values
    //setFormData((prevData: unknown) => ({ ...prevData, ...formValues }));
     //console.log(formValues)
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1);
    }
  };
  const steps = [
    { id: 1, name: 'General Information', component: <GeneralInformation handleNext={handleNext} /> },
    { id: 2, name: 'Health Status', component: <HealthStatus /> },
    { id: 3, name: 'Cognitive Function', component: <CognitiveFunction /> },
    { id: 4, name: 'Wealth Status', component: <WealthStatus /> },

  ];

  const submitted = () => {
    router.push(`/score?score=70`);
  }
  // Function to validate and move to next step
  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      {/* Single Form Container */}
      <div className="bg-white shadow-lg rounded-lg p-8 max-w-4xl w-full">
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
    </div>
  );
}

// Step 1: Health Status
/* function HealthStatus() {
  return (
    <div >
      <h2 className="text-xl font-semibold mb-4">Health Status</h2>
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
} */

// Step 2: Cognitive Function
/* function CognitiveFunction() {
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
} */

// Step 3: Wealth Status
/* function WealthStatus() {
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
} */