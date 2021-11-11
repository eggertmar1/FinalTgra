
# try:
#     try:
#         from OpenGL.GL import * # this fails in <=2020 versions of Python on OS X 11.x
#     except ImportError:
#         print('Drat, patching for Big Sur')
#         from ctypes import util
#         orig_util_find_library = util.find_library
#         def new_util_find_library( name ):
#             res = orig_util_find_library( name )
#             if res: return res
#             return '/System/Library/Frameworks/'+name+'.framework/'+name
#         util.find_library = new_util_find_library
#         from OpenGL.GL import *
# except ImportError:
#     pass
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GLU
from math import * # trigonometry

import sys

from Base3DObjects import *

class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/shaders/simple3D.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))


        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/shaders/simple3D.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)
        result = glGetProgramiv(self.renderingProgramID, GL_LINK_STATUS)
        if (result != 1): # program didn't link
            print("Couldn't link shader program\nShader link Log:\n" + str(glGetProgramInfoLog(self.renderingProgramID))) 

        self.materialDiffuseLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_diffuse") # my code 
        self.materialShininessLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_shininess") # my code
        self.lightDiffuseLoc = glGetUniformLocation(self.renderingProgramID, "u_light_diffuse") # my code
        self.positionLoc			= glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)
        self.normalLoc			    = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)
        self.modelMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc	= glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")
        self.lightPosLoc            = glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.cutOffPos             = glGetUniformLocation(self.renderingProgramID, "u_cut_off_position")



    def use(self):
        try:
            glUseProgram(self.renderingProgramID)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_light_position(self, pos):
        glUniform4f(self.lightPosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_attribute_buffers(self, vertex_buffer_id):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
    
    # my code --------------------------------------------------

    def set_material_diffuse(self, red, green, blue):
        glUniform4f(self.materialDiffuseLoc, red, green, blue, 1.0)
    def set_light_diffuse(self, red, green, blue):
        glUniform4f(self.lightDiffuseLoc, red, green, blue, 1.0)

    # set material shininess
    def set_material_shininess(self, shininess):
        glUniform1f(self.materialShininessLoc, shininess)
    
    # set cut off position
    def set_cut_off_position(self, pos):
        glUniform1f(self.cutOffPos, pos)

    # def set_position_attribute(self, vertex_array):
    #     glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    # def set_normal_attribute(self, vertex_array):
    #     glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)
