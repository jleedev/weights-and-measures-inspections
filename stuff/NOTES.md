# Notes from data dictionary

## Devices

| Column | Type | Description |
|:---|:---|:---|
| device_id | text | ID number of the device. If null, then a price verification was conducted and no weighing or measuring devices were tested. |
| store_id | text | ID number of the store |
| device_type | text | Type of device (gasoline, jewelry scale, etc) |
| device_group | text | Group of device (fuel, timing, scale, or miscellaneous |
| make | text | Brand of scale, pump etc. |
| model | text | Model of scale, pump etc. |
| serial_number | text | Serial number |
| pump | text | Pump number |
| grade | text | Fuel grade |
| capacity | text | Capacity of pump or scale |
| inspection_cycle | text |  |
| remarks | text | Notes |
| deleted | text | Old devices deleted from inspection schedule (1=yes, 0=no) |

## Inspections

| Column | Type | Label | Description |
|:---|:---|:---|:---|
| inspection_id | text |  | ID number of the inspection |
| store_id | text |  | ID number of the store |
| device_id | text |  | ID number of the device. If null, then a price verification was conducted and no weighing or measuring devices were tested. |
| date | date | Date | Date for AQI reading |
| result | text |  | Result of inspection (pass/fail) |
| reinspection | text |  | Whether the device needs to be reinspected (yes/no) |

## Stores

| Column | Type | Label | Description |
|:---|:---|:---|:---|
| store_id | text |  | ID number of the store |
| store_name | text |  | Name of the store |
| address | text | Street address | Building number and street. When a structure is demolished the county removes the building number. The structure technically has no address at that point. These properties have a building number of zero. |
| mailing_city | text |  | City |
| state | text |  | State of the facility |
| zip | text |  | Zip code of the city |
| municipality | text |  |  |
| corp_id | text |  | Internal use code |
| neighborhood | text | neighborhood |  |
| longitude | float8 |  |  |
| latitude | float8 |  |  |
| business_phone | text |  | Phone number |
| alternate_phone | text |  | Other phone number |
| price_verification | text |  | Needs price verification (1=yes, 0=no) |
| fuel_dispenser | text |  | Has fuel dispensers (1=yes, 0=no) |
| scale | text |  | Has weigh scales (1=yes, 0=no) |
| timing | text |  | Has timing device (1=yes, 0=no) |
| misc_inspection | text |  | Not used |
| oob | text |  | Out of business (1=yes, 0=no) |
| unit | text | Unit | Unit the reported value is measured in |
| shopping_center | text |  | Shopping center name |
| new_municipality | text |  | Municipality |
