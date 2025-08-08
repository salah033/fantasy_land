from products.models import Products
from sentence_transformers import SentenceTransformer, util
import torch
from groq import Groq
from django.conf import settings

groq_client = Groq(api_key=settings.GROQ_API_KEY)

ABBREVIATIONS = {
    "ps5": "playstation 5",
    "ps4": "playstation 4",
    "rdr2": "red dead redemption 2",
    "gow": "god of war",
    "cod": "call of duty",
}

def preprocess_message(message: str) -> str:
    message_lower = message.lower()
    for abbr, full in ABBREVIATIONS.items():
        if abbr in message_lower:
            message_lower = message_lower.replace(abbr, full)
    return message_lower

# Load model once when server starts
model = SentenceTransformer('all-MiniLM-L6-v2')

# Cache product data and embeddings globally (for performance)
product_queryset = Products.objects.all()
product_texts = [f"{p.name} {p.designation or ''} {p.abbreviation or ''} {p.category or ''}".strip()
                for p in product_queryset]
product_embeddings = model.encode(product_texts, convert_to_tensor=True)

def get_response(message):
    # Preprocess abbreviations (you define this)
    clean_message = preprocess_message(message)

    # Encode user message embedding
    user_embedding = model.encode(clean_message, convert_to_tensor=True)

    # Semantic search over product_texts
    cosine_scores = util.cos_sim(user_embedding, product_embeddings)[0]
    best_score_idx = int(torch.argmax(cosine_scores))
    best_score = float(cosine_scores[best_score_idx])

    if best_score >= 0.4:
        best_match = product_queryset[best_score_idx]
        availability = "available" if best_match.quantity > 0 else "out of stock"
        product_info = f"{best_match.name} is {availability} at {best_match.price} DT."

        # Prompt Groq to generate a natural response including product info
        prompt_messages = [
            {"role": "system", "content": "You are a friendly store assistant."},
            {
                "role": "user",
                "content": f"User asked: '{clean_message}'. Product info: {product_info}. Reply naturally."
            }
        ]
    else:
        # No relevant product found - ask Groq politely with fallback prompt
        prompt_messages = [
            {
                "role": "system",
                "content": (
    "You are a friendly assistant representing a store that sells PS4, PS5, and Nintendo games, consoles, and accessories. "
    "If the user asks about products you don't have, respond politely and never say the store doesn't sell games. "
    "Always try to help by suggesting popular gaming products or asking what else you can assist with. "
    "If a product is not available, ask the user if they want to make an order by calling 46570966, or leaving a message on our Facebook or Instagram page. "
    "Never say that we don't sell gaming stuff. "
    "If a product is out of stock, apologize and say the user can place an order and you will provide it as soon as possible."
    "Always try to get short responses instead of giving big text that may make the user flee"
                ),
            },
            {"role": "user", "content": clean_message},
        ]

    # Call Groq LLM
    chat_completion = groq_client.chat.completions.create(
        messages=prompt_messages,
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content
