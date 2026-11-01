import polars as pl
import polars.selectors as cs

from .load_data import get_resources

data: dict[str, pl.LazyFrame] = {}
for name, path in get_resources().items():
    data[name] = pl.scan_csv(path, schema_overrides={
        'pump': pl.String(),
        'serial_number': pl.String(),
        'zip': pl.String(),
    })

Devices = data['Devices']
Stores = data['Stores']
Inspections = data['Inspections']

__all__ = ["Devices", "Stores", "Inspections"]

# Data cleaning notes

# >>> Devices.group_by(pl.col('device_group').str.to_uppercase()).len().show(100)
# FUEL DISPENSER 13378
# TIMING         16296
# SCALE          9607 
# MISCELLANEOUS  21   


# Converting device_type to uppercase reduces the number of distinct values from 46 to 27.

Devices = Devices.with_columns(
    pl.col('device_group', 'device_type').str.to_uppercase(),
    pl.col('deleted').cast(pl.Boolean()),
).with_columns(
    pl.col('device_group').cast(pl.Categorical()),
    # Annoying whitespace
    pl.col('make').str.strip_chars(),
)

# Convenient value for polars function
Devices = Devices.with_columns(
    pl.col('inspection_cycle').str.replace(' MONTH', 'mo').alias('offset'),
)

# Stores

# new_municipality: 'unknown'
# Reduce from 175 to 108

Stores = Stores.with_columns(
    pl.col('new_municipality').str.to_uppercase().str.replace_all
('[^A-Z]', ''),
        pl.col('neighborhood').str.to_uppercase().str.replace(r' \(.*', ''),
).drop('corp_id', 'misc_inspection')

# More kinds of null
Stores = Stores.with_columns(
    alternate_phone=pl.when(
        pl.col('alternate_phone').str.contains('_')
    ).then(None).otherwise('alternate_phone'),
    business_phone=pl.when(
        pl.col('business_phone').str.contains(r'\d').not_()
    ).then(None).otherwise('business_phone'),
)

# The columns neighborhood,mailing_city,municipality,new_municipality contain mostly nonsense.

# | unit | text | Unit | Unit the reported value is measured in |
#
# Appears to actually be the suite number of the address.

# | misc_inspection | text |  | Not used |


# Inspections
# No nonsense detected.

Inspections = Inspections.with_columns(
    pl.col('result', 'reinspection').cast(pl.Categorical()),
    pl.col('date').str.to_date(),
)

# | device_id | text |  | ID number of the device. If null, then a price verification was conducted and no weighing or measuring devices were tested. |
# However, no nulls detected.
