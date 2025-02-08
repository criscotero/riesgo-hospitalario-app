import { devtools, persist } from 'zustand/middleware'
import { FormFields } from '../types/form';
import { create } from 'zustand';

interface FormState {
    formData: FormFields;
    setFormData: (data: Partial<FormFields>) => void; // Allow updating specific fields
    clearFormData: () => void; // Reset form data to initial state
  }
  
  const initialFormData: FormFields = {
    firstName: '',
    lastName: '',
    identification: '',
    age: 0,
    r5height: 0,
    r5weight: 0,
    
    r5adla: 0,        // Default value (No difficulty with ADLs)
    r5adltot6: 0,     // Default value (No difficulty with ADLs)
    r5iadlfour: 0,    // Default value (No difficulty with IADLs)
    r5nagi8: 0,       // Default value (No difficulty with NAGI tasks)
    r5grossa: 0,      // Default value (No difficulty with gross motor tasks)
    r5mobilsev: 0,    // Default value (No difficulty with mobility tasks)
    r5uppermob: 0,    // Default value (No difficulty with upper body mobility)
    r5lowermob: 0,  // Default value (No difficulty with lower body mobility)

    r5fallnum: 0
  };
  
  
  export const useFormStore = create<FormState>()(
    devtools(
      persist(
        (set) => ({
          formData: initialFormData,
          setFormData: (data) =>
            set((state) => ({
              formData: { ...state.formData, ...data }, // Merge new data with existing formData
            })),
          clearFormData: () => set({ formData: initialFormData }),
        }),
        { name: 'form-store' }
      )
    )
  );

