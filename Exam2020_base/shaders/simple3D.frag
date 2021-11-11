varying vec4 v_color;
varying vec4 v_normal;
varying vec4 v_s;
uniform vec4 u_light_diffuse; 
uniform vec4 u_mat_diffuse;
varying vec4 v_light_diffuse;

varying vec4 v_position;

uniform float u_cut_off_position;

void main(void)
{
	vec4 normal = normalize(v_normal);
	float lambert = max(dot(normal, normalize(v_s)), 0.0);
	// float phong = pow(max(dot(normalize(v_s), normalize(v_light_diffuse)), 0.0), u_mat_shininess);
	vec4 color = u_light_diffuse * u_mat_diffuse * lambert; //my code

	

	// create linear gradient from 0 to 1
	float falloff = 1.0;
	float gradient = (u_cut_off_position - v_position.x + falloff / 2.0) / falloff;
	gradient = pow(gradient, 3.0);
	color = mix(vec4(0.0, 0.0, 1.0, 1.0), vec4(1.0, 0.0, 0.0, 1.0), gradient);

	// if (v_position.x < u_cut_off_position)
	// {
	// 	color.r = 0.5;
	// }
	// else
	// {
	// 	color.b = 0.5;
	// 	//this is only the intensity value and a full white color
	// 	// gl_FragColor = lambert * vec4(1.0, 1.0, 1.0, 1.0);
	// }
	gl_FragColor = color;
}