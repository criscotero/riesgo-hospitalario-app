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
    r5bmi: 0,
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

