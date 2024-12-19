import glob
import pandas as pd
import modelskill as ms

obs_fldr = "../observations/" 
df_stn = pd.read_csv(obs_fldr + "stations.csv", index_col=0)

def get_wl_point_obs():
    """Get water level point observations as list of PointObservation objects"""
    q = ms.Quantity(name="Surface Elevation", unit="meter")
    fn = obs_fldr + "Holyrood_Bay_wl.dfs0"
    return ms.PointObservation(fn, x=-53.135, y=47.402, name="Holyrood Bay", quantity=q)

def get_altimetry_obs(quality=None):
    """Get altimetry observations as list of TrackObservation objects"""
    sat_files = sorted(glob.glob(obs_fldr + "Altimetry_wl_*.csv"))
    missions = [f.split("_")[2].split(".")[0] for f in sat_files]
    q = ms.Quantity(name="Surface Elevation", unit="meter")
    altlist = []
    for m in missions:
        df = pd.read_csv(obs_fldr + f"Altimetry_wl_{m}.csv", index_col=0)
        df.index = pd.to_datetime(df.index, format="ISO8601")
        if quality is not None:
            df = df[df.quality_water_level == quality]
        o = ms.TrackObservation(df, item="water_level", x_item="longitude", y_item="latitude", name=m, quantity=q)
        altlist.append(o)
    return altlist