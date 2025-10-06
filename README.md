# LinkedIn Ad Generator

A full-stack application that generates professional LinkedIn advertisements using AI. Built with React (TypeScript) frontend and FastAPI (Python) backend.

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API Key

### Backend Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the `backend/` directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:8000`

## 🏗️ Technical Approach

### Architecture Overview
I structured this project using a clean, layered architecture that prioritizes maintainability and testability. The backend follows a traditional MVC pattern with FastAPI, where I separated concerns into distinct layers: routes handle HTTP requests, controllers manage business logic, services contain core functionality, and DTOs define data contracts. I implemented dependency injection using FastAPI's built-in system, creating factory functions that wire together services and their dependencies, making the code highly testable and allowing easy swapping of components. The frontend uses React with TypeScript for type safety, and I designed it to communicate with the backend through a clean API layer. I organized the codebase into logical modules - prompts are separated into their own files for maintainability, interfaces define contracts for AI providers, and the project structure mirrors the architectural layers. This approach balances simplicity with extensibility, allowing the application to grow while maintaining clear boundaries between components and making it easy to add new features or swap out AI providers in the future.

### Technology Stack
- **Frontend**: React with TypeScript
- **Backend**: FastAPI (Python)
- **AI Provider**: OpenAI GPT-4o and DALL-E
- **UI Framework**: Built with lovable.ai
- **IDE**: Cursor

### Project Structure

#### Frontend (`frontend/src/`)
- **`pages/`**: Main application pages
  - `AdForm.tsx` - Company details form
  - `AdResults.tsx` - Generated images display
- **`lib/`**: API integration layer
- **`components/`**: Reusable UI components

#### Backend (`backend/`)
- **`routes/`**: HTTP request handling
- **`controller/`**: Business logic orchestration
- **`service/`**: Core functionality
- **`prompts/`**: AI prompt templates
- **`dto/`**: Data transfer objects 
- **`interfaces/`**: Abstract contracts
- **`dependencies/`**: Dependency injection
- **`tests/`**: Unit and integration tests

### Prompt Engineering Strategy

I divided the prompt into five major sections for comprehensive LinkedIn ad generation:

```python
linkedin_ad_agent_instruction = f"""
{linkedin_ad_agent_role_and_goal}
{linkedin_ad_agent_mandatory_rules}
{linkedin_ad_agent_styles}
{linkedin_ad_agent_design_hints}
{linkedin_ad_agent_chain_of_thought_directions}
"""
```

**Prompt Components:**
1. **Role & Goal**: Defines the AI's purpose and objectives
2. **Mandatory Rules**: Critical guidelines that must be followed
3. **Styles**: Visual style examples and guidance
4. **Design Hints**: Specific design recommendations
5. **Chain of Thought**: Step-by-step reasoning directions

## 🔧 Key Design Decisions

### SOLID Principles Implementation
- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Extensible through interfaces without modification
- **Liskov Substitution**: Implementations are fully substitutable
- **Interface Segregation**: Focused, minimal interfaces
- **Dependency Inversion**: High-level modules depend on abstractions

### Dependency Injection
- Factory functions manage object creation
- FastAPI's `Depends` system handles injection
- Easy to swap implementations (e.g., different AI providers)

### Error Handling
- Comprehensive error handling in services
- Graceful degradation for API failures
- Structured logging throughout the application

## ⚠️ Assumptions & Limitations

### Current Limitations
1. **Logo Hallucination**: The model may generate inaccurate company logos. This can be improved by allowing users to upload actual company logos for better branding accuracy.

2. **Single AI Provider**: Currently only uses OpenAI's image generation models. The architecture supports easy integration of additional providers.

3. **No Image Storage**: Generated images are not persisted server-side but can be downloaded locally.

4. **Prompt Context**: Only derives context from the 6 form fields and prompt engineering, without additional data sources.

### Assumptions
- Users have valid OpenAI API keys
- Generated images meet LinkedIn's advertising guidelines
- Form data provided is accurate and complete


## 🎯 Focus Areas for Review

Please pay special attention to:

1. **Prompt Engineering**: Effectiveness of the multi-section prompt structure and its impact on ad quality
2. **Image Generation Models**: Integration with OpenAI's DALL-E and potential for model switching
3. **Software Engineering Principles**: SOLID principles implementation and architectural decisions
4. **Future Extensibility**: Ideas for expanding the project with new features or AI providers

## 📁 Project Files

- Generated ad examples are available in the `images/` folder
- Test cases are located in `backend/tests/`
- API documentation is available at `http://localhost:8000/docs` when the backend is running

## 🤝 Contributing

This project demonstrates clean architecture principles and is designed for easy extension. Key areas for future development include:
- Additional AI provider integrations
- Enhanced branding capabilities
- Image storage and management
- Advanced prompt customization
- Analytics and performance tracking

P.S: Used prompts to generate Readme.md file based on context given