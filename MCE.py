import arcpy
from arcpy.sa import Raster

# Set the database for the dataset invocation and storage
arcpy.env.workspace = "F:\Leeds\Semester 1\Data Visualisation & Analysis\Assignment\Assessment 2\Woodland-1\MCE.gdb"

# Enable to overwrite dataset files
arcpy.env.overwriteOutput = True

# Check Spatial Analysis Expansion Permission
arcpy.CheckOutExtension("Spatial")


# Define raster standardization function
def raster_standardization(raster):
    # Get the maximum and minimum value of the input raster
    max_value = float(arcpy.GetRasterProperties_management(raster, "MAXIMUM").getOutput(0))
    min_value = float(arcpy.GetRasterProperties_management(raster, "MINIMUM").getOutput(0))

    # Standardization Calculation
    values = (Raster(raster) - min_value) / (max_value - min_value)

    # Save the output standardized raster
    values.save(f"{raster}_standard")


# Define MCE weighting function
def mce_calculation(raster_dictionary):
    # Create an empty raster for the calculation
    mce = None

    # Loop for weights calculation
    for raster, weight in raster_dictionary.items():
        # Activate raster added in the loop
        raster_1 = Raster(f'{raster}_standard')
        # Calculation
        mce_value = raster_1 * weight
        if mce is None:
            mce = mce_value
        else:
            mce += mce_value

    # Save the MCE result
    mce.save("MCE")

# List of the rasters to be standardized
raster_list = ["DEM", "Roads_distance", "Urban_area_distance", "South_facing"]
# Dictionary with the target rasters with weights
raster_weight = {"DEM": 0.15, "Roads_distance": 0.25, "Urban_area_distance": 0.25, "South_facing": 0.35}

# Loop for standardization operation
for raster_data in raster_list:
    raster_standardization(raster_data)

# MCE operation with weights
mce_calculation(raster_weight)

# Release Spatial analysis expansion permission
arcpy.CheckInExtension("Spatial")
