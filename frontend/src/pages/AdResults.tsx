import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Download, ArrowLeft, Loader2 } from "lucide-react";
import { AdFormData } from "./AdForm";
import { toast } from "sonner";
import { generateAdImage, getStylePrompts } from "@/lib/imageGenerator";

interface GeneratedImage {
  id: number;
  prompt: string;
  imageUrl: string | null;
  isGenerating: boolean;
  modificationPrompt: string;
}

const AdResults = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const formData = location.state as AdFormData;
  const [images, setImages] = useState<GeneratedImage[]>([]);

  useEffect(() => {
    if (!formData) {
      navigate("/");
      return;
    }

    const stylePrompts = getStylePrompts();

    // Initialize 5 image slots
    const initialImages: GeneratedImage[] = stylePrompts.map((style, index) => ({
      id: index + 1,
      prompt: style,
      imageUrl: null,
      isGenerating: true,
      modificationPrompt: "",
    }));

    setImages(initialImages);

    // Generate images sequentially with delays
    initialImages.forEach((img, index) => {
      setTimeout(() => generateImage(img.id, img.prompt), index * 1500);
    });
  }, [formData, navigate]);

  const generateImage = async (imageId: number, stylePrompt: string) => {
    try {
      toast.info(`Generating image ${imageId}...`);

      const result = await generateAdImage(formData, stylePrompt, imageId);

      if (result.success && result.imagePath) {
        setImages((prev) =>
          prev.map((img) =>
            img.id === imageId
              ? { ...img, imageUrl: result.imagePath, isGenerating: false }
              : img
          )
        );
        toast.success(`Image ${imageId} generated!`);
      } else {
        throw new Error(result.error || "Failed to generate image");
      }
    } catch (error) {
      console.error("Error generating image:", error);
      setImages((prev) =>
        prev.map((img) =>
          img.id === imageId ? { ...img, isGenerating: false } : img
        )
      );
      toast.error(`Failed to generate image ${imageId}`);
    }
  };

  const handleModify = async (imageId: number) => {
    const image = images.find((img) => img.id === imageId);
    if (!image || !image.modificationPrompt.trim()) {
      toast.error("Please enter modification instructions");
      return;
    }

    const modifiedPrompt = `${image.prompt}. Modified with: ${image.modificationPrompt}`;

    setImages((prev) =>
      prev.map((img) =>
        img.id === imageId ? { ...img, isGenerating: true } : img
      )
    );

    await generateImage(imageId, modifiedPrompt);
    
    // Clear the modification prompt after regenerating
    setImages((prev) =>
      prev.map((img) =>
        img.id === imageId ? { ...img, modificationPrompt: "" } : img
      )
    );
  };

  const handleDownload = async (imageId: number) => {
    const image = images.find((img) => img.id === imageId);
    if (!image?.imageUrl) return;

    try {
      // Fetch the image as a blob
      const response = await fetch(image.imageUrl);
      const blob = await response.blob();
      
      // Create a temporary URL for the blob
      const blobUrl = URL.createObjectURL(blob);
      
      // Create a temporary link and trigger download
      const link = document.createElement("a");
      link.href = blobUrl;
      link.download = `linkedin-ad-${formData.productName.replace(/\s+/g, '-').toLowerCase()}-${imageId}.png`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      // Clean up the blob URL
      URL.revokeObjectURL(blobUrl);
      
      toast.success(`Image ${imageId} downloaded!`);
    } catch (error) {
      console.error("Download error:", error);
      toast.error("Failed to download image");
    }
  };

  if (!formData) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-primary/5 to-accent">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => navigate("/")}
              className="gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back
            </Button>
            <div className="flex items-center gap-3">
              <img src="/kalos-logo.svg" alt="Kalos" className="h-8" />
              <h1 className="text-2xl font-semibold text-foreground">
                Generated LinkedIn Ads
              </h1>
            </div>
          </div>
        </div>

        {/* Campaign Info */}
        <Card className="p-6 mb-8 bg-card/50 backdrop-blur border-primary/10">
          <h2 className="text-lg font-semibold mb-4 text-foreground">
            Campaign Details
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Company URL */}
            <div className="space-y-1">
              <p className="text-sm font-medium text-foreground">Company URL</p>
              <p className="text-sm text-muted-foreground break-all">
                {formData.companyUrl || "Not provided"}
              </p>
            </div>
            
            {/* Product Name */}
            <div className="space-y-1">
              <p className="text-sm font-medium text-foreground">Product Name</p>
              <p className="text-sm text-muted-foreground">
                {formData.productName || "Not provided"}
              </p>
            </div>
            
            {/* Business Value */}
            <div className="space-y-1">
              <p className="text-sm font-medium text-foreground">Value Proposition</p>
              <p className="text-sm text-muted-foreground">
                {formData.businessValue || "Not provided"}
              </p>
            </div>
            
            {/* Target Audience */}
            <div className="space-y-1">
              <p className="text-sm font-medium text-foreground">Target Audience</p>
              <p className="text-sm text-muted-foreground">
                {formData.audience || "Not provided"}
              </p>
            </div>
            
            {/* Body Text */}
            <div className="space-y-1 md:col-span-2">
              <p className="text-sm font-medium text-foreground">Body Text</p>
              <p className="text-sm text-muted-foreground">
                {formData.bodyText || "Not provided"}
              </p>
            </div>
            
            {/* Footer Text */}
            <div className="space-y-1 md:col-span-2">
              <p className="text-sm font-medium text-foreground">Footer Text (CTA)</p>
              <p className="text-sm text-muted-foreground">
                {formData.footerText || "Not provided"}
              </p>
            </div>
          </div>
        </Card>

        {/* Generated Images */}
        <div className="space-y-8">
          {images.map((image) => (
            <Card
              key={image.id}
              className="p-6 shadow-lg border-primary/10 bg-card"
            >
              <div className="flex flex-col lg:flex-row gap-6">
                {/* Image Display */}
                <div className="flex-1">
                  <div className="relative bg-muted rounded-lg overflow-hidden aspect-[1O24/1024]">
                    {image.isGenerating ? (
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="text-center">
                          <Loader2 className="h-12 w-12 animate-spin text-primary mx-auto mb-4" />
                          <p className="text-sm text-muted-foreground">
                            Generating image {image.id}...
                          </p>
                        </div>
                      </div>
                    ) : image.imageUrl ? (
                      <img
                        src={image.imageUrl}
                        alt={`LinkedIn Ad ${image.id}`}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="absolute inset-0 flex items-center justify-center">
                        <p className="text-sm text-muted-foreground">
                          Failed to generate image
                        </p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Controls */}
                <div className="lg:w-80 space-y-4">
                  <div>
                    <h3 className="font-semibold mb-2 text-foreground">
                      Image {image.id}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                      LinkedIn Ad Size (1024×1024)
                    </p>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-medium text-foreground">
                      Modify Image
                    </label>
                    <Input
                      placeholder="E.g., make it darker, add more blue, change style..."
                      value={image.modificationPrompt}
                      onChange={(e) =>
                        setImages((prev) =>
                          prev.map((img) =>
                            img.id === image.id
                              ? { ...img, modificationPrompt: e.target.value }
                              : img
                          )
                        )
                      }
                      disabled={image.isGenerating}
                      className="bg-background"
                    />
                    <Button
                      onClick={() => handleModify(image.id)}
                      disabled={
                        image.isGenerating || !image.modificationPrompt.trim()
                      }
                      className="w-full"
                      variant="outline"
                    >
                      {image.isGenerating ? (
                        <>
                          <Loader2 className="h-4 w-4 animate-spin mr-2" />
                          Regenerating...
                        </>
                      ) : (
                        "Regenerate with Changes"
                      )}
                    </Button>
                  </div>

                  <Button
                    onClick={() => handleDownload(image.id)}
                    disabled={!image.imageUrl || image.isGenerating}
                    className="w-full bg-primary hover:bg-primary/90 text-primary-foreground"
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Download Image
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdResults;
