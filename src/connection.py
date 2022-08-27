import enum
import pandas as pd
from sqlalchemy import Column, DateTime, Enum, Float, create_engine
from sqlalchemy.orm.session import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
INSTALL_DATE = "2022-08-02T08:00:00"

Base = declarative_base()


class ConsumptionType(enum.Enum):
    elec = "electricity"
    gas = "gas"


class ConsumptionReading(Base):
    __tablename__ = "consumption_reading"
    interval_start = Column(DateTime, primary_key=True)
    consumption_type = Column(Enum(ConsumptionType), primary_key=True)
    interval_end = Column(DateTime)
    consumption = Column(Float(precision=3))


class Connection:
    def __init__(self):
        self.engine = create_engine("sqlite:///db/database.db")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def write(self, data, consumption_type):
        df = (
            pd.DataFrame(data)
            .sort_values("interval_start")
            .assign(consumption_type=consumption_type)
        )
        df["interval_start"] = pd.to_datetime(df["interval_start"], format=DATE_FORMAT)
        df["interval_end"] = pd.to_datetime(df["interval_end"], format=DATE_FORMAT)
        df.to_sql("consumption_reading", self.engine, if_exists="append", index=False)

    def read(self, consumption_type):
        return pd.read_sql(
            f"""
            SELECT *
            FROM consumption_reading
            WHERE consumption_type='{consumption_type}'
            """,
            self.engine,
            parse_dates={"interval_start": DATE_FORMAT, "interval_end": DATE_FORMAT},
            index_col="interval_start",
        )

    def get_last_recorded_date(self, consumption_type):
        last_reading = (
            self.session.query(ConsumptionReading)
            .filter(ConsumptionReading.consumption_type == consumption_type)
            .order_by(ConsumptionReading.interval_start.desc())
            .limit(1)
            .one_or_none()
        )

        if last_reading is None:
            return INSTALL_DATE

        return last_reading.interval_end
