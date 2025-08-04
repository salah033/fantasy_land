'''from products.models import Products
from sentence_transformers import SentenceTransformer, util
import torch

# Load model once when server starts
model = SentenceTransformer('all-MiniLM-L6-v2')

# Cache product data and embeddings globally (for performance)
product_queryset = Products.objects.all()
product_names = [product.name for product in product_queryset]
product_embeddings = model.encode(product_names, convert_to_tensor=True)

def get_response(message):
    # Encode the incoming message
    user_embedding = model.encode(message, convert_to_tensor=True)

    # Calculate cosine similarity
    cosine_scores = util.cos_sim(user_embedding, product_embeddings)[0]

    # Get best match
    best_score_idx = int(torch.argmax(cosine_scores))
    best_score = float(cosine_scores[best_score_idx])
    best_match = product_queryset[best_score_idx]

    # Optional: set a minimum threshold to avoid unrelated matches
    if best_score < 0.4:
        return "Sorry, I couldn't find that product."

    availability = "available" if best_match.quantity > 0 else "out of stock"
    return f"{best_match.name} is {availability} at {best_match.price} DT."'''
