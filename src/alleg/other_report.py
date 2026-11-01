import polars as pl
import polars.selectors as cs

from .process_data import *

# Interesting things to explore that weren't part of the main report

# Add a date of the inspection which follows
next_date = cs.date().shift(-1).over('device_id', order_by=cs.date())

# Inspections including how long we went until the next inspection, or today
# Only meaningful if deactivated devices are excluded
Inspection_Interval = Inspections.join(Devices, "device_id").drop(
    '_id', cs.ends_with('_right'),
).with_columns(
    # The date of the inspection which followed, or null
    next_date=next_date,
).with_columns(
    # The date of the inspection which followed, or today
    # next_date_upcoming=pl.when(pl.col("next_date").is_null() & pl.col("deleted").not_()).then(date.today()).otherwise(pl.col("next_date")),
).with_columns(
    # How long from this inspecction to the one which followed
    interval=pl.col('next_date') - pl.col('date'),
    # interval_upcoming=pl.col('next_date_upcoming') - pl.col('date'),
)

# From here we can e.g. make a histogram of how much time actually elapsed between inspections, perhaps faceted by type or make of device, or by inspection result.
