import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String, Text, Enum as SqlEnum, ForeignKey, DateTime, JSON
from ..domain.enums import landlord_enum, agent_enum, user_enum, campaign_enum, tenant_enum, house_enum, booking_enum, entity_enum
from ..infrastructure.db.database import db

Base = db.Base

def generate_uuid():
    return str(uuid.uuid4())

class SoftDeleteMixin:
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", String(36), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", String(36), ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", String(36), ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)


class TenantModel(Base):
    __tablename__ = "tenants"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)

    status = Column(SqlEnum(tenant_enum.TenantStatus), default=tenant_enum.TenantStatus.ACTIVE)
    role = Column(
        SqlEnum(user_enum.UserRoles),
        nullable=False,
        default=user_enum.UserRoles.CUSTOMER
    )
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))


class LandlordModel(Base):
    __tablename__ = "landlords"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)

    status = Column(SqlEnum(landlord_enum.LandlordStatus), default=landlord_enum.LandlordStatus.ACTIVE)
    role = Column(
        SqlEnum(user_enum.UserRoles),
        nullable=False,
        default=user_enum.UserRoles.CUSTOMER
    )
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))
    
    properties = relationship("PropertyModel", back_populates="landlord")
    
    
class AgentModel(Base):
    __tablename__ = "agents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)

    status = Column(SqlEnum(agent_enum.AgentStatus), default=agent_enum.AgentStatus.ACTIVE)
    role = Column(
        SqlEnum(user_enum.UserRoles),
        nullable=False,
        default=user_enum.UserRoles.CUSTOMER
    )
    
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    username = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    email = Column(String(50), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    avatar = Column(String(30), nullable=True)
    password = Column(String(255), nullable=False)

    status = Column(SqlEnum(user_enum.UserStatus), default=user_enum.UserStatus.ACTIVE)

    role = Column(
        SqlEnum(user_enum.UserRoles),
        nullable=False,
        default=user_enum.UserRoles.CUSTOMER
    )

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))
    
    tenant = relationship("TenantModel", backref="user", uselist=False)
    landlord = relationship("LandlordModel", backref="user", uselist=False)
    agent = relationship("AgentModel", backref="user", uselist=False)
    roles = relationship('RoleModel', secondary=user_roles, back_populates="users", lazy="selectin")  # many-to-many


class PropertyModel(Base):
    __tablename__ = "properties"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(50), index=True)
    price = Column(Integer, index=True)
    
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    images = Column(JSON, nullable=True)
    is_available = Column(SqlEnum(house_enum.HouseStatus), default=house_enum.HouseStatus.AVAILABLE)
    amenities = Column(JSON, nullable=True)

    landlord_id = Column(String(36), ForeignKey("landlords.id", ondelete="CASCADE"))
    agent_id = Column(String(36), ForeignKey("agents.id", ondelete="CASCADE"), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))

    landlord = relationship("LandlordModel", back_populates="properties")


class CampaignModel(Base):
    __tablename__ = "campaigns"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    title = Column(String(255))
    content = Column(Text)

    status = Column(SqlEnum(campaign_enum.CampaignStatus), default=campaign_enum.CampaignStatus.DRAFT)
    target_user_segment = Column(String(255))

    sent_at = Column(DateTime)
    expires_at = Column(DateTime)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))
    
    
class BookingModel(Base):
    __tablename__ = "bookings"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    tenant_id = Column(String(36), ForeignKey("tenants.id"))
    property_id = Column(String(36), ForeignKey("properties.id"))

    start_date = Column(DateTime)
    end_date = Column(DateTime)
    total_price = Column(Integer, index=True)
    
    status = Column(SqlEnum(booking_enum.BookingStatus), default=booking_enum.BookingStatus.PENDING)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))
    
    property = relationship("PropertyModel")
    tenant = relationship("TenantModel")
    
    
class FeatureModel(Base):
    __tablename__ = "features"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    entity_id = Column(String(36), ForeignKey("entities.id", ondelete="CASCADE"), nullable=True)
    
    entity = relationship("EntityModel")
    permissions = relationship("PermissionModel", back_populates="feature")
    
    
class EntityModel(Base):
    __tablename__ = "entities"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    email = Column(String(30), nullable=False)
    currency = Column(
        SqlEnum(
            entity_enum.CurrencyEnum,
            name="currency_enum",
            native_enum=True,   # REQUIRED for MySQL
            validate_strings=True
        ),
        nullable=True
    )
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    
class PermissionModel(Base):
    __tablename__ = "permissions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    feature_id = Column(String(36), ForeignKey("features.id", ondelete="CASCADE"))

    feature = relationship("FeatureModel", back_populates="permissions")
    roles = relationship("RoleModel", secondary=role_permissions, back_populates="permissions", lazy="selectin")
    
    def __repr__(self): 
        return f"<Permission id={self.id} name={self.name}>"


class RoleModel(Base):
    __tablename__ = "roles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    permissions = relationship("PermissionModel", secondary=role_permissions, back_populates="roles", lazy="selectin")
    users = relationship("UserModel", secondary=user_roles, back_populates="roles", lazy="selectin")
    
    def __repr__(self):
        return f"<Role id={self.id} name={self.name}>"
    