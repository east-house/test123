from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from schemas.predictdetail import PredictDetail

class PredictDetailsRoute():
    def __init__(self, db_session: Session):
        self.db_session= db_session

    async def create(self, total_idx:int, m_file_idx:int, model_idx:int, evidence:str,
                     result:str, sim:str, remark:str, correct:str):
        new_filename = PredictDetail(
            total_idx=total_idx, m_file_idx=m_file_idx, model_idx=model_idx, evidence=evidence,
            result=result, sim=sim, remark=remark, correct=correct)
        self.db_session.add(new_filename)
        await self.db_session.flush()

    async def get_all(self) -> List[PredictDetail]:
        res = await self.db_session.execute(select(PredictDetail).order_by(PredictDetail.predict_idx))
        return res.scalars().all()
    
    async def get_file_idx(self, file_idx:int)-> List[PredictDetail]:
        res = await self.db_session.execute(select(PredictDetail).where(PredictDetail.m_file_idx==int(file_idx)))
        return res.scalars().all() 

    async def get_total_manual_idx(self, total_list:List, manual_idx)->List[PredictDetail]:
        res = await self.db_session.execute(select(PredictDetail).where(PredictDetail.total_idx.in_(total_list)).where(PredictDetail.m_file_idx==manual_idx))
        return res.scalars().all()
    
    async def get_manual_idx(self, manual_idx)->List[PredictDetail]:
        res = await self.db_session.execute(select(PredictDetail).where(PredictDetail.m_file_idx==manual_idx))
        return res.scalars().all()

    async def get_total_manual(self, total_idx, manual_idx)->List[PredictDetail]:
        res = await self.db_session.execute(select(PredictDetail).where(PredictDetail.total_idx==total_idx).where(PredictDetail.m_file_idx==manual_idx))
        return res.scalars().all()

    async def update(self, total_idx:int, m_file_idx: Optional[int], model_idx:Optional[int],
                     evidence:Optional[str], result:Optional[str], sim:Optional[str],
                     remark: Optional[str], correct: Optional[str]):
        res = update(PredictDetail).where(PredictDetail.total_idx==total_idx).where(PredictDetail.m_file_idx==m_file_idx)
        if model_idx:
            res = res.values(model_idx=model_idx)
        if evidence:
            res = res.values(evidence=evidence)
        if result:
            res = res.values(result=result)
        if sim:
            res = res.values(sim=sim)
        if remark:
            res = res.values(remark=remark)
        if correct:
            res = res.values(correct=correct)
        res.execution_options(synchronize_session="fetch")
        await  self.db_session.execute(res)