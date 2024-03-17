from openai import AsyncOpenAI
import logging
import config

client = AsyncOpenAI(api_key=config.OPENAI_TOKEN)


async def generate_text(prompt) -> dict:
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(e)


async def generate_image(prompt, n=1, size="1024x1024") -> list[str]:
    try:
        response = await client.images.generate(prompt=prompt, n=n, size=size)
        urls = []
        for i in response.data:
            urls.append(i.url)
        return urls
    except Exception as e:
        logging.error(e)
        return []
