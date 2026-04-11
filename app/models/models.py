import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Table, Column, Integer, String, Text, Enum as SqlEnum, 
    ForeignKey, DateTime, JSON, Boolean, UniqueConstraint, Float
)
from ..domain.enums import (
    user_enum, campaign_enum, house_enum, booking_enum, 
    entity_enum, base_enum, transporter_enum, support_ticket_enum
)
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


class UserPermissionModel(Base):
    __tablename__ = "user_permissions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"))
    permission_id = Column(String(36), ForeignKey("permissions.id", ondelete="CASCADE"))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    permission = relationship("PermissionModel")


class PermissionModel(Base):
    __tablename__ = "permissions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    feature = relationship("FeatureModel", back_populates="permissions")
    roles = relationship("RoleModel", secondary=role_permissions, back_populates="permissions", lazy="selectin")
    feature_id = Column(String(36), ForeignKey("features.id", ondelete="CASCADE"))
    entity_id = Column(String(36), ForeignKey("entities.id", ondelete="CASCADE"), nullable=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=True)
    
    entity = relationship("EntityModel")
    
    def __repr__(self): 
        return f"<Permission id={self.id} name={self.name}>"


class RoleModel(Base):
    __tablename__ = "roles"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    permissions = relationship("PermissionModel", secondary=role_permissions, back_populates="roles", lazy="selectin")
    users = relationship("UserModel", secondary=user_roles, back_populates="roles", lazy="selectin")
    entity_id = Column(String(36), ForeignKey("entities.id", ondelete="CASCADE"), nullable=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=True)
    
    entity = relationship("EntityModel")
    
    def __repr__(self):
        return f"<Role id={self.id} name={self.name}>"


class TenantModel(Base):
    __tablename__ = "tenants"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)

    status = Column(SqlEnum(base_enum.Status), default=base_enum.Status.ACTIVE)
    role = Column(
        SqlEnum(user_enum.UserRoles),
        nullable=False,
        default=user_enum.UserRoles.CUSTOMER
    )
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))
    
    entity_id = Column(String(36), ForeignKey("entities.id", ondelete="CASCADE"), nullable=True)
    
    entity = relationship("EntityModel")
    users = relationship("UserModel", back_populates="tenant")


class LandlordModel(Base):
    __tablename__ = "landlords"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)

    status = Column(SqlEnum(base_enum.Status), default=base_enum.Status.ACTIVE)
    role = Column(
        SqlEnum(user_enum.UserRoles),
        nullable=False,
        default=user_enum.UserRoles.CUSTOMER
    )

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))
    
    entity_id = Column(String(36), ForeignKey("entities.id", ondelete="CASCADE"), nullable=True)
    
    properties = relationship("PropertyModel", back_populates="landlord")
    entity = relationship("EntityModel")
    user = relationship("UserModel", back_populates="landlord")
    
    
class AgentModel(Base):
    __tablename__ = "agents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    username = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(50), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)

    status = Column(SqlEnum(base_enum.Status), default=base_enum.Status.ACTIVE)
    role = Column(
        SqlEnum(user_enum.UserRoles),
        nullable=False,
        default=user_enum.UserRoles.CUSTOMER
    )

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))
    
    entity_id = Column(String(36), ForeignKey("entities.id", ondelete="CASCADE"), nullable=True)
    
    entity = relationship("EntityModel")
    user = relationship("UserModel", back_populates="agent")
    
    
