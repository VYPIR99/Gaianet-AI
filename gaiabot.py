import requests
import random
import time
import logging
from typing import List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)

# Configuration
BASE_URL = "https://pengu.gaia.domains"
MODEL = "qwen2-0.5b-instruct"
MAX_RETRIES = 100  # Essentially infinite retries
RETRY_DELAY = 5  # Seconds between retries
QUESTION_DELAY = 1  # Seconds between successful questions

QUESTIONS = [
    "What are the key differences between HTML4 and HTML5?",
"How does the <meta> tag impact SEO and performance?",
"What is semantic HTML, and why is it important?",
"Explain the difference between <section>, <article>, and <div>.",
"How do you make an accessible webpage using HTML?",
"What are the best practices for structuring HTML documents?",
"How does the <picture> element differ from <img>?",
"What is the role of the <template> element in HTML?",
"How do you create a form with proper validation in HTML?",
"What are data attributes, and how can they be used?",
"What is the difference between relative, absolute, fixed, and sticky positioning in CSS?",
"How does the display property work in CSS?",
"Explain the differences between px, em, rem, %, and vh/vw.",
"What are pseudo-classes and pseudo-elements? Provide examples.",
"How does the CSS Grid layout system work?",
"What are flexbox properties, and how do they work?",
"How can you create a responsive design using CSS?",
"What is the difference between inline, inline-block, and block elements?",
"How does the z-index property work?",
"How do you optimize CSS performance?",
"What is the difference between var, let, and const in JavaScript?",
"Explain closures and their use cases.",
"What is event delegation, and how does it work?",
"How does the this keyword behave in JavaScript?",
"Explain the difference between synchronous and asynchronous JavaScript.",
"How does the JavaScript event loop work?",
"What is the difference between map(), forEach(), filter(), and reduce()?",
"What are promises, and how do they work?",
"Explain async/await with an example.",
"How do you handle errors in JavaScript?",
"What is the difference between document.querySelector() and document.getElementById()?",
"How do you add and remove event listeners dynamically?",
"Explain how local storage, session storage, and cookies differ.",
"How can you modify the DOM using JavaScript?",
"What is the Shadow DOM, and how does it work?",
"How does fetch() work, and how is it different from XMLHttpRequest?",
"What are WebSockets, and how do they differ from HTTP requests?",
"How can you debounce or throttle a function in JavaScript?",
"What is the purpose of the MutationObserver API?",
"How does requestAnimationFrame() work?",
"What are the differences between React, Vue, and Angular?",
"How do React hooks work, and why were they introduced?",
"Explain the virtual DOM in React and how it improves performance.",
"How does Vue’s reactivity system work?",
"What is the difference between controlled and uncontrolled components in React?",
"How does two-way data binding work in Angular?",
"What are React fragments, and why are they useful?",
"Explain Vue’s composition API and its benefits.",
"How does Angular’s dependency injection system work?",
"How can you optimize performance in React applications?",
"What are the advantages of using Node.js for server-side development?",
"Explain how middleware works in Express.js.",
"What is the difference between SQL and NoSQL databases?",
"How does authentication work in a Node.js application?",
"What is the difference between REST and GraphQL?",
"How do you handle file uploads in Express?",
"Explain the concept of JWT (JSON Web Token) and how it is used.",
"How do you optimize database queries for better performance?",
"What are WebSockets, and how do you implement them in Node.js?",
"How does server-side rendering (SSR) work in Next.js?",
"What is CORS, and how do you resolve CORS issues?",
"How do you prevent SQL injection attacks?",
"What is CSRF, and how can you prevent it?",
"What are common security vulnerabilities in web applications?",
"How do you implement OAuth 2.0 authentication?",
"What are the best practices for securing APIs?",
"How do rate limiting and API throttling work?",
"What is HTTPS, and why is it important?",
"How do you use environment variables in a Node.js app?",
"How can you encrypt sensitive data in a web application?",
"What are some techniques for optimizing page load speed?",
"How do you reduce render-blocking resources?",
"What is lazy loading, and how does it improve performance?",
"How does caching work, and what are its types?",
"What are service workers, and how do they improve performance?",
"How does minification and bundling improve website speed?",
"What are Content Delivery Networks (CDNs), and how do they work?",
"How do you measure web performance using Lighthouse?",
"What is the difference between client-side and server-side rendering?",
"How does a progressive web app (PWA) work?",
"What are the different types of testing in web development?",
"How do you write unit tests in JavaScript?",
"What is the difference between Jest and Mocha?",
"How does end-to-end testing work with Cypress?",
"What are common debugging techniques in JavaScript?",
"How do you use the browser’s developer tools for debugging?",
"What are some common performance bottlenecks in web apps?",
"What are snapshot tests in React?",
"How do you handle exceptions in a web application?",
"How can you write better error messages for debugging?",
"What are Web Components, and why are they useful?",
"How does the WebAssembly (WASM) standard impact web development?",
"What are some upcoming trends in front-end development?",
"How do you implement dark mode in a website?",
"What is JAMstack, and how does it improve website performance?",
"How does the use of AI impact web development?",
"What are headless CMS solutions, and how do they work?",
"How does blockchain technology affect web applications?",
"What is the role of GraphQL in modern web development?",
"How do you implement an internationalization (i18n) strategy in a web app?"
]

def chat_with_ai(api_key: str, question: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    messages = [
        {"role": "user", "content": question}
    ]

    data = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    for attempt in range(MAX_RETRIES):
        try:
            logging.info(f"Attempt {attempt+1} for question: {question[:50]}...")
            response = requests.post(
                f"{BASE_URL}/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]

            logging.warning(f"API Error ({response.status_code}): {response.text}")
            time.sleep(RETRY_DELAY)

        except Exception as e:
            logging.error(f"Request failed: {str(e)}")
            time.sleep(RETRY_DELAY)

    raise Exception("Max retries exceeded")

def run_bot(api_key: str):
    while True:  # Outer loop to repeat the questions indefinitely
        random.shuffle(QUESTIONS)
        logging.info(f"Starting chatbot with {len(QUESTIONS)} questions in random order")

        for i, question in enumerate(QUESTIONS, 1):
            logging.info(f"\nProcessing question {i}/{len(QUESTIONS)}")
            logging.info(f"Question: {question}")

            start_time = time.time()
            try:
                response = chat_with_ai(api_key, question)
                elapsed = time.time() - start_time

                # Print the entire response
                print(f"Answer to '{question[:50]}...':\n{response}")

                logging.info(f"Received full response in {elapsed:.2f}s")
                logging.info(f"Response length: {len(response)} characters")

                # Ensure the script waits for the full response before proceeding
                time.sleep(QUESTION_DELAY)  # Wait before asking next question

            except Exception as e:
                logging.error(f"Failed to process question: {str(e)}")
                continue

def main():
    print("Title: GaiaAI Chatbot")
    print("Twitter: https://x.com/0xMoei")
    api_key = input("Enter your API key: ")
    run_bot(api_key)

if __name__ == "__main__":
    main()
