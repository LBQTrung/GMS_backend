from fastcrud import FastCRUD

from ..models.master_data_type import MasterDataType
from ..schemas.master_data_type import MasterDataTypeCreateInternal, MasterDataTypeDelete, MasterDataTypeUpdate, MasterDataTypeUpdateInternal

CRUDMasterDataTypes = FastCRUD[MasterDataType, MasterDataTypeCreateInternal, MasterDataTypeDelete, MasterDataTypeUpdate, MasterDataTypeUpdateInternal]
crud_master_data_types = CRUDMasterDataTypes(MasterDataType)
