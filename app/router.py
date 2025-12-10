from semantic_router import Route
from semantic_router.routers import SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2")

faq = Route(
    name='faq',
    score_threshold=0.35,
    utterances=[
        "What is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
        "Are there any ongoing sales or promotions?",
        "Can I cancel or modify my order after placing it?",
        "Do you offer international shipping?",
        "What should I do if I receive a damaged product?",
        "How do I use a promo code during checkout?"
    ]
)

sql = Route(
    name='sql',
    score_threshold=0.35,
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?"
    ]
)

small_talk = Route(
    name='small_talk',
    score_threshold=0.35,
    utterances=[
    "How are you?",
    "What is your name?",
    "Are you a robot?",
    "What are you?",
    "What do you do?"
    ]
)

router = SemanticRouter(routes=[faq, sql,small_talk],encoder=encoder,auto_sync='local')

if __name__ == "__main__":
    print(router("What is your policy on defective product?").name)
    print(router("Pink puma shoes in price range 4000 to 6000?").name)
    print(router("whats your name?").name)