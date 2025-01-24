from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model = "llama3") # המודל הרלונטי שנשתמש, בהמשך מודל של ניירות ערך ומניות
prompt = ChatPromptTemplate.from_template(template) # יצירת תבנית לפונקציה
chain = prompt | model # חיבור התבנית למודל


def handle_conversation():
    context = ""
    print("welcome to the AI chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("AI bot: Thank you for chatting! Goodbye!")  # הודעה לפני יציאה
            break
        result = chain.invoke({"context": context, "question": user_input})
        print(f"AI bot: {result}")
        context += f"\nYou: {user_input}\nAI bot: {result}"
        
if __name__ == "__main__":
    handle_conversation()
