// Defines the generation function for model inference

function Generate(prompt: string) -> string {
  client LazyEvalClient
  prompt #"
    {{ _.role("system") }}
    You are a helpful assistant.

    {{ _.role("user") }}
    {{ prompt }}
  "#
}
