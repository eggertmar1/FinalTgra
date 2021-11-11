// Need variables for mat_diffuse, mat_specular, mat_shine
uniform vec4 u_material_diffuse;
uniform vec4 u_material_specular;
uniform vec4 u_material_emission;
uniform vec4 u_material_ambient;
uniform float u_material_shine;

uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;
uniform vec4 u_light_ambient;

uniform vec4 u_global_ambient;

uniform vec4 negVec = vec4(-1.0, -1.0, -1.0, 1.0);

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;


varying vec4 v_position;

uniform float u_cut_off_position;

void main(void)
{
	vec4 normal = normalize(v_normal); //Þarf ekki að normalize-a
	float lambert = max(dot(normal, normalize(v_s)), 0.0);
	//vec4 negVec = vec4(-1.0, -1.0, -1.0, 1.0);
	// My code for implementing color:
	float phong = max(dot(v_normal, v_h), 0.0);
	vec4 ambientColor = u_light_ambient * u_material_ambient;
	vec4 diffuseColor = u_light_diffuse * u_material_diffuse * lambert;
	vec4 specularColor = u_light_specular * u_material_specular * pow(phong, u_material_shine);
	vec4 lightCalculatedColor = diffuseColor + specularColor + u_global_ambient * ambientColor + u_material_emission;

	vec4 invSpecularColor = u_light_specular * abs(u_material_specular + negVec) * pow(phong, u_material_shine);
	vec4 invDiffuseColor = u_light_diffuse * abs(u_material_diffuse + negVec) * lambert;
	vec4 inverseCalculatedColor = invDiffuseColor + invSpecularColor + u_global_ambient * ambientColor + u_material_emission;
	
	float falloff = 1.0; //    flip this V to flip sides, change v_position.x to get a vertical line and to .y to horizontal
	float gradient = (u_cut_off_position - v_position.x + falloff / 2.0) / falloff;
	gradient = pow(gradient, 3.0);// This needs to be a odd num, And the vec4 bellow
	vec4 inverseColor = negVec + lightCalculatedColor;
	//vec4 color = mix(lightCalculatedColor, vec4(0.1, 0.1, 0.7, 0.0), gradient);
	vec4 color = mix(lightCalculatedColor, inverseCalculatedColor, gradient);

	gl_FragColor = color;


	//this is only the intensity value and a full white color
	//gl_FragColor = lambert * vec4(1.0, 1.0, 1.0, 1.0);
}