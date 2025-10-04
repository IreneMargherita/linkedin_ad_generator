import { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Card } from "@/components/ui/card";
import { Sparkles } from "lucide-react";

export interface AdFormData {
  companyUrl: string;
  productName: string;
  businessValue: string;
  audience: string;
  bodyText: string;
  footerText: string;
}

const STORAGE_KEY = "linkedin-ad-form-data";

const AdForm = () => {
  const navigate = useNavigate();
  const location = useLocation();
  
  // Initialize form data from localStorage or use empty defaults
  const getInitialFormData = (): AdFormData => {
    try {
      const savedData = localStorage.getItem(STORAGE_KEY);
      if (savedData) {
        return JSON.parse(savedData);
      }
    } catch (error) {
      console.error("Error loading saved form data:", error);
    }
    return {
      companyUrl: "",
      productName: "",
      businessValue: "",
      audience: "",
      bodyText: "",
      footerText: "",
    };
  };

  const [formData, setFormData] = useState<AdFormData>(getInitialFormData);

  // Load form data from location state if coming back from results page
  useEffect(() => {
    if (location.state && typeof location.state === 'object') {
      const stateData = location.state as AdFormData;
      setFormData(stateData);
      // Save to localStorage for persistence
      localStorage.setItem(STORAGE_KEY, JSON.stringify(stateData));
    }
  }, [location.state]);

  // Save form data to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(formData));
  }, [formData]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Save final form data to localStorage
    localStorage.setItem(STORAGE_KEY, JSON.stringify(formData));
    // Navigate to results page with form data
    navigate("/results", { state: formData });
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const clearForm = () => {
    setFormData({
      companyUrl: "",
      productName: "",
      businessValue: "",
      audience: "",
      bodyText: "",
      footerText: "",
    });
    localStorage.removeItem(STORAGE_KEY);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-primary/5 to-accent">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-12">
          <div className="flex items-center gap-3">
            <img src="/kalos-logo.svg" alt="Kalos" className="h-8" />
            <h1 className="text-2xl font-semibold text-foreground">
              LinkedIn Ad Generator
            </h1>
          </div>
        </div>

        {/* Form Card */}
        <Card className="p-8 shadow-lg border-primary/10">
          <div className="flex items-center gap-2 mb-6">
            <Sparkles className="h-6 w-6 text-primary" />
            <h2 className="text-xl font-semibold text-foreground">
              Create Your LinkedIn Ad Campaign
            </h2>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="companyUrl">Company URL</Label>
              <Input
                id="companyUrl"
                name="companyUrl"
                type="url"
                placeholder="https://example.com"
                value={formData.companyUrl}
                onChange={handleChange}
                required
                className="bg-background"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="productName">Product Name</Label>
              <Input
                id="productName"
                name="productName"
                placeholder="AI powered Email"
                value={formData.productName}
                onChange={handleChange}
                required
                className="bg-background"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="businessValue">Business Value</Label>
              <Input
                id="businessValue"
                name="businessValue"
                placeholder="Reply to Your Customers Faster"
                value={formData.businessValue}
                onChange={handleChange}
                required
                className="bg-background"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="audience">Target Audience</Label>
              <Input
                id="audience"
                name="audience"
                placeholder="Director of Sales, VP of Sales, Head of Sales"
                value={formData.audience}
                onChange={handleChange}
                required
                className="bg-background"
              />
              <p className="text-sm text-muted-foreground">
                Function + Title (e.g., Director of Sales, VP of Marketing)
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="bodyText">Body Text</Label>
              <Textarea
                id="bodyText"
                name="bodyText"
                placeholder="Context for your ad that appears before the image..."
                value={formData.bodyText}
                onChange={handleChange}
                required
                rows={5}
                className="bg-background"
              />
              <p className="text-sm text-muted-foreground">
                Text that will appear before the image in your ad
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="footerText">Footer Text (Call to Action)</Label>
              <Input
                id="footerText"
                name="footerText"
                placeholder="Boost Client Trust: Respond to Emails 3x Faster!"
                value={formData.footerText}
                onChange={handleChange}
                required
                className="bg-background"
              />
              <p className="text-sm text-muted-foreground">
                Call to action that appears after the image
              </p>
            </div>

            <div className="flex gap-3">
              <Button
                type="button"
                variant="outline"
                onClick={clearForm}
                className="flex-1"
              >
                Clear Form
              </Button>
              <Button
                type="submit"
                size="lg"
                className="flex-1 bg-primary hover:bg-primary/90 text-primary-foreground font-medium"
              >
                Generate Ad Images
              </Button>
            </div>
          </form>
        </Card>
      </div>
    </div>
  );
};

export default AdForm;
