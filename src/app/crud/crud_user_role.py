from fastcrud import FastCRUD

from ..models.user import UserRole
from ..schemas.user_role import UserRoleCreateInternal, UserRoleDelete, UserRoleUpdate, UserRoleUpdateInternal

CRUDUserRole = FastCRUD[UserRole, UserRoleCreateInternal, UserRoleDelete, UserRoleUpdate, UserRoleUpdateInternal]
crud_user_role = CRUDUserRole(UserRole)
