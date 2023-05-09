from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from schemas.manualdetail import ManualDetail

class ManualDetailsRoute():
    def __init__(self, db_session: Session):
        self.db_session= db_session

    async def create(self, file_idx:str, sent:str, page_num:str):
        new_filename = ManualDetail(file_idx=file_idx, sent=sent, page_num=page_num)
        self.db_session.add(new_filename)
        await self.db_session.flush()

    async def get_all(self) -> List[ManualDetail]:
        res = await self.db_session.execute(select(ManualDetail).order_by(ManualDetail.manual_idx))
        return res.scalars().all()
    
    async def get_file_idx(self, file_idx)-> List[ManualDetail]:
        res = await self.db_session.execute(select(ManualDetail).where(ManualDetail.file_idx==file_idx))
        return res.scalars().all() 

    async def update(self, manual_idx:int, file_idx: Optional[int],
                     sent: Optional[str], page_num: Optional[str]):
        res = update(ManualDetail).where(ManualDetail.manual_idx == manual_idx)
        if file_idx:
            res = res.values(file_idx=file_idx)
        if sent:
            res = res.values(sent=sent)
        if page_num:
            res = res.values(page_num=page_num)
        res.execution_options(synchronize_session="fetch")
        await  self.db_session.execute(res)