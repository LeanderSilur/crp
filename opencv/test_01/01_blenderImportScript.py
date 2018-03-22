import bpy
import bmesh
import json

def RealizeBmesh(bm):
    mesh = bpy.data.meshes.new("mesh")  # add a new mesh
    obj = bpy.data.objects.new("MyObject", mesh)  # add a new object using the mesh
    scene = bpy.context.scene
    scene.objects.link(obj)  # put the object into the scene (link)
    scene.objects.active = obj  # set as the active object in the scene
    obj.select = True  # select object

    mesh = bpy.context.object.data
    # make the bmesh the object's mesh
    bm.to_mesh(mesh)
    bm.free()  # always do this when finished
    return obj
    
def CreateHistogramMesh():
    fd  = open("D:/180105_crp/crp/opencv/test_01/data_matplotlib.txt", "r")
    histo = json.loads(fd.read())
    fd.close()

    
    bm = bmesh.new()

    l = len(histo)
    w = len(histo[0])
    print(w)
    max = 0.001
    
    
    for i, line in enumerate(histo):
        for j, v in enumerate(line):
            if v > max:
                max = v
            bm.verts.new((pow((j/w), 0.5)*5, i, v))  # add a new vert
    
    bm.verts.ensure_lookup_table()
    
    for v in bm.verts:
        v.co.y /= 2
        v.co.z *= 5 / max
    
    for i in range(l - 1):
        for j in range(w - 1):
            bm.faces.new((   bm.verts[i * w + j],
                            bm.verts[i * w + j + 1],
                            bm.verts[(i + 1) * w + j + 1],
                            bm.verts[(i + 1) * w + j]))
        print(i)
        
    obj = RealizeBmesh(bm)

    obj.data.materials.append(bpy.data.materials.get("surface"))
    obj.data.materials.append(bpy.data.materials.get("wire"))
    
    # add a modifier (fancy stuff)
    mod = obj.modifiers.new("display wire", 'WIREFRAME')
    mod.thickness = 0.07
    mod.use_replace = False
    mod.material_offset = 1
    
#    bm.faces.new(
    
CreateHistogramMesh()

"""
verts = [(1, 1, 1), (0, 0, 0)]  # 2 verts made with XYZ coords
mesh = bpy.data.meshes.new("mesh")  # add a new mesh
obj = bpy.data.objects.new("MyObject", mesh)  # add a new object using the mesh

scene = bpy.context.scene
scene.objects.link(obj)  # put the object into the scene (link)
scene.objects.active = obj  # set as the active object in the scene
obj.select = True  # select object

mesh = bpy.context.object.data
bm = bmesh.new()

for v in verts:
    bm.verts.new(v)  # add a new vert


v1 = bm.verts.new((2.0, 2.0, 2.0))
v2 = bm.verts.new((-2.0, 2.0, 2.0))
v3 = bm.verts.new((-2.0, -2.0, 2.0))
bm.faces.new((v1, v2, v3))

# make the bmesh the object's mesh
bm.to_mesh(mesh)  
bm.free()  # always do this when finished
"""