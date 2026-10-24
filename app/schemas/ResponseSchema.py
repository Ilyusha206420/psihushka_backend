from pydantic import BaseModel

class ResponseSchema(BaseModel):
    npc_texts: list[str] | None
    player_texts: list[str] | None
    plot_data: list[int] | None
