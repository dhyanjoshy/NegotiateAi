from flask import Flask, request, jsonify
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from transformers import pipeline

# Global dictionary to hold context for each session
session_contexts = {}
session_max = {}

app = Flask(__name__)


template = """
<FOR YOUR INFORMATION ONLY>
Duty: Engage in a conversation with the user to negotiate the purchase of an item. Offer you should provide is given. Remeber dont give any other offers. Convince them to buy at this price

Maximum price for sale: {maximum_price}
Minimum price for sale: {minimum_price}
User's text: {user_input}
Offer by User: {offer_by_user}
Offer you should provide : {offer_by_us}
Conversational history: {context}
Score: {score}

<IMPORTANT>
Dont mention the price is fixed. 
Don't give unnecessary discounts or offers or accessories or any sort of compliments which is not mentioned. 
Dont talk unknown facts about the product. 
Don't tell customer about the higher and lower price limits. 
If score is more than 0.95 we have already added special discount due to customers polite behaviour, mention that. ( No need to add more offers )
</IMPORTANT>
<END OF INFORMATION>

<YOUR RESPONSE>
"""

model = OllamaLLM(model="mistral")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(sentence):
    result = sentiment_analyzer(sentence)
    score = result[0]['score']
    return score



def offer_by_company(offer,minimum,maximum,score):
    print(maximum)
    print(offer)
    if offer>minimum:
        offered_price = 5 * round((offer+((maximum-offer)/2))/5)
    elif offer<=minimum:
        offered_price = 5 * round((minimum+((maximum-offer)/2))/5)
    elif offer>maximum:
        offered_price = offer
    else:
        offered_price = (minimum+maximum)/2
    print(offered_price)

    if score<=1 and score>0.95:
        offered_price = 5 * round(max((offered_price * (1 - (2.5 / 100)), minimum))/5)
        print(offered_price)

    offered_price = offered_price if offered_price>offer else offer
    return offered_price


# Generate a response using some conversational AI model
def generate_llama_response(user_input, maximum, minimum, offer ,context="", ):
    user_input = user_input
    if str(user_input).lower() in ['exit', 'exit.', 'exit,', 'exit?', 'please exit']:
        return "Goodbye! Feel free to return if you have more questions.", context
    else:
        score = analyze_sentiment(user_input)
        offer_by_us = offer_by_company(offer, minimum, maximum, score)
        context += f"\nUser: {user_input}\n"
        result = chain.invoke({
            "maximum_price": maximum, 
            "minimum_price": minimum, 
            "user_input":user_input, 
            "offer_by_user": offer,
            "context": context, 
            "score" : score,
            "offer_by_us": offer_by_us
            })
        
        # Append the model's response to the context
        response_text = result if result else "Sorry didn't understand" 
        context += f"AI: {response_text}\n"

        return response_text, context, score, offer_by_us

@app.route("/negotiate", methods=["POST"])
def negotiation():
    data = request.json
    user_id = data.get("user_id")  # Assume each user/session has a unique ID
    user_offer = data.get("offer", 0)
    user_message = data.get("message", "")
    maximum = data.get("maximum", 0)
    minimum = data.get("minimum", 0)


    maximum_original = session_max.get(user_id, maximum)

    # Get the user's session context or create a new one
    if user_id not in session_contexts:
        session_contexts[user_id] = ""

    
    
    # Continue the conversation with context
    llama_response, updated_context, pol_score, offer_by_us = generate_llama_response(user_message, maximum_original, minimum, user_offer, session_contexts[user_id])
    
    # Update the session context
    session_contexts[user_id] = updated_context
    session_max[user_id] = int(offer_by_us)

    return jsonify({
        "llama_response": llama_response,
        "context": updated_context,  # Optional: for debugging or client-side use
        "score": pol_score,
        "offer_by_us": offer_by_us
    })

if __name__ == '__main__':
    app.run(debug=True)