class TransporterModel(Base):
    __tablename__ = "transporters"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    username = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    email = Column(String(50), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    avatar = Column(String(30), nullable=True)
    password = Column(String(255), nullable=False)
    
    base_price = Column(Float, nullable=False, default=50)
    price_per_km = Column(Float, nullable=False, default=2)
    rating = Column(Float, nullable=False, default=4.7)
    driver_status = Column(SqlEnum(transporter_enum.DriverStatus), nullable=False, default=transporter_enum.DriverStatus.AVAILABLE)

    status = Column(SqlEnum(base_enum.Status), default=base_enum.Status.ACTIVE)

    role = Column(
        SqlEnum(user_enum.UserRoles),
        nullable=False,
        default=user_enum.UserRoles.CUSTOMER
    )

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))
    
    entity_id = Column(String(36), ForeignKey("entities.id", ondelete="CASCADE"), nullable=True)
    
    entity = relationship("EntityModel")
    user = relationship("UserModel", back_populates="agent")
    

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

    status = Column(SqlEnum(base_enum.Status), default=base_enum.Status.ACTIVE)

    role = Column(
        SqlEnum(user_enum.UserRoles),
        nullable=False,
        default=user_enum.UserRoles.CUSTOMER
    )

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))
    
    entity_id = Column(String(36), ForeignKey("entities.id", ondelete="CASCADE"), nullable=True)
    tenant_id = Column(String(36), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=True)
    landlord_id = Column(String(36), ForeignKey("landlords.id", ondelete="CASCADE"), nullable=True)
    agent_id = Column(String(36), ForeignKey("agents.id", ondelete="CASCADE"), nullable=True)
    
    tenant = relationship("TenantModel", back_populates="users")
    landlord = relationship("LandlordModel", back_populates="user", uselist=False)
    agent = relationship("AgentModel", back_populates="user", uselist=False)
    transporter = relationship("TransporterModel", back_populates="user")
    roles = relationship('RoleModel', secondary=user_roles, back_populates="users", lazy="selectin")  # many-to-many
    entity = relationship("EntityModel")
    

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
    entity_id = Column(String(36), ForeignKey("entities.id", ondelete="CASCADE"))

    landlord = relationship("LandlordModel", back_populates="properties")
    entity = relationship("EntityModel")


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
    entity_id = Column(String(36), ForeignKey("entities.id", ondelete="CASCADE"))
    
    entity = relationship("EntityModel")
    
    
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
    feature_id = Column(String(36), ForeignKey("features.id", ondelete="CASCADE"))
    entity_id = Column(String(36), ForeignKey("entities.id", ondelete="CASCADE"), nullable=True)
    
    property = relationship("PropertyModel")
    tenant = relationship("TenantModel")
    entity = relationship("EntityModel", back_populates="bookings")
    
    
class FeatureModel(Base):
    __tablename__ = "features"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    status = Column(SqlEnum(base_enum.Status), default=base_enum.Status.ACTIVE)

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
    status = Column(SqlEnum(base_enum.Status), default=base_enum.Status.ACTIVE)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    bookings = relationship("BookingModel", back_populates="entity")    
    
    
class FieldModel(Base):
    __tablename__ = "fields"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    module = Column(String(64), nullable=False, index=True)
    feature_id = Column(String(36), ForeignKey("features.id"), nullable=True)
    name = Column(String(128), nullable=False)
    key = Column(String(100), nullable=False)  # slug, unique per module
    type = Column(String(32), nullable=False)  # 'text','number','boolean','date','select'
    options = Column(JSON, nullable=True)
    required = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    values = relationship("ValueModel", back_populates="field")


class ValueModel(Base):
    __tablename__ = "values"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    module = Column(String(64), nullable=False, index=True)
    entity_id = Column(String(64), nullable=False)  # e.g., user id or product id
    field_id = Column(String(36), ForeignKey("fields.id"))
    value = Column(JSON, nullable=True)  # store typed value(s) as JSON
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("field_id", "entity_id"),
    )

    field = relationship("FieldModel", back_populates="values")
    
    
class SubscriptionModel(Base):
    __tablename__ = "subscriptions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    interval = Column(SqlEnum(transporter_enum.IntervalEnum), nullable=False)
    role = Column(SqlEnum(user_enum.UserRoles), nullable=False)
    description = Column(Text)
    features = Column(Text)  # JSON string
    is_deleted = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)


class SupportTicketModel(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    role = Column(SqlEnum(user_enum.UserRoles), nullable=False)

    title = Column(String(255))
    description = Column(Text)

    category = Column(SqlEnum(support_ticket_enum.TicketCategory), default=support_ticket_enum.TicketCategory.OTHER)
    status = Column(SqlEnum(support_ticket_enum.TicketStatus), default=support_ticket_enum.TicketStatus.OPEN)

    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)