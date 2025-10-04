import { AdFormData } from "@/pages/AdForm";

const API_BASE_URL = "http://localhost:8000/api/ads";

export interface ImageGenerationResult {
  success: boolean;
  imagePath?: string;
  error?: string;
}

export const generateAdImage = async (
  formData: AdFormData,
  style: string,
  imageNumber: number
): Promise<ImageGenerationResult> => {
  try {
    // Call the backend API to generate the image
    const response = await fetch(`${API_BASE_URL}/generate-image`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        formData,
        style,
        imageNumber,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error generating image:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Failed to generate image",
    };
  }
};

export const getStylePrompts = () => [
  "minimalist and clean with bold typography",
  "vibrant and colorful with modern gradient",
  "professional corporate style with subtle colors",
  "tech-focused with geometric patterns",
  "elegant and sophisticated with premium feel",
];
