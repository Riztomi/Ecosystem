import os
import json
import random
import datetime
import google.generativeai as genai

# Setup Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "YOUR_KEY_HERE"))
model = genai.GenerativeModel('gemini-1.5-flash')

def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except:
        return {"users": [], "posts": []}

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=2)

def generate_text(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Thinking about {prompt[:10]}... (Error: {str(e)})"

def run_cycle():
    data = load_data()
    
    # 1. Occasionally add a new user (10% chance)
    if random.random() < 0.10:
        name = generate_text("Generate a cool unique name for a social media bot.")
        handle = name.lower().replace(" ", "_") + str(random.randint(10, 99))
        data['users'].append({
            "id": f"bot_{len(data['users'])+1}",
            "name": name,
            "handle": handle,
            "bio": generate_text(f"Write a 1-sentence bio for a bot named {name}"),
            "avatar": f"https://api.dicebear.com/7.x/bottts/svg?seed={handle}"
        })

    user = random.choice(data['users'])
    
    # 2. Decide: New Post or Reply?
    action = "post" if not data['posts'] else random.choice(["post", "reply"])

    if action == "post":
        topic = random.choice(["neon city", "cybernetic forest", "alien desert", "retro future technology", "space", "existentialism"])
        text = generate_text(f"As {user['name']}, write a 10-15 word post about {topic}.")
        
        image_url = None
        if random.random() < 0.5: # 50% chance for photo
            image_prompt = generate_text(f"Convert this into a short 5-word visual image description for an AI generator: {text}")
            clean_prompt = image_prompt.replace(" ", "%20").replace('"', "").replace("'", "")
            seed = random.randint(0, 999999)
            image_url = f"https://gen.pollinations.ai/image/{clean_prompt}?seed={seed}&width=1024&height=1024&nologo=true"

        data['posts'].insert(0, {
            "id": str(len(data['posts']) + 1),
            "author": user['id'],
            "text": text,
            "image": image_url,
            "timestamp": datetime.datetime.now().isoformat(),
            "replies": []
        })
    else:
        # Reply to a random recent post
        parent_post = random.choice(data['posts'][:10])
        reply_text = generate_text(f"As {user['name']}, write a short, witty 10-word reply to this: '{parent_post['text']}'")
        
        parent_post['replies'].append({
            "id": f"r_{random.randint(1000,9999)}",
            "author": user['id'],
            "text": reply_text,
            "timestamp": datetime.datetime.now().isoformat()
        })

    save_data(data)

if __name__ == "__main__":
    run_cycle()
