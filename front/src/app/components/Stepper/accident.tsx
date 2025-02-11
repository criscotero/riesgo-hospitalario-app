
//import { useFormStore } from "@/app/store/formStore";
import { useFormStore } from "@/app/store/formStore";
import { useForm } from "react-hook-form";
interface Props {
    handleBack: () => void
    submitted: () => void
  }
export default function Accident({ handleBack, submitted }:Props) {
  
  const { formData, setFormData } = useFormStore();
  const {
    register,
    handleSubmit,
    formState: { errors },
    getValues,
  } = useForm();


  const onSubmit = () => {
    const formValues = getValues();
    setFormData({
        ...formData,
        ...formValues,
      });
      submitted();
    
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
     
      <div className="grid grid-cols-2 gap-4">
     


        {/* Age */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">Number of falls in the last two years</label>
          <input
            {...register("r5fallnum", {
              required: "Number of falls is required",
              min: { value: 0, message: "Age must be greater or equal than 0" },
            })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.r5fallnum ? "border-red-500" : "border-gray-300"
            }`}
            type="number"
            placeholder="Enter number of falls"
          />
          {(errors.r5fallnum != null) && (
            <p className="text-red-500">{`${errors.r5fallnum.message}`}</p>
          )}
        </div>

     

  
      </div>

        
        {/* Navigation Buttons */}
        <div className="mt-6 flex justify-between">
        <button
          type="button"
          onClick={handleBack}
          className="px-4 py-2 bg-gray-300 text-white rounded-lg"
        >
          Back
        </button>
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded-lg"
        >
          Submit
        </button>
      </div>
    </form>
  );
}