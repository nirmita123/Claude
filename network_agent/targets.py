"""Target companies by tier, with the name variants people use on LinkedIn.

Matching is exact after normalization (see network_map.normalize), so short or
generic names like "Writer", "Linear", "Modal" or "Ramp" won't pick up
unrelated companies. Add aliases here if a connection's company isn't caught.
"""

TARGETS = [
    # Tier 1
    (1, "Cursor", ["cursor", "anysphere"]),
    (1, "Anthropic", ["anthropic"]),
    (1, "OpenRouter", ["openrouter"]),
    (1, "Decagon", ["decagon"]),
    (1, "Sierra", ["sierra", "sierra ai", "sierra technologies"]),
    (1, "Glean", ["glean", "glean technologies"]),
    (1, "ElevenLabs", ["elevenlabs", "eleven labs"]),
    (1, "Harvey", ["harvey", "harvey ai"]),
    (1, "Hebbia", ["hebbia"]),
    (1, "LangChain", ["langchain"]),
    # Tier 2
    (2, "Databricks", ["databricks"]),
    (2, "Mercor", ["mercor"]),
    (2, "Cognition", ["cognition", "cognition ai", "cognition labs", "windsurf", "codeium"]),
    (2, "Replit", ["replit"]),
    (2, "Vercel", ["vercel"]),
    (2, "Perplexity", ["perplexity", "perplexity ai"]),
    (2, "Notion", ["notion", "notion labs"]),
    (2, "Writer", ["writer", "writer com", "writer ai"]),
    (2, "Hex", ["hex", "hex technologies"]),
    (2, "Lovable", ["lovable"]),
    (2, "Clay", ["clay", "clay labs", "clay com"]),
    (2, "Gamma", ["gamma", "gamma app", "gamma tech"]),
    (2, "Granola", ["granola", "granola ai"]),
    (2, "Runway", ["runway", "runwayml", "runway ml", "runway ai"]),
    (2, "Retool", ["retool"]),
    # Tier 3
    (3, "Baseten", ["baseten"]),
    (3, "Together AI", ["together ai", "together computer", "togetherai"]),
    (3, "Fireworks AI", ["fireworks ai", "fireworks"]),
    (3, "Modal", ["modal", "modal labs"]),
    (3, "Braintrust", ["braintrust", "braintrust data"]),
    (3, "Arize AI", ["arize ai", "arize"]),
    (3, "Pinecone", ["pinecone", "pinecone systems"]),
    (3, "Scale AI", ["scale ai", "scale"]),
    (3, "Cohere", ["cohere"]),
    (3, "Mistral", ["mistral ai", "mistral"]),
    # Tier 4
    (4, "Abridge", ["abridge", "abridge ai"]),
    (4, "Ambience Healthcare", ["ambience healthcare", "ambience"]),
    (4, "EvenUp", ["evenup", "even up"]),
    (4, "Legora", ["legora", "leya"]),
    (4, "Rogo", ["rogo"]),
    (4, "Ramp", ["ramp"]),
    (4, "Synthesia", ["synthesia"]),
    (4, "Descript", ["descript"]),
    (4, "Cartesia", ["cartesia", "cartesia ai"]),
    (4, "Deepgram", ["deepgram"]),
    (4, "Lindy", ["lindy", "lindy ai"]),
    (4, "Factory", ["factory", "factory ai"]),
    (4, "Poolside", ["poolside", "poolside ai"]),
    (4, "Supabase", ["supabase"]),
    (4, "Linear", ["linear", "linear app"]),
]
