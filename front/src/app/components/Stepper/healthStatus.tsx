import { useFormStore } from "@/app/store/formStore";
import { useForm } from "react-hook-form";
import { 
  r5adlaOptions, 
  r5adltot6Options, 
  r5iadlfourOptions, 
  r5nagi8Options,
  r5grossaOptions,
  r5mobilsevOptions,
  r5uppermobOptions,
  r5lowermobOptions
} from '../../types/utils';  // Make sure to use the correct path
interface Props {
  handleNext: () => void
  handleBack: () => void
}


export default function HealthStatus({ handleBack, handleNext }: Props) {
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
     
     {/*  <div>
        <label className="block text-sm font-medium text-gray-700">
          Self-report of health change in the last 12 months
        </label>
        <select
          {...register("healthChange", { required: "Health change is required" })}
          className={`w-full px-3 py-2 border rounded-lg ${
            errors.healthChange ? "border-red-500" : "border-gray-300"
          }`}
        >
          <option value="somewhatWorse">Somewhat worse</option>
          <option value="same">Same</option>
          <option value="somewhatBetter">Somewhat better</option>
        </select>
        {(errors.healthChange != null) && (
            <p className="text-red-500">{`${errors.healthChange.message}`}</p>
          )}
      </div> */}
 
      <div className="grid grid-cols-1 gap-4 mt-4">
       
        <div>
          <label className="block text-sm font-medium text-gray-700">
           <b>ADLs Difficulty (Activities of Daily Living)</b> include: Bathing, Dressing, Eating, Toileting, Transferring (e.g., getting in/out of bed)
          </label>
          <select
            {...register("r5adla", { required: "ADL selection is required" })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.r5adla ? "border-red-500" : "border-gray-300"
            }`}
          >
            {r5adlaOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          {(errors.r5adla != null) && (
            <p className="text-red-500">{`${errors.r5adla.message}`}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
          <b>ADLs (6 tasks)</b> 1.Bathing 2.Dressing 3.Eating 4.Toileting (using the restroom) 5.Transferring 6.Continence (control over bladder/bowel function)
          </label>
          <select
            {...register("r5adltot6", { required: "ADL selection is required" })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.r5adltot6 ? "border-red-500" : "border-gray-300"
            }`}
          >
            {r5adltot6Options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          {(errors.r5adltot6 != null) && (
            <p className="text-red-500">{`${errors.r5adltot6.message}`}</p>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 mt-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
          <b>IADLs (Instrumental Activities of Daily Living)</b> 1.Managing medications 2.Shopping for groceries and essentials 3.Handling transportation 4.Managing finances (paying bills, budgeting)
          </label>
          <select
            {...register("r5iadlfour", { required: "IADL selection is required" })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.r5iadlfour ? "border-red-500" : "border-gray-300"
            }`}
          >
            {r5iadlfourOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          {(errors.r5iadlfour != null) && (
            <p className="text-red-500">{`${errors.r5iadlfour.message}`}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            <b>NAGI Tasks Difficulty</b> Assesses physical function limitations and includes (Lifting or carrying heavy objects,Pushing or pulling large objects,Standing for long periods,Sitting for long periods
          </label>
          <select
            {...register("r5nagi8", { required: "NAGI task selection is required" })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.r5nagi8 ? "border-red-500" : "border-gray-300"
            }`}
          >
            {r5nagi8Options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          {(errors.r5nagi8 != null) && (
            <p className="text-red-500">{`${errors.r5nagi8.message}`}</p>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 mt-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            <b>Gross Motor Tasks Difficulty </b>Assesses major movement-related limitations. (Walking,Running,Jumping,Balancing,Climbing stairs)
)
          </label>
          <select
            {...register("r5grossa", { required: "Gross motor task selection is required" })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.r5grossa ? "border-red-500" : "border-gray-300"
            }`}
          >
            {r5grossaOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          {(errors.r5grossa != null) && (
            <p className="text-red-500">{`${errors.r5grossa.message}`}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            <b>Mobility Severity Difficulty</b> Assesses difficulties in essential mobility functions.(Standing up from a chair
Walking short or long distances,Climbing stairs,Moving around indoors and outdoors.)
          </label>
          <select
            {...register("r5mobilsev", { required: "Mobility severity selection is required" })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.r5mobilsev ? "border-red-500" : "border-gray-300"
            }`}
          >
            {r5mobilsevOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          {(errors.r5mobilsev != null) && (
            <p className="text-red-500">{`${errors.r5mobilsev.message}`}</p>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 mt-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            <b>Upper Body Mobility Difficulty</b>Assesses difficulties in upper body movement.(Like arms, shoulders, and torso)
          </label>
          <select
            {...register("r5uppermob", { required: "Upper body mobility selection is required" })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.r5uppermob ? "border-red-500" : "border-gray-300"
            }`}
          >
            {r5uppermobOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          {(errors.r5uppermob != null) && (
            <p className="text-red-500">{`${errors.r5uppermob.message}`}</p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            <b>Lower Body Mobility Difficulty</b> Assesses difficulties in lower body movement. (hips, legs, knees, and feet)
          </label>
          <select
            {...register("r5lowermob", { required: "Lower body mobility selection is required" })}
            className={`w-full px-3 py-2 border rounded-lg ${
              errors.r5lowermob ? "border-red-500" : "border-gray-300"
            }`}
          >
            {r5lowermobOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          {(errors.r5lowermob != null) && (
            <p className="text-red-500">{`${errors.r5lowermob.message}`}</p>
          )}
        </div>
      </div>

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
          Next
        </button>
      </div>
    </form>
  );
}
