import sys
import os

# Добавление корневой директории проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ProjectDirectory.AdForgePackageVer4.ad_manager import AdManager
from ProjectDirectory.AdForgePackageVer4.ad_editor import AdEditor
from ProjectDirectory.AdForgePackageVer4.config import proxies
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

app = FastAPI()

class AdRequest(BaseModel):
    headline: str
    audience: str
    key_benefits: str = None
    call_to_action: str = None
    style: str = None
    length_limit: int = None
    model_choice: int = 1
    temperature: float = 0.7
    stream: bool = False

ad_manager = AdManager(proxies=proxies)

@app.post("/generate_ad")
async def generate_ad(request: AdRequest):
    try:
        ad_manager.set_basic_params(request.headline, request.audience)
        ad_manager.set_advanced_params(
            key_benefits=request.key_benefits,
            call_to_action=request.call_to_action,
            style=request.style,
            length_limit=request.length_limit,
            model_choice=request.model_choice,
            temperature=request.temperature,
            stream=request.stream
        )

        ad_text = await ad_manager.generate_ad()
        return {"ad_text": ad_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import asyncio

class EditRequest(BaseModel):
    old_ad_text: str
    edit_instructions: str
    model_choice: int = 1
    temperature: float = 0.7
    stream: bool = False


@app.post("/edit_ad")
async def edit_ad(request: EditRequest):
    try:
        # Создаем экземпляр AdEditor и передаем ему текущий текст объявления и экземпляр AdManager
        editor = AdEditor(ad_text=request.old_ad_text, ad_manager=ad_manager)

        # Задаем параметры для редактора
        await editor.change_model(request.model_choice)
        await editor.toggle_stream(request.stream)
        await editor.change_temperature(request.temperature)
        await editor.add_arbitrary_change(request.edit_instructions)

        # Применяем изменения и сохраняем обновленное объявление
        ad_text = await editor.apply_changes()
        return {"ad_text": ad_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)