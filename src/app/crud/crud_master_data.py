from fastcrud import FastCRUD

from ..models.master_data import MasterData
from ..schemas.master_data import MasterDataCreateInternal, MasterDataDelete, MasterDataUpdate, MasterDataUpdateInternal

CRUDMasterData = FastCRUD[MasterData, MasterDataCreateInternal, MasterDataDelete, MasterDataUpdate, MasterDataUpdateInternal]
crud_master_data = CRUDMasterData(MasterData)
