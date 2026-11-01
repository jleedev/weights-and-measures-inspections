import base64
from datetime import date, timedelta
import io
import json
from pathlib import Path

import jinja2
import polars as pl
import polars.selectors as cs
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate

from .process_data import Devices, Stores, Inspections

# Inspections dashboard!

# Some prerequisites:

# device_id's which are not deleted and the store is not oob (and also exists in the Stores table)
ActiveDeviceIds = Devices.join(Stores, 'store_id').filter(oob=False, deleted=False).select('device_id')

# The latest inspection date for each device_id
LatestInspections = Inspections.sort('date').group_by('device_id', maintain_order=True).last()

# Said latest date with the inspection cycle added to it
UpcomingReinspections = LatestInspections.join(
    ActiveDeviceIds, 'device_id',
).join(
    Devices.select('device_id', 'offset'), 'device_id',
).select(
    'device_id',
    'store_id',
    pl.col('date').dt.offset_by(pl.col('offset')),
)

Today = date.today()
NumDays = timedelta(days=7)

# Some upcoming values to look at:
ReinspectionView = UpcomingReinspections.filter(
    pl.col('date').is_between(Today, Today+NumDays)
).group_by(
    'store_id',
).agg(
    pl.count('device_id').alias('device_count'),
).join(Stores.select('store_id', 'store_name', 'address'), 'store_id')

# Additional parts of the dashboard

NeverInspectedDeviceIds = Devices.join(Inspections, 'device_id', how='anti').select('device_id')

OverdueReinspections = UpcomingReinspections.filter(
    pl.col('date') < date.today() - timedelta(days=365),
)

TotalStores = ReinspectionView.select('store_id').count().collect().item()

TotalDevices = ReinspectionView.select('device_count').sum().collect().item()

# Date histogram of:
# 1) Inspections that happened
# 2) Computed upcoming inspections in the past (i.e. didn't happen as of today)
# 3) Computed upcoming inspections in the future
sns.histplot(
    pl.concat([
        Inspections.select(
            pl.col('date'),
            pl.lit('past').alias('kind'),
        ),
        UpcomingReinspections.select(
            pl.col('date'),
            pl.when(
                pl.col('date') < date.today(),
            ).then(pl.lit('missed').alias('kind')).otherwise(pl.lit('future')),
        ),
    ]).collect().to_dict(),
    x='date',
    hue='kind',
    multiple='stack',
    bins=64,  # 3-mo buckets given the current extent of data
    element='step',
)

# Apparently you can't open palm slam a Base64-encoded SVG into a
# GitHub Markdown file…

images_dir = Path("images")
images_dir.mkdir(exist_ok=True)

class ImageAsset:
    def __init__(self, path):
        self.path = path
    def __html__(self):
        return self.path
    @classmethod
    def savefig(cls, fname, **kwargs):
        path = images_dir / fname
        plt.savefig(path, **kwargs)
        return cls(path)

InspectionTimeline = ImageAsset.savefig("timeline.svg", format="svg")

# Gather the results
Dataset = json.load(Path("./raw/allegheny-county-weights-and-measures-inspections.json").open())

template = jinja2.Environment(
    loader=jinja2.PackageLoader(__package__),
    autoescape=True,
)

# (I wonder if there's a way to use IPython's display module to produce
# reports without committing the entire output to ipynb format, which is
# a little bit limiting.)
# Anyway, it looks like pandas uses tabulate to spit out markdown so sure.

def to_markdown(df: pl.DataFrame):
    return tabulate(
        df.to_dict(),
        headers="keys",
        tablefmt="github",
    )

ReinspectionView = to_markdown(ReinspectionView.collect())

if __name__ == '__main__':
    out = template.get_template('README.md').render(locals())
    Path("README.md").write_text(out)
