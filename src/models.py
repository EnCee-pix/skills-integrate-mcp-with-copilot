"""
Database models for the High School Management System
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

# Association table for many-to-many relationship between activities and participants
activity_participants = Table(
    'activity_participants',
    Base.metadata,
    Column('activity_id', Integer, ForeignKey('activities.id'), primary_key=True),
    Column('participant_email', String, primary_key=True),
    Column('signed_up_at', DateTime, default=datetime.utcnow)
)


class Activity(Base):
    """Activity model representing extracurricular activities"""
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    max_participants = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert activity to dictionary format matching the original structure"""
        return {
            "description": self.description,
            "schedule": self.schedule,
            "max_participants": self.max_participants,
            "participants": self.get_participants()
        }

    def get_participants(self):
        """Get list of participant emails"""
        from .database import SessionLocal
        db = SessionLocal()
        try:
            result = db.execute(
                activity_participants.select().where(
                    activity_participants.c.activity_id == self.id
                )
            )
            return [row.participant_email for row in result]
        finally:
            db.close()

    def add_participant(self, email: str, db):
        """Add a participant to the activity"""
        db.execute(
            activity_participants.insert().values(
                activity_id=self.id,
                participant_email=email
            )
        )
        db.commit()

    def remove_participant(self, email: str, db):
        """Remove a participant from the activity"""
        db.execute(
            activity_participants.delete().where(
                (activity_participants.c.activity_id == self.id) &
                (activity_participants.c.participant_email == email)
            )
        )
        db.commit()

    def has_participant(self, email: str, db) -> bool:
        """Check if a participant is signed up for the activity"""
        result = db.execute(
            activity_participants.select().where(
                (activity_participants.c.activity_id == self.id) &
                (activity_participants.c.participant_email == email)
            )
        ).first()
        return result is not None
