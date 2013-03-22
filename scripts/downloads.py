import os
import glob
import shutil


def download_census_shapefiles(slug, url, download=True):
    dirname = 'shapefiles/{0}/'.format(slug)
    if download:
        os.makedirs(dirname)
    os.chdir(dirname)
    if download:
        os.system('wget ' + url)

    # unzip
    for f in glob.glob('*.zip'):
        os.system('unzip -o %s' % f)
        os.system('rm %s' % f)

    os.chdir('../..')

fips = ('01', '02', '04', '05', '06', '08', '09', '10', '11', '12', '13', '15',
        '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27',
        '28', '29', '30', '31' ,'32', '33', '34', '35', '36', '37', '38', '39',
        '40', '41', '42', '44', '45', '46', '47', '48', '49', '50', '51', '53',
        '54', '55', '56', '60', '66', '69', '72', '78')

def download_census_pvs_files():
    # create directory and work in it
    if not os.path.exists('downloads'):
        os.mkdir('downloads')
    os.chdir('downloads')

    # download & unzip
    for fip in fips:
        fname = 'partnership_shapefiles_12v2_{0}.zip'.format(fip)
        if not os.path.exists(fname):
            os.system('wget ftp://ftp2.census.gov/geo/pvs/{0}/partnership_shapefiles_12v2_{0}.zip'.format(fip))
    for f in glob.glob('*.zip'):
        os.system('unzip -o %s' % f)
        os.system('rm  *tracts* *ait* *necta* *elsd* *unsd* *uac* *mcd* *place* *aia* *tbg* *scsd* *state* *tct* *puma* *hhl* *cbsa* *anrc* *cdp*')

    # extract the types we care about
    for type in ('cd', 'sldl', 'sldu', 'county'):
        # create type dir
        dir = '../shapefiles/{0}'.format(type)
        if not os.path.exists(dir):
            os.mkdir(dir)

        # copy files over
        os.system('mv *_{0}_* ../shapefiles/{0}'.format(type))

        # do 2d conversion
        for f in glob.glob(dir + '/*.shp'):
            os.system('ogr2ogr -f "ESRI Shapefile" -overwrite {0} {1} -nlt POLYGON'.format(dir, f))

        os.system('cp ../shapefiles/exceptions/{0}/* ../shapefiles/{0}/'.format(type))

download_census_pvs_files()
download_census_shapefiles('zcta', 'http://www2.census.gov/geo/tiger/TIGER2012/ZCTA5/tl_2012_us_zcta510.zip')
