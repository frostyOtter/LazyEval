// Defines the client configuration for LazyEval
// Uses environment variables for configuration to match existing project setup

client<llm> LazyEvalClient {
  provider fallback
  options {
    strategy [
      Gemini3Flash
    ]
  }
}


client<llm> JudgeClient {
  provider fallback
  options {
    strategy [
      Gemini3Flash
    ]
  }
}

client<llm> Gemini3Flash{
  provider "google-ai"
  options {
    api_key env.GEMINI_API_KEY
    model "gemini-3-flash-preview"
  }
}

client<llm> CustomeClient{
  provider openai
  options {
    base_url env.MODEL_BASE_URL
    api_key env.MODEL_API_KEY
    model env.MODEL_NAME
  }
}