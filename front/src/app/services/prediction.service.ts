import axios from "axios"
import { FormFields } from "../types/form"


  
  export async function createPrediction(form: FormFields) {
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/model/predict`,
        form
      )
  
      // Check if the response status code is within the 2xx range to ensure success.
      if (response.status >= 200 && response.status < 300) {
        return response.data // Return the data from the response.
      } else {
        throw new Error(`Request failed with status ${response.status}`)
      }
    } catch (error) {
      // Handle any errors, e.g., network issues, API errors, etc.
      console.error('Error creating post:', error)
      throw error // Re-throw the error for higher-level error handling.
    }
  }