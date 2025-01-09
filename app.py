from flask import jsonify,request
from Files import app,llm_client,image_client, pattern
import re
import base64
from io import BytesIO
from flask_cors import CORS

CORS(app)

def find_prompt(text):
    matches = re.findall(pattern, text, re.DOTALL)
    final_response = re.sub(pattern,"",text,re.DOTALL)

    return [final_response,matches]

def make_LLM_call(content):
    response = llm_client.chat.completions.create(
                model="nvidia/llama-3.1-nemotron-70b-instruct",
                messages=content,
                temperature=0.5,
                top_p=0.7,
                max_tokens=1024,
                stream=True
            )
    response_text = ""
            
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            text = chunk.choices[0].delta.content
            response_text += text
    
    return find_prompt(response_text)

def generate_image(prompt):
    print(prompt)
    try:
        image = image_client.text_to_image(prompt)
        image_io = BytesIO()
        image.save(image_io, 'PNG')
        image_io.seek(0)

        return base64.b64encode(image_io.getvalue()).decode('utf-8')
    except:
        return None

@app.route("/send_prompt", methods=['POST'])
def send_prompt():
    content = request.json.get("content")
    (message,prompt) = make_LLM_call(content)
    
    if len(prompt)>0:
      prompt = generate_image(prompt[0])
    else:
      prompt=None
    
    return jsonify({"message":message, "image":prompt})


if __name__ == "__main__":
    app.run(debug=True)
