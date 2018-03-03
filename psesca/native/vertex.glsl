#version 130
in vec4 position;
in vec4 vNormal;
centroid out vec4 normal;
uniform mat4 projection;
void main()
{
	gl_Position = projection * position;
	normal = vNormal;
}
