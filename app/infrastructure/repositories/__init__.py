from .value_repository import ValueRepository
from ..db.database import db

value_repo = ValueRepository(db)