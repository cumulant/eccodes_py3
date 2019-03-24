# Test to read ICON-EU GRIB2 data witch Eccodes and python3
# By Hermann Asensio
# based on examples from ECMWF https://confluence.ecmwf.int/display/ECC/grib_get_keys
# changed by Hermann Asensio
# aim is to learn Python3 Interface of EcCodes to read GRIB data
# example Input GRIB is from Numerical Weather Prediction Model ICON-EU from Deutscher Wetterdienst
# Data from http://opendata.dwd.de/weather/nwp/icon-eu/grib/00/t_2m/icon-eu_europe_regular-lat-lon_single-level_2019032300_000_T_2M.grib2.bz2 (unpacked and renamed to icon-eu_T_2M_example.grib2)

import traceback
import sys
from eccodes import *
 
INPUT='icon-eu_T_2M_example.grib2'
VERBOSE = 1  # verbose error reporting
 
 
def readgribkeys():
    f = open(INPUT, 'rb')
 
    keys = [
        'Ni',
        'Nj',
        'latitudeOfFirstGridPointInDegrees',
        'longitudeOfFirstGridPointInDegrees',
        'latitudeOfLastGridPointInDegrees',
        'longitudeOfLastGridPointInDegrees',
    ]
 
    while 1:
        gid = codes_grib_new_from_file(f)
        if gid is None:
            break
 
        for key in keys:
            try:
                print('  %s: %s' % (key, codes_get(gid, key)))
            except KeyValueNotFoundError as err:
                # Full list of exceptions here:
                #   https://confluence.ecmwf.int/display/ECC/Python+exception+classes
                print('  Key="%s" was not found: %s' % (key, err.msg))
            except CodesInternalError as err:
                print('Error with key="%s" : %s' % (key, err.msg))
 
        print('There are %d values, average is %f, min is %f, max is %f' % (
            codes_get_size(gid, 'values'),
            codes_get(gid, 'average'),
            codes_get(gid, 'min'),
            codes_get(gid, 'max')
        ))
 
        codes_release(gid)
 
    f.close()
 
 
def main():
    try:
        readgribkeys()
    except CodesInternalError as err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            sys.stderr.write(err.msg + '\n')
 
        return 1
 
 
if __name__ == "__main__":
    sys.exit(main())
