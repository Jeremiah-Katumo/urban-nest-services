from sqlalchemy import Column, Integer, String, Text, Enum as SqlEnum, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone
import uuid

from ..enums.user_enum import TenantStatus, LandlordStatus, UserRoles

Base = declarative_base()


def generate_uuid():
    return str(uuid.uuid4())


class TenantModel(Base):
    __tablename__ = "tenants"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)

    status = Column(SqlEnum(TenantStatus), default=TenantStatus.ACTIVE)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))


class LandlordModel(Base):
    __tablename__ = "landlords"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)

    status = Column(SqlEnum(LandlordStatus), default=LandlordStatus.ACTIVE)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    email = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)

    status = Column(SqlEnum(TenantStatus), default=TenantStatus.ACTIVE)

    role = Column(
        SqlEnum(UserRoles),
        nullable=False,
        default=UserRoles.CUSTOMER
    )

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))

    properties = relationship("PropertyModel", back_populates="user")


class PropertyModel(Base):
    __tablename__ = "properties"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    title = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    location = Column(String(50))

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))

    user = relationship("UserModel", back_populates="properties")


class CampaignModel(Base):
    __tablename__ = "campaigns"

    id = Column(String(36), primary_key=True, default=generate_uuid)

    title = Column(String(255))
    content = Column(Text)

    status = Column(String(20), default="draft")
    target_user_segment = Column(String(255))

    sent_at = Column(DateTime)
    expires_at = Column(DateTime)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
    deleted_at = Column(DateTime(timezone=True))