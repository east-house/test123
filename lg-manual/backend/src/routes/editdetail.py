from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from schemas.editdetail import EditDetail

class EditDetailRoute():
    def __init__(self, db_session: Session):
        self.db_session= db_session

    async def create(self, total_idx:int, m_file_idx:int, save_datetime:str, 
                     correct_data:str, inspector:str):
        new_filename = EditDetail(
            total_idx=total_idx, m_file_idx=m_file_idx, save_datetime=save_datetime, 
            correct_data=correct_data, inspector=inspector)
        self.db_session.add(new_filename)
        await self.db_session.flush()

    async def get_all(self) -> List[EditDetail]:
        res = await self.db_session.execute(select(EditDetail).order_by(EditDetail.edit_idx))
        return res.scalars().all()
    
    async def get_file_idx(self, file_idx)-> List[EditDetail]:
        res = await self.db_session.execute(select(EditDetail).where(EditDetail.m_file_idx==file_idx))
        return res.scalars().all() 

    async def get_total_manual(self, total_idx, manual_idx)->List[EditDetail]:
        res = await self.db_session.execute(select(EditDetail).where(EditDetail.total_idx==total_idx).where(EditDetail.m_file_idx==manual_idx))
        return res.scalars().all()

    async def get_manual_idx(self, manual_idx)->List[EditDetail]:
        res = await self.db_session.execute(select(EditDetail).where(EditDetail.m_file_idx==manual_idx))
        return res.scalars().all()
    
    async def update(self, total_idx:int, m_file_idx: Optional[int], save_datetime:Optional[str],
                     correct_data:Optional[str],inspector:Optional[str]):
        res = update(EditDetail).where(EditDetail.total_idx==total_idx).where(EditDetail.m_file_idx==m_file_idx)
        if save_datetime:
            res = res.values(save_datetime=save_datetime)
        if correct_data:
            res = res.values(correct_data=correct_data)
        if inspector:
            res = res.values(inspector=inspector)
        res.execution_options(synchronize_session="fetch")
        await  self.db_session.execute(res)