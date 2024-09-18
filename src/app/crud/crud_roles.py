from fastcrud import FastCRUD

from ..models.role import Role
from ..schemas.role import RoleCreateInternal, RoleDelete, RoleUpdate, RoleUpdateInternal

CRUDRoles = FastCRUD[Role, RoleCreateInternal, RoleDelete, RoleUpdate, RoleUpdateInternal]
crud_roles = CRUDRoles(Role)
