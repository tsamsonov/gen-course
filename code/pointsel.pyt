import arcpy, numpy
class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Point Selection"
        self.alias = ""
        # List of tool classes associated with this toolbox
        self.tools = [SettlementSpacing, VoronoySelection]
class SettlementSpacing(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Settlement Spacing"
        self.description = "Settlement spacing point selection algorithm"
        self.canRunInBackground = True
    def getParameterInfo(self):
        """Define parameter definitions"""
        in_features = arcpy.Parameter(
            displayName="Input Features",
            name="in_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        # Second parameter
        in_field = arcpy.Parameter(
            displayName="Importance Field",
            name="in_field",
            datatype="Field",
            parameterType="Optional",
            direction="Input")
        in_field.parameterDependencies = [in_features.name]

        scale = arcpy.Parameter(
            displayName="Scale Factor",
            name="scale",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        scale.value= 1

        remain_field = arcpy.Parameter(
            displayName="Remain field",
            name="remain_field",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        remain_field.value = 'Remain'
        params = [in_features, in_field, scale, remain_field]
        return params
    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True
    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return
    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_features = parameters[0].valueAsText
        in_field = parameters[1].valueAsText
        scale = int(parameters[2].valueAsText)
        remain_field = parameters[3].valueAsText

        arcpy.AddField_management(in_features, remain_field, "SHORT")

        in_lyr = 'in_lyr'
        arcpy.MakeFeatureLayer_management(in_features, in_lyr)

        fields = [in_field, remain_field, 'SHAPE@']
        buf = 'in_memory/buf'

        num_pts = int(arcpy.GetCount_management(in_features).getOutput(0))
        arcpy.SetProgressor("step", "Selecting points...",
                            0, num_pts, 1)
        i = 1
        with arcpy.da.UpdateCursor(in_features, fields,
                                   sql_clause=(None, "ORDER BY {0} DESC".format(in_field))) as cursor:
            for row in cursor:
                arcpy.SetProgressorLabel("Processing {0} from {1}".format(i, num_pts))
                radius = scale / row[0]
                arcpy.Buffer_analysis(row[2], buf, radius)
                arcpy.SelectLayerByAttribute_management(in_lyr, 'NEW_SELECTION', ' "{0}" = 1 '.format(remain_field))
                arcpy.SelectLayerByLocation_management(in_lyr, 'INTERSECT', buf, selection_type='SUBSET_SELECTION')
                num_selected = int(arcpy.GetCount_management(in_lyr).getOutput(0))
                row[1] = 0 if num_selected > 0 else 1
                cursor.updateRow(row)
                arcpy.SetProgressorPosition()
                i += 1
        arcpy.ResetProgressor()
        return

def get_values(features, field):
    return numpy.asarray([row[0] for row in arcpy.da.SearchCursor(features, field)])

def set_values(features, field, values):
    with arcpy.da.UpdateCursor(features, field) as rows:
        i = 0
        for row in rows:
            row[0] = values[i]
            rows.updateRow(row)
            i += 1
    return features

class VoronoySelection(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Voronoy Selection"
        self.description = "Voronoy-based point selection algorithm"
        self.canRunInBackground = True
    def getParameterInfo(self):
        """Define parameter definitions"""
        in_features = arcpy.Parameter(
            displayName="Input Features",
            name="in_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        # Second parameter
        in_field = arcpy.Parameter(
            displayName="Importance Field",
            name="in_field",
            datatype="Field",
            parameterType="Optional",
            direction="Input")
        in_field.parameterDependencies = [in_features.name]

        perc = arcpy.Parameter(
            displayName="Selection percentage",
            name="perc",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        perc.value = 50.0

        remain_field = arcpy.Parameter(
            displayName="Remain field",
            name="remain_field",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        remain_field.value = 'Remain'
        params = [in_features, in_field, perc, remain_field]
        return params
    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True
    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return
    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return
    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_features = parameters[0].valueAsText
        in_field = parameters[1].valueAsText
        perc = float(parameters[2].valueAsText)
        remain_field = parameters[3].valueAsText
        susp_field = 'susp'

        arcpy.AddField_management(in_features, remain_field, "SHORT")
        arcpy.CalculateField_management(in_features, remain_field, 1)

        arcpy.AddField_management(in_features, susp_field, "SHORT")
        arcpy.CalculateField_management(in_features, susp_field, 0)

        wt_field = 'weight'
        arcpy.AddField_management(in_features, wt_field, "DOUBLE")

        vor = 'in_memory/voronoy'
        arcpy.CreateThiessenPolygons_analysis(in_features, vor, 'ALL')
        arcpy.AddGeometryAttributes_management(vor, 'AREA_GEODESIC')

        with arcpy.da.UpdateCursor(vor, [wt_field, in_field, 'AREA_GEO']) as cursor:
            for row in cursor:
                row[0] = row[1] * row[2]
                cursor.updateRow(row)

        set_values(in_features, wt_field, get_values(vor, wt_field))

        in_lyr = 'in_lyr'
        arcpy.MakeFeatureLayer_management(in_features, in_lyr)

        vor_lyr = 'vor_lyr'
        arcpy.MakeFeatureLayer_management(vor, vor_lyr)

        total_pts = int(arcpy.GetCount_management(in_features).getOutput(0))

        num_pts = int(total_pts * (1 - 0.01 * perc))
        arcpy.SetProgressor("step", "Omitting points...",
                            0, num_pts, 1)
        i = 1
        fields = [remain_field, susp_field, wt_field, 'SHAPE@']


        vor_new = 'in_memory/vor_new'
        vor_new_lyr = 'vor_new_lyr'

        with arcpy.da.UpdateCursor(in_features, fields,
                                   sql_clause=(None, "ORDER BY {0} DESC".format(wt_field))) as cursor:
            for row in cursor:
                if row[0] == 0 or row[1] == 1:
                    continue

                arcpy.SelectLayerByLocation_management(vor_lyr, 'INTERSECT', row[3])
                arcpy.SelectLayerByLocation_management(vor_lyr, 'INTERSECT', vor_lyr)
                arcpy.SelectLayerByLocation_management(in_lyr, 'INTERSECT', vor_lyr)
                arcpy.CalculateField_management(in_lyr, susp_field, 1)
                row[0] = 0

                # rearrange thiessen polygons
                arcpy.SelectLayerByLocation_management(vor_lyr, 'INTERSECT', vor_lyr)
                arcpy.SelectLayerByLocation_management(in_lyr, 'INTERSECT', vor_lyr)

                arcpy.CreateThiessenPolygons_analysis(in_lyr, vor_new, 'ALL')
                arcpy.AddGeometryAttributes_management(vor_new, 'AREA_GEODESIC')

                arcpy.AddField_management(vor_new, 'weight', 'DOUBLE')
                with arcpy.da.UpdateCursor(vor_new, [wt_field, in_field, 'AREA_GEO']) as cursor2:
                    for row2 in cursor2:
                        row2[0] = row2[1] * row2[2]
                        cursor2.updateRow(row2)

                arcpy.MakeFeatureLayer_management(vor_new, vor_new_lyr)

                arcpy.SelectLayerByLocation_management(vor_lyr, 'INTERSECT', row[3])
                arcpy.SelectLayerByLocation_management(vor_new_lyr, 'INTERSECT', vor_lyr)

                arcpy.DeleteFeatures_management(vor_lyr)
                arcpy.Append_management(vor_new_lyr, vor, "NO_TEST")

                cursor.updateRow(row)
                arcpy.SetProgressorPosition()
                i += 1
        arcpy.ResetProgressor()
        return