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
      <h2 className="text-xl font-semibold mb-4">Health Status</h2>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          Self-report of health change
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
      </div>

      <div className="grid grid-cols-2 gap-4 mt-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            ADLs Difficulty
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
            ADLs (6 tasks)
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

      <div className="grid grid-cols-2 gap-4 mt-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            IADLs Difficulty
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
            NAGI Tasks Difficulty
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

      <div className="grid grid-cols-2 gap-4 mt-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Gross Motor Tasks Difficulty
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
            Mobility Severity Difficulty
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

      <div className="grid grid-cols-2 gap-4 mt-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            Upper Body Mobility Difficulty
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
            Lower Body Mobility Difficulty
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
