from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from schemas.filename import Filenames

class FilenamesRoute():
    def __init__(self, db_session: Session):
        self.db_session= db_session

    async def create(self, name:str, types:str):
        new_filename = Filenames(name=name, types=types)
        self.db_session.add(new_filename)
        await self.db_session.flush()

    async def get_all(self) -> List[Filenames]:
        res = await self.db_session.execute(select(Filenames).order_by(Filenames.file_idx))
        return res.scalars().all()
    
    async def get_by_name(self, f_name)-> List[Filenames]:
        res = await self.db_session.execute(select(Filenames).where(Filenames.name==f_name))
        # res = await self.db_session.execute(select(Filenames).where(Filenames.name.in_([f_name])))
        return res.scalars().all()
    
    async def update(self, id:int, name: Optional[str], types: Optional[str]):
        res = update(Filenames).where(Filenames.file_idx == id)
        if name:
            res = res.values(name=name)
        if types:
            res = res.values(types=types)
        res.execution_options(synchronize_session="fetch")
        await  self.db_session.execute(res)