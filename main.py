import asyncio

from fastapi import FastAPI

from core.api import complaint_router
from core.repositories.complaint import ComplaintRepository

app = FastAPI()
app.include_router(complaint_router)

if __name__ == '__main__':
    orm = ComplaintRepository()
    asyncio.run(orm.init_db())

    import uvicorn
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )
