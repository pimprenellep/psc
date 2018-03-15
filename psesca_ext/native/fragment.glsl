#version 130
centroid in vec4 normal;
out vec4 color;
uniform vec4 light;
void main()
{
	color = dot(light, normal) * vec4( 0.3, 0.3, 0.3, 1.0 );
	gl_FragDepth = gl_FragCoord[2];
}
