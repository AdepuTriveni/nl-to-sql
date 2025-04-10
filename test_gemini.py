import google.generativeai as genai

# Replace with your actual API key
genai.configure(api_key="AIzaSyDrqUwQbRK22mTdN4k9hwPBRvDINqy3108")

try:
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    response = model.generate_content("Explain SQL in simple terms")
    print(response.text)
except Exception as e:
    print("❌ Error occurred:")
    print(e)
