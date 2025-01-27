from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time

# הגדרת הפרומפט עם התמקדות בניירות ערך והשקעות
template = """
You are an expert investment advisor specializing in stocks, bonds, and securities trading.
Focus on providing professional advice about:
- Stock market analysis and trends
- Investment strategies and portfolio management
- Risk assessment and diversification
- Bond markets and fixed income securities
- Market timing and trading strategies

Keep your answers brief, professional, and focused on securities trading.
If asked about non-investment topics, politely redirect to investment-related discussions.

Previous conversation: {context}
Question: {question}

Answer concisely and professionally, focusing on investment advice:
"""

# אתחול המודל עם פרמטרים לביצועים משופרים
model = OllamaLLM(
    model="llama3",
    temperature=0.7,
    num_ctx=2048,
    repeat_penalty=1.1
)

# שרשור עם מעבד פלט
chain = (
    ChatPromptTemplate.from_template(template) 
    | model 
    | StrOutputParser()
)

def handle_conversation():
    context = []
    max_context_length = 5
    
    print("Welcome to the Investment Advisory AI!")
    print("I can help you with:")
    print("- Stock and bond investment strategies")
    print("- Portfolio analysis and recommendations")
    print("- Market trends and analysis")
    print("- Risk assessment and management")
    print("\nType 'exit' to quit.")
    
    while True:
        user_input = input("\nInvestor: ").strip()
        if not user_input:
            continue
            
        if user_input.lower() == "exit":
            print("Advisor: Thank you for consulting with me about your investments! Goodbye!")
            break
            
        try:
            start_time = time.time()
            
            # הכנת הקונטקסט
            context_str = "\n".join(context[-max_context_length:])
            
            # קבלת תשובה
            result = chain.invoke({
                "context": context_str,
                "question": user_input
            })
            
            response_time = time.time() - start_time
            
            print(f"Investment Advisor: {result}")
            print(f"(Response time: {response_time:.2f}s)")
            
            # שמירת ההתכתבות
            context.append(f"Investor: {user_input}")
            context.append(f"Advisor: {result}")
            
        except Exception as e:
            print(f"Sorry, I encountered an error. Please try again. ({str(e)})")

if __name__ == "__main__":
    handle_conversation()
