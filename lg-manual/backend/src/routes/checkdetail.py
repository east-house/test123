from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from schemas.checkdetail import CheckDetail

class CheckDetailsRoute():
    def __init__(self, db_session: Session):
        self.db_session= db_session

    async def create(self, file_idx:int, no:str, product_type:str, regulation:str, category:str, region:str, 
                    country:str, detail:str, checking_data:str, image:str, file:str):
        new_filename = CheckDetail(file_idx=file_idx, no=no, product_type=product_type, regulation=regulation,
                                category=category, region=region, country=country, detail=detail,
                                checking_data=checking_data, image=image, file=file)
        self.db_session.add(new_filename)
        await self.db_session.flush()

    async def get_all(self) -> List[CheckDetail]:
        res = await self.db_session.execute(select(CheckDetail).order_by(CheckDetail.total_idx))
        return res.scalars().all()
    
    async def get_file_idx(self, file_idx)-> List[CheckDetail]:
        res = await self.db_session.execute(select(CheckDetail).where(CheckDetail.file_idx==file_idx))
        return res.scalars().all()
    
    async def get_by_list(self, by_list:List)-> List[CheckDetail]:
        res = await self.db_session.execute(select(CheckDetail).where(CheckDetail.no.in_(by_list)))
        return res.scalars().all()  

    # async def update(self, total_idx:int, file_idx: Optional[int],
    #                  no: Optional[str], detail_E: Optional[str],
    #                  detail_K: Optional[str], stand_sent: Optional[str]):
    #     res = update(CheckDetail).where(CheckDetail.total_idx == total_idx)
    #     if file_idx:
    #         res = res.values(file_idx=file_idx)
    #     if no:
    #         res = res.values(no=no)
    #     if detail_E:
    #         res = res.values(detail_E=detail_E)
    #     if detail_K:
    #         res = res.values(detail_K=detail_K)
    #     if stand_sent:
    #         res = res.values(stand_sent=stand_sent)
    #     res.execution_options(synchronize_session="fetch")
    #     await  self.db_session.execute(res)