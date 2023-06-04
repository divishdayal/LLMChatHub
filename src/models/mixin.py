from datetime import datetime

from sqlalchemy import TIMESTAMP, Column


def get_created_at(context):
    return context.get_current_parameters()["created_at"]


class TimestampMixin(object):
    created_at = Column(
        TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=get_created_at,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    deleted_at = Column(
        TIMESTAMP(timezone=True),
        default=None,
        onupdate=datetime.utcnow,
        nullable=True,
    )

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
