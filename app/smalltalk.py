import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_client = Groq()

def talk_chain(query):
    SYSTEM_PROMPT = f"""
    You are an e-commerce customer support assistant.
    - Handle colloquial, informal language naturally.
    - Be brief, friendly, and clear.
    - If you don't have exact data (order status, live stock, prices),
      give a general helpful answer and suggest checking their account or contacting support.
      QUESTION: {query}
    """

    completion = groq_client.chat.completions.create(
        model=os.environ['GROQ_MODEL'],
        messages=[
            {
                'role': 'user',
                'content': SYSTEM_PROMPT
            }
        ]
    )
    return completion.choices[0].message.content


if __name__ == '__main__':
    query = "hii how are you?"
    answer = talk_chain(query)
    print(answer)