
//import { useFormStore } from "@/app/store/formStore";
import { useFormStore } from "@/app/store/formStore";
import { useForm } from "react-hook-form";
interface Props {
    handleNext: () => void
  }
export default function GeneralInformation({ handleNext }:Props) {
  
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
      handleNext();
    
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <h2 className="text-xl font-semibold mb-4">General Information</h2>
      <div className="grid grid-cols-2 gap-4">
        {/* First Name */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">
            First Name
          </label>
          <input
            {...register("firstName", { required: "First name is required" })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.firstName ? "border-red-500" : "border-gray-300"
            }`}
            type="text"
            placeholder="Enter your first name"
          />
          {(errors.firstName != null) && (
            <p className="text-red-500">{`${errors.firstName.message}`}</p>
          )}
        </div>

        {/* Last Name */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">
            Last Name
          </label>
          <input
            {...register("lastName", { required: "Last name is required" })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.lastName ? "border-red-500" : "border-gray-300"
            }`}
            type="text"
            placeholder="Enter your last name"
          />
          {(errors.lastName != null) && (
            <p className="text-red-500">{`${errors.lastName.message}`}</p>
          )}
        </div>

        {/* Identification */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">
            Identification
          </label>
          <input
            {...register("identification", {
              required: "Identification is required",
            })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.identification ? "border-red-500" : "border-gray-300"
            }`}
            type="text"
            placeholder="Enter your ID"
          />
          {(errors.identification != null) && (
            <p className="text-red-500">{`${errors.identification.message}`}</p>
          )}
        </div>

        {/* Age */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">Age</label>
          <input
            {...register("age", {
              required: "Age is required",
              min: { value: 50, message: "Age must be equal or greater than 50" },
            })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.age ? "border-red-500" : "border-gray-300"
            }`}
            type="number"
            placeholder="Enter your age"
          />
          {(errors.age != null) && (
            <p className="text-red-500">{`${errors.age.message}`}</p>
          )}
        </div>

        {/* Height */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">
            Height (meters)
          </label>
          <input
            {...register("r5height", { required: "Height is required" })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.r5height ? "border-red-500" : "border-gray-300"
            }`}
            type="number"
            step="0.01"
            placeholder="Enter your height"
          />
          {(errors.r5height != null) && (
            <p className="text-red-500">{`${errors.r5height.message}`}</p>
          )}
        </div>

        {/* Weight */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">
            Weight (kg)
          </label>
          <input
            {...register("r5weight", { required: "Weight is required" })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.r5weight ? "border-red-500" : "border-gray-300"
            }`}
            type="number"
            step="0.01"
            placeholder="Enter your weight"
          />
          {(errors.r5weight != null) && (
            <p className="text-red-500">{`${errors.r5weight.message}`}</p>
          )}
        </div>

  
      </div>

        
        {/* Navigation Buttons */}
        <div className="flex justify-end mt-4">
        <button
          type="submit"
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
          Next
        </button>
      </div>
    </form>
  );
}