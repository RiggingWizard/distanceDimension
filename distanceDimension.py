import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import sys
import math

node_name = 'distanceDimension'
node_id = OpenMaya.MTypeId(0x1046ff)

class distanceDimension(OpenMayaMPx.MPxNode):
    
    # DEFINING OUR ATTRIBUTES #
    
    in_radius = OpenMaya.MObject()
    in_translate = OpenMaya.MObject()
    out_rotate = OpenMaya.MObject()
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        
    def compute(self, plug, data_block):

        if plug == distanceDimension.distance:
            
            # CREATING DATA HANDLES TO DATA BLOCK #        
            
            point_A_val = data_block.inputValue(distanceDimension.pointA).asFloat3()
            point_B_val = data_block.inputValue(distanceDimension.pointB).asFloat3()
            
            # PERFORMING COMPUTATION #
            
            distance_calculate = (((point_B_val[0] - point_A_val[0])**2 + (point_B_val[1] - point_A_val[1])**2 + (point_B_val[2] - point_A_val[2])**2)**0.5)
            
            # SETTING THE OUTPUT VALUE #
            distance_handle = data_block.outputValue(distanceDimension.distance)            
            distance_handle.setFloat(distance_calculate)       
            
            # SET THE DATA BLOCK AS CLEAN #
            
            data_block.setClean(plug)
            
        else:
            return OpenMaya.kUnknownParameter
       
def nodeCreator():
    return OpenMayaMPx.asMPxPtr(distanceDimension())
    
def nodeInitializer():
    
    # 1. CREATING FUNCTION SET FOR NUMERIC ATTRIBUTES #
    
    mfn_numeric_attr = OpenMaya.MFnNumericAttribute()
    
    # 2. CREATING THE ATTRIBUTES #
    
    distanceDimension.pointA = mfn_numeric_attr.create('positionA', 'posA', OpenMaya.MFnNumericData.k3Float)
    mfn_numeric_attr.setReadable(True)
    mfn_numeric_attr.setWritable(True)
    mfn_numeric_attr.setStorable(True)
    mfn_numeric_attr.setKeyable(True)
    
    distanceDimension.pointB = mfn_numeric_attr.create('positionB', 'posB', OpenMaya.MFnNumericData.k3Float)
    mfn_numeric_attr.setReadable(True)
    mfn_numeric_attr.setWritable(True)
    mfn_numeric_attr.setStorable(True)
    mfn_numeric_attr.setKeyable(True)
    
    distanceDimension.distance = mfn_numeric_attr.create('distance', 'distance', OpenMaya.MFnNumericData.kFloat)  
    mfn_numeric_attr.setReadable(True)
    mfn_numeric_attr.setWritable(False)
    mfn_numeric_attr.setStorable(False)
    mfn_numeric_attr.setKeyable(False)
    
    # 3. ATTACHING THE ATTRIBUTES TO THE NODE #
    
    distanceDimension.addAttribute(distanceDimension.pointA)
    distanceDimension.addAttribute(distanceDimension.pointB)
    distanceDimension.addAttribute(distanceDimension.distance)
    
    # 4. DESIGN CIRCUITRY #
    
    distanceDimension.attributeAffects(distanceDimension.pointA, distanceDimension.distance)
    distanceDimension.attributeAffects(distanceDimension.pointB, distanceDimension.distance)
    
def initializePlugin(mobject):
    my_plugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        my_plugin.registerNode(node_name, node_id, nodeCreator, nodeInitializer)
    except:
        sys.stderr.write("Failed to register node: %s\n" %node_name)
        raise
        
def uninitializePlugin(mobject):
    my_plugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        my_plugin.deregisterNode(node_id)
    except:
        sys.stderr.write("Failed to deregister node: %s\n" %node_name)
        raise 