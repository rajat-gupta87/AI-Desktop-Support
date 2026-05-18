import os

from groq import Groq

from dotenv import load_dotenv

load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_ai(user_message, screenshot=None):

    prompt = user_message

    prompt += """

Give response in:
- clean format
- bullet points
- short paragraphs
- proper troubleshooting steps
"""

    if screenshot:

        prompt += f"""

        User uploaded screenshot:
        {screenshot}

        Analyze possible desktop support issue
        and provide troubleshooting steps.
        """

    chat_completion = client.chat.completions.create(

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        model="llama-3.3-70b-versatile"
    )

    return chat_completion.choices[0].message.content