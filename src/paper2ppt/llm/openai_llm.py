from openai import Client, AsyncClient

from src.paper2ppt.configs.settings import get_settings


from functools import lru_cache

# client = unify.Unify("gpt-4o@openai", api_key=get_settings().OPENAI_API_KEY)


# async_client = AsyncClient(api_key=get_settings().OPENAI_API_KEY)
sync_client = Client(api_key=get_settings().OPENAI_API_KEY)


class ClientWrapper:
    def __init__(self, client: Client):
        self.client = client

    def __getattr__(self, item):
        return getattr(self.client, item)

    def generate(self, prompt: str, **kwargs):
        res = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                }
            ],
            **kwargs,
        )
        content = res.choices[0].message.content
        return content


@lru_cache()
def get_openai_sync_client() -> ClientWrapper:
    return ClientWrapper(sync_client)
