attribute vec3 a_position;
attribute vec3 a_normal;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec4 u_light_position;
// uniform vec4 u_light_diffuse; 
// uniform vec4 u_mat_diffuse;
varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_position;

// varying vec4 v_color; // my code 
void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);
	// local coordinates

	position = u_model_matrix * position;
	v_normal = normalize(u_model_matrix * normal);
	// global coordinates

	v_s = normalize(u_light_position - position);

	// float lambert = max(dot(v_normal, v_s), 0.0); // my code 
	// v_color = u_light_diffuse * u_mat_diffuse * lambert; //my code

	position = u_view_matrix * position;
	//eye coordinates

	position = u_projection_matrix * position;
	//clip coordinates

	gl_Position = position;

	v_position = position;
}